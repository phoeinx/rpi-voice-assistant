<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/tactilenews/rpi-voice-assistant">
    <img src="assets/tactile_news_logo.png" alt="Logo" width="800" height="200">
  </a>

<h3 align="center"> Raspberry Pi Voice Assistant / Dialogbank </h3>

  <p align="center">
    This repository contains the code for a custom voice assistant that runs on a Raspberry Pi, uses the Google Speech-To-Text API and Elevenlabs Text-To-Speech API, and whose logic can be created and managed via a Voiceflow voice agent. This repository was created for the <a href="https://tactile.news/startseite/dialogbox/">Dialogbox</a> project of tactile.news and additionally contains functionality to build and install this project as a Debian package, run it as a user service and manage further hardware components with an Arduino.
    <br />
    <a href="https://github.com/tactilenews/rpi-voice-assistant?tab=readme-ov-file#getting-started"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/tactilenews/rpi-voice-assistant/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/tactilenews/rpi-voice-assistant/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#local-development-setup">Local Development Setup</a></li>
      </ul>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#technical-details">Technical Details</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#funding">Funding</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Use this project to setup your own Raspberry Pi Voice Assistant/Dialogbox.
The `dialogbank` directory contains the code for the voice assistant, the `arduino` directory contains the code for the Arduino components and the main directory contains the code for building a Debian package which can be used to install the voice assistant on a Raspberry Pi and run it as a user service.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [Elevenlabs Text-To-Speech API](https://elevenlabs.io/api)
* [Google Speech-To-Text API](https://pypi.org/project/google-cloud-speech/)
* [Voiceflow](https://www.voiceflow.com/)

### Based on

* [Voiceflow RPi Voice Assistant](https://github.com/voiceflow/rpi-voice-assistant) by [Frank Yu Cheng Gu](https://github.com/frankgu968)
* [Voiceflow Python Package](https://github.com/daiangan/voiceflow-python) by [Daian Gan](https://github.com/daiangan).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

For local development, you need to have the following:

1. A Linux machine (tested on Raspberry Pi OS) as some of the audio libraries are not available on other platforms.
2. A Google Cloud account with the Speech-To-Text API enabled and a service account key file. (See instructions below.)
3. A Elevenlabs account with the Text-To-Speech API enabled and an API key and voice_id.
4. A Voiceflow account with a voice agent you want to use for the voice assistant and the API key for the agent.

#### Google Cloud Account Setup
- Create an account: [https://console.cloud.google.com](https://console.cloud.google.com/)
- Setup prerequisites for being able to generate an authentication token from here: https://cloud.google.com/text-to-speech/docs/before-you-begin
- Store JSON file with key in path location you remember (and add it to .env file in next step)
- Should the JSON file not work, have a look here: Authentication Generation with Google Cli instructions: https://cloud.google.com/docs/authentication/external/set-up-adc
- More info: https://cloud.google.com/docs/authentication/application-default-credentials

### Local Development Setup

1. Clone the repo
   ```sh
   git clone https://github.com/tactilenews/rpi-voice-assistant
   ```
2. Install system dependencies
   ```sh
   sudo apt-get install -y python3 python3-pip python3-all-dev python3-pyaudio portaudio19-dev libsndfile1 mpv mpg123
   ```
3. Install Python dependencies
   ```sh
    pip install -r requirements.txt
   ```
   (If you don't use a virtual environment, you can set the `--break-system-packages` flag at your own risk.)
4. Create local .env file and set API Keys and other environment variables
   ```sh
   cp .env.example .env
   ```
   Fill in the `.env` file with the necessary API keys and environment variables. The `GOOGLE_APPLICATION_CREDENTIALS` variable should point to the path of the JSON file with the Google Cloud service account key. The `WAIT_TONE_PATH` variable should point to the path of the audio file that should be played while the voice assistant is processing a request and is optional.

5. Run the voice assistant.
   ```sh
   python3 -m dialogbank.main
   ```
   The voice assistant needs to be run as a module to allow relative imports. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Setup Options -->
## Setup Options
You can either run the voice assistant as a *script application* with the setup described in <a href="#local-development-setup">Local Development Setup</a> above or as *system user service* installed via a Debian package. For a setup with a Debian package, see the instructions in the `setup/SETUP_PACKAGE.md` file.

The main difference between the two setups is that the script application runs in a terminal in the foreground when started and quits when the terminal is closed. This is useful for development and testing. 

The system user service runs in the background, starts automatically on boot-up and can be started and stopped with the `systemctl` command. This is useful for running the voice assistant on a Raspberry Pi without a monitor and keyboard. The Debian package allows for easy installation. Once installed, the voice assistant automatically starts on boot-up and continues running/waiting for input until the Raspberry Pi is shut down.

For hardware setup instructions, including the Arduino components and necessary code, please refer to the `setup/SETUP_HARDWARE.md` file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Usage -->

## Usage
To start the voice assistant:

1. In local development setup run from the root directory:
   ```sh
   python3 -m dialogbank.main
   ```
2. In the Debian package setup, the voice assistant starts automatically on boot-up and can be started and stopped with the following commands:
   ```sh
   systemctl --user start dialogbank
   systemctl --user stop dialogbank
   ```

The voice assistant runs in a loop. In idle mode, it waits for a key press of 's' to start the interaction. 
Once the interaction is started, the voice assistant accesses the first Voiceflow state and possible speech output, synthesizes the audio, plays it to the user and waits for the user to speak. 
In a loop from then on:
1. The user's speech is transcribed by the Google Speech-To-Text API and sent to the Voiceflow agent. 
2. The agent processes the input and sends a response back to the voice assistant. 
3. The response is then synthesized by the Elevenlabs Text-To-Speech API and played back to the user.

The interaction can be interrupted at any time by pressing 'q'. The voice assistant then returns to idle mode.
If the end of the voice agent interaction is reached, the voice assistant also returns to idle mode.
The whole system (RPi) can be shut down by pressing 'p' at any point. (This is helpful when running the application in headless mode.)


### Performance Tips
- We cache the Elevenlabs API responses in the `cache` directory and parallelize the API requests to Elevenlabs based on sentence parts separated by punctuation. The more static the content of the voice agent (/the more parts of the response do not change) the more efficient the caching will be. If you start a new dialogue, the cache will be empty and the first request will take longer. Run it once to cache the responses, before testing the dialogue with users.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Technical Details -->
## Technical Details

### Debian Package
The Debian package is built using the `fpm` tool.
It builds a Python package bundling the `dialogbank` directory code and creates an entry point to the main script at `/usr/share/python/bin/dbank` which is called from the user service. The Debian package is specified in the `Makefile` and contains multiple files also found in the root directory that are used to register the user service (e.g. `/usr/lib/systemd/user/dialogbank.service` and `etc/xdg/autostart/dialogbank.desktop`) and install the Python package.

#### Building the Debian package

Building a Debian package allows easy installation and upgrades of the Dialogbank application and all system dependencies on Raspberry Pis running Debian (or Raspberry Pi OS which is based on Debian).

The Dockerfile in this repository contains the necessary prerequisites in order to build the Debian package, in particular [`fpm`](https://fpm.readthedocs.io/en/latest/) (a tool to build OS packages for different distributions from different source formats) as well as Python 3.11, the default Python version for Debian Bookworm.

In order to build the Debian package run the following command:

```
docker compose run --rm dev make
```

The binary Debian package will be written to `dist/dialogbank.deb`.

### Running the Dialogbank application as a user service
To allow creating a out-of-the-box dialogbank, we implemented running the software as a user service. Gained functionality includes: Starting of the software at boot time, automatic restarts in case of failure and logging. This allows users to just power on their device and start interacting with the voice assistant.

As the necessary functionality of our software (especially receiving keyboard input) is not what system/user services are usually used and designed for, the process was not straightforward and the resulting solution a bit hacky. Therefore a few notes on the implementation:

- Instead of a system service, we use a user service, meaning the service is started by the user and runs in the user's session. This is necessary for audio output, as the Pulse-Audio-Server is running in the user's session and the audio output is directed to the user's audio device. When running as a system service, the correct audio device is not accessible.
- To receive keyboard input we start the dialogbank software in an xterm window with: "xterm -e "/usr/share/python/bin/dbank". This opens a terminal window and executes the dialogbank software. If you attach a monitor to the RPi while running the service, you'll see the terminal window being opened. We have not experienced issues with dropped focus on the window etc., but this is admittedly a bit hacky.
- We require the graphical session to have started to be able to open the xterm window. In theory it should be possible to start the service after the graphical-session.target, but this appears to not be implemented in Raspberry Pi OS bookworm, see [here](https://github.com/raspberrypi/bookworm-feedback/issues/96). Therefore, we use the [xdg autostart](https://wiki.archlinux.org/title/XDG_Autostart) functionality to manually start the service, which is configured in `/etc/xdg/autostart/dialogbank.desktop`. This file is copied to the user's autostart directory during installation of the Debian package.
- As the dialogbank service crashes when there is no WIFI connection and the WIFI connection is sometimes established after the graphical session has been started and our service has been registered, a restart mechanism is vital. Ideally, one would like to spread out restart times with the `RestartSec/RestartSteps` configuration options in the service file. However, these options are only available from systemd version 254 and Raspberry Pi OS Bookworm is currently using version 252. Therefore we set the restart time to once every second (instead of once every 100ms as is the default) and set the `StartLimitInterval` option to 0, which effectively disables any start limiting. (Meaning that the service will never stop to retry starting after a failure.)

### Logging
For logging we use the `journalctl` functionality.
The logs regarding the start/restart/stops of the dialogbank service are automatically logged to `journalctl` due to being a user system service.
As we start the dialogbank software in an xterm window, the logs of the software are written to the terminal window and not automatically logged to `journalctl`. We use `systemcat` to manually log the output of the xterm window to `journalctl`. This is done in the `dialogbank.service` file in the `ExecStart` command. It's not possible to log from the user `dialogbank` that way, but we set the tag `dialogbank`. 
To see the logs of the dialogbank software and service (so everything), run `journalctl --user -u dialogbank`.
To see only the logs of the dialogbank software, run `journalctl -t dialogbank`.

`journalctl` logs are persistent across reboots and can be accessed at any time. They are also rotated automatically if space limitations arise.
To access logs there is a sophisticated filtering system available, see `man journalctl` for more information.

E.g. to see the last 50 messages of the dialogbank service from the last hour, run: `journalctl -n 50 --user -u dialogbank --since "1 hour ago"`.

### Interacting with dialogbank user service

Get status: `systemctl --user status dialogbank`

Start service: `systemctl --user start dialogbank`

Stop service: `systemctl --user stop dialogbank` 

Reload service manager after changes to dialogbank service file: `systemctl --user daemon-reload` 

Reset failed services (e.g. after uninstalling package): `systemctl --user reset-failed`

### Performance Considerations: Caching, Parallelization & API Parameters
To allow a natural conversation it is important to keep response times as low as possible. The bottleneck in our application are the different APIs we need to call to generate a response. We implemented several strategies to improve the performance of the application:
1. Caching
Implemented for the TTS queries to Elevenlabs and implemented in the `dialogbank/elevenlabs.py` file. We split each generated text response according to punctuation and then check if we've already queried this sentence part from Elevenlabs before. If no, we query the audio file and store it under the hash for the sentence part. If yes, we access the sentence part directly from disk. There is currently no mechanism to empty the cache. If you want to clear the cache, you can delete the `cache` directory. The stored audio files are small and the cache is not expected to grow very large (we have seen ~100MB after a few weeks of testing). Dependent on your storage capabilities and the expected usage of the application, you might want to think about making the cache directory temporary or implementing a cache clearing mechanism.
2. Parallelization
As the time necessary for synthetisation of speech from text from Elevenlabs increases linearly with the length of the text, we parallelize the requests to Elevenlabs. We split the text into sentence parts and query each sentence part in parallel. The parallelization is implemented in the `dialogbank/elevenlabs.py` file.
3. API Settings
For the Elevenlabs API we always set the following two query parameters: `"optimize_streaming_latency": "4", "output_format": "mp3_22050_32"`. The `optimize_streaming_latency` parameter is set to 4, which leads to: "max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates)." (According to Elevenlabs documentation.) We chose the output_format with lowest sample_rate and kbps to also increase efficiency of transmission and storage of the audio files (as they are generally smaller).

### Development notes
- If you add new dependencies to the project, make sure to add them to the `requirements.txt` file **and** in the `setup.py` file.

### Code Structure of Dialogbank Application
The code for the voice assistant is structured as follows:
- `audio.py`: Provides functionality for playing audio files and audio streams and handle Google Speech-To-Text API responses.
- `elevenlabs.py`: Provides functionality for querying the Elevenlabs Text-To-Speech API and caching the responses.
- `led_status.py`: Provides functionality for updating the status of the LED strip across multiple processes (each process holds its own instance of the `LEDStatusManager` class provided).
- `voiceflow` directory: Contains the code for querying the Voiceflow API and handling its responses.
- `main.py`: Contains the entry point and runs the interaction loop of the voice assistant. It starts a main process which waits for keyboard input to start the interaction and then starts a new process for each interaction. The main process continues to wait for keyboard input to stop the interaction or shut down the system. There can always max. one interaction process be running. The main process also starts a separate process for updating the WIFI status LED on the LED strip.

### LED Status Strip
As an optional component the LED Strip can be used to display the status of the voice assistant without having to access the logs. The LED strip is controlled via the `blinkt` library, the meaning of the LED colors is described below.

The code for the LED strip updates is implemented in the `led_status.py` file and is offered through the `LEDStatusManager` class. To allow updates to the LED strip from multiple processes, the `LEDStatusManager` class uses a `shared_memory.ShareableList` to store the current status of the LEDs. Each process holds its own instance of the `LEDStatusManager` class which updates the shared list with the new status. After each update the `LEDStatusManager` class writes the new status of all LEDs to the LED strip via the `blinkt` library.
A `LEDStatusManager` instance can be created from an existing `ShareableList` or by creating a new one.

### Meaning of status LED strip colors

No LED lights up at all -> application is not running.
LED lights are read from left to right.

**LED1: Wifi**<br>
🔴 Red - No Wifi <br>
🟢 Green - Has Wifi <br>

**LED2: Dialogbank application running** <br>
🟡 Yellow - Start up <br>
🟢 Green - Ready <br>
🔵 Blue - Off-hook handset <br>

**LED3: Google ASR API** <br>
🔵 Blue: Running request <br>
🟢 Green: Successful request <br>
🔴 Red: Unsuccessful request <br>

**LED4: Voiceflow API** <br>
🔵 Blue: Running request <br>
🟢 Green: Last request successful <br>
🔴 Red: Last request failed <br>

**LED5: Elevenlabs API** <br>
🔵 Blue: Running request <br>
🟢 Green: Last request successful <br>
🔴 Red: Last request failed <br>

**LED6: Listening** <br>
💗 Pink: Listening <br>
⚪ Nothing: Not listening <br>

### Remote maintenance
To allow access to RaspberryPis running the dialogbank software/prototypes in the field without having to be in the same network, we use [tailscale](https://tailscale.com). Tailscale is a VPN service that allows you to connect to devices in a network without having to open ports in the router or having to be in the same network. The RaspberryPi running the dialogbank software needs to have the tailscale client installed and to be connected to the tailscale network. More information on how to setup Tailscale can be found in "7. Setup Tailscale" in the `setup/SETUP_HARDWARE.md` file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License
`Dialogbank` is developed by [tactile.news](https://tactile.news) and is licensed under the [MIT license](https://github.com/tactilenews/rpi-voice-assistant/blob/main/LICENSE).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Funding -->

<!-- ## Funding
<div align="center">
  <a href="https://miz-babelsberg.de">
    <img src="assets/miz-logo.png" alt="Logo" width="400" height="200">
  </a>


The [Medieninnovationszentrum Babelsberg](https://miz-babelsberg.de) funded the development of this project.

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/tactilenews/rpi-voice-assistant.svg?style=for-the-badge
[contributors-url]: https://github.com/tactilenews/rpi-voice-assistant/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/tactilenews/rpi-voice-assistant.svg?style=for-the-badge
[forks-url]: https://github.com/tactilenews/rpi-voice-assistant/network/members
[stars-shield]: https://img.shields.io/github/stars/tactilenews/rpi-voice-assistant?style=for-the-badge
[stars-url]: https://github.com/tactilenews/rpi-voice-assistant/stargazers
[issues-shield]: https://img.shields.io/github/issues/tactilenews/rpi-voice-assistant?style=for-the-badge
[issues-url]: https://github.com/tactilenews/rpi-voice-assistant/issues
[license-shield]: https://img.shields.io/github/license/tactilenews/rpi-voice-assistant?style=for-the-badge
[license-url]: https://github.com/tactilenews/rpi-voice-assistant/blob/main/LICENSE.txt