from multiprocessing import Process
from dataclasses import dataclass

from requests import HTTPError
import os
import signal
import time
import requests
from pathlib import Path

import structlog
import sys
import uuid

from dotenv import load_dotenv
from google.cloud import speech_v1 as speech

from . import audio
from .voiceflow import Voiceflow
from .elevenlabs import ElevenLabs

from typing import Dict, Any
JSON = Dict[str, Any]

import RPi.GPIO as GPIO
import time


# Setup
load_dotenv()
load_dotenv("/etc/dialogbank/dialogbank.env")

TELEPHONE_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(TELEPHONE_PIN, GPIO.IN)

# Google ASR Config Values
RATE = 16000
CHUNK = 128
language_code = "de-DE"  #BCP-47 language tag
FAILED_REQUEST = -1

WIFI_CHECK_PERIOD = 1  # seconds

log = structlog.get_logger(__name__)

@dataclass
class Settings:
    EL_API_KEY: str
    EL_VOICE_ID: str
    VF_API_KEY: str
    WAIT_TONE_PATH: str | None

    @classmethod
    def load(cls):
        dialogbank_id = os.getenv("DIALOGBANK_ID")
        airtable_api_key = os.getenv("AIRTABLE_API_KEY")
        airtable_base_id = os.getenv("AIRTABLE_BASE_ID")
        airtable_table_id = os.getenv("AIRTABLE_TABLE_ID")

        response = requests.get(
            f"https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_id}", 
            params={"filterByFormula" : f"dialogbank_id='{dialogbank_id}'"},
            headers={"Authorization": f"Bearer {airtable_api_key}"},
        )

        try:
            response.raise_for_status()
        except HTTPError as err:
            raise Exception("Could not query configuration from airtable.") from err

        config = response.json()["records"][0]["fields"]

        wait_tone_path = None
        if "wait_tone" in config:
            wait_tone_url = config["wait_tone"][0]["url"]
            response = requests.get(wait_tone_url)
            file = Path.cwd().joinpath('wait_tone')
            file.write_bytes(response.content)
            wait_tone_path = file

        settings = Settings(
            EL_API_KEY = os.getenv("EL_API_KEY"),
            EL_VOICE_ID = config.get("el_voice_id"),
            VF_API_KEY = config.get("vf_api_key"),
            WAIT_TONE_PATH = wait_tone_path,
        )

        if not settings.EL_API_KEY:
            raise Exception("Missing Elevenlabs api key configuration.")
        if not settings.EL_VOICE_ID:
            raise Exception("Missing Elevenlabs voice id configuration.")
        if not settings.VF_API_KEY:
            raise Exception("Missing Voiceflow api key configuration.")

        return settings

def reboot():
    os.system("sudo reboot")


def generate_and_play_elevenlabs_audio(
    el: ElevenLabs, message: str, audio_player: audio.AudioPlayer
) -> bool:
    """
        Generates audio using the Elevenlabs API and plays it back.
    """
    try:
        stream = el.generate_audio_stream(message)
        audio_player.play_audio_stream(stream)
    except Exception as e:
        log.error("Error in Elevenlabs interaction", error=str(e))
        sys.exit(1)


def unpack_vf_response(vf_response: JSON) -> tuple[bool, str | None]:
    messages = []
    end = False
    for item in vf_response:
        if item["type"] == "speak":
            message = item["payload"]["message"]
            log.debug("[Voiceflow]: Got response", response=message)
            messages.append(message)
        elif item["type"] == "end":
            log.debug("[Voiceflow]: Got signal for end of interaction.")
            end = True
    full_message = ' '.join(m.strip() for m in messages if m.strip())
    log.debug("Voiceflow generated message", message=full_message)
    return end, full_message


def terminate_interaction(
    vf: Voiceflow,
    elevenlabs_client: ElevenLabs,
    audio_player: audio.AudioPlayer,
    message: str = None,
):
    if message:
        log.debug("[Voiceflow]: Got end response", response=message)
        generate_and_play_elevenlabs_audio(elevenlabs_client, message, audio_player)
    log.debug("[Voice Assistant]: =========END OF INTERACTION=========")
    vf.user_state.delete()


def is_successful_vf_response(response: JSON) -> bool:
    for item in response:
        if "type" in item:
            return True
    return False


def run_voiceflow_launch_request(voiceflow_client: Voiceflow) -> dict:
    try:    
        log.debug(
            "[Voiceflow]: Requesting first voiceflow interaction.",
            voiceflow_user_id=voiceflow_client.user_id,
        )
        vf_response = voiceflow_client.interact.launch()
        if not is_successful_vf_response(vf_response):
            log.error("Unsuccessful Voiceflow API request.", error=str(e))
            sys.exit(1)
    except Exception as e:
        log.error("Error in voiceflow interaction", error=str(e))
        sys.exit(1)
    return vf_response


def run_voiceflow_interact_request(voiceflow_client: Voiceflow, utterance: str) -> dict:
    try:    
        log.debug(
            "[Voiceflow]: Requesting voiceflow text interaction.",
            voiceflow_user_id=voiceflow_client.user_id,
        )
        vf_response = voiceflow_client.interact.text(user_input=utterance)
        if not is_successful_vf_response(vf_response):
            log.error("Unsuccessful Voiceflow API request.", error=str(e))
            sys.exit(1)
    except Exception as e:
        log.error("Error in voiceflow interaction", error=str(e))
        sys.exit(1)
    return vf_response


def recognize_user_input(
    google_asr_client: speech.SpeechClient,
    google_streaming_config: speech.StreamingRecognitionConfig,
    stream,
) -> str:
    log.debug("[Voice Assistant]: Start listening.")
    stream.start_buf()

    audio_generator = stream.generator()
    requests = (
        speech.StreamingRecognizeRequest(audio_content=content)
        for content in audio_generator
    )

    try:
        responses = google_asr_client.streaming_recognize(
            google_streaming_config, requests
        )
        utterance = audio.process(responses)
        log.debug("[Google ASR]: Recognized utterance", utterance=utterance)
    except Exception as e:
        log.error("Error in Google ASR interaction", error=str(e))
        sys.exit(1)

    stream.stop_buf()
    log.debug("[Voice Assistant]: Stop listening.")
    return utterance


# TODO: Move WIFI Check to single LED.
# def run_update_wifi_availability(shared_status_list: shared_memory.ShareableList):
# def check_internet_availability(self, host="8.8.8.8", port=53, timeout=2):
# """
# Host: 8.8.8.8 (google-public-dns-a.google.com)
# OpenPort: 53/tcp
# Service: domain (DNS/TCP)
# """
# try:
#     socket.setdefaulttimeout(timeout)
#     socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
#     return True
# except socket.error as ex:
#     print(ex)
#     return False


def run_dialogbench(
    voiceflow_client: Voiceflow,
    google_asr_client: speech.SpeechClient,
    google_streaming_config: speech.StreamingRecognitionConfig,
    elevenlabs_client: ElevenLabs,
    settings: Settings,
):
    def sigterm_handler(signum, frame):
        # TODO: The signal handler gets registered to also terminate the audio child process when the dialog loop is interrupted.
        # The AudioPlayer object has a __del__ method that cleans the process up.
        # However, the call to sys.exit() usually leads to the call of the __del__ function on the AudioPlayer,
        # this is however not guaranteed.
        # If time: check if more robust solution is possible.
        sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)
    audio_player = audio.AudioPlayer(settings.WAIT_TONE_PATH)

    with audio.MicrophoneStream(RATE, CHUNK) as stream:
        # Each loop iteration represents one interaction of one user with the voice assistant
        audio_player.async_waiting_tone() #signal processing to user

        vf_response = run_voiceflow_launch_request(voiceflow_client)

        end, message = unpack_vf_response(vf_response)

        while not end:
            generate_and_play_elevenlabs_audio(elevenlabs_client, message, audio_player)

            utterance = recognize_user_input(
                google_asr_client, google_streaming_config, stream
            )

            audio_player.async_waiting_tone() #signal processing to user
            vf_response = run_voiceflow_interact_request(voiceflow_client, utterance)

            end, message = unpack_vf_response(vf_response)

        terminate_interaction(
            voiceflow_client, elevenlabs_client, audio_player, message
        )


def wait_until_telephone_picked_up():
    while not GPIO.input(TELEPHONE_PIN):
        time.sleep(0.2)

        # TODO: Update Code to run reset with directly connected reset button.
        # if userInput == "p":
        #     log.debug("[Voice Assistant]: User signal to shutdown system received. Shutting down.")
        #     reboot()


def main():
    # Run setup for Dialogbench Loop
    settings = Settings.load()

    voiceflow_client = Voiceflow(
        api_key=settings.VF_API_KEY,
        user_id=uuid.uuid4()
    )
    # Remove any potential user state to always start from beginning of voice assistant
    voiceflow_client.user_state.delete()

    google_asr_client = speech.SpeechClient()
    google_asr_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )
    google_streaming_config = speech.StreamingRecognitionConfig(
        config=google_asr_config, interim_results=False
    )

    elevenlabs_client = ElevenLabs(
        api_key=settings.EL_API_KEY, 
        voice_id=settings.EL_VOICE_ID,
    )

    while True:
        voiceflow_client.user_id = uuid.uuid4()
        log.debug(
            "[Voice Assistant]: Starting voice assistant",
            voiceflow_user_id=voiceflow_client.user_id,
        )

        # TODO: Update Wifi-Process to run with single, directly connected WIFI LED.
        # wifi_process = Process(target=run_update_wifi_availability, args=(led_status_manager.status,), daemon=True)
        # wifi_process.start()

        wait_until_telephone_picked_up()

        p = Process(
            target=run_dialogbench,
            args=(
                voiceflow_client,
                google_asr_client,
                google_streaming_config,
                elevenlabs_client,
                settings,
            ),
        )  # , daemon=True) TODO: why daemon?
        p.start()

        log.debug(
            "[Dialogbench]: Running busy waiting loop to listen for interrupt signal."
        )
        # TODO: Check if logic covers all cases sufficiently.
        while p.is_alive() and GPIO.input(TELEPHONE_PIN):
            time.sleep(0.2)

            # TODO: Update Code to run reset with directly connected reset button.
            # if userText == "p":
            #     log.debug("[Voice Assistant]: User signal to shutdown system received. Shutting down.")
            #     reboot()

        p.terminate()
        time.sleep(1)

if __name__ == "__main__":
    main()
