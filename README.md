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
    This repository contains the code for a custom voice assistant that runs on a Raspberry Pi, uses the Google Speech-To-Text API and Elevenlabs Text-To-Speech API, and whose logic can be created and managed via as a Voiceflow voice agent. This repository was created for the <a href="https://tactile.news/startseite/dialogbox/">Dialogbox</a> project of tactile.news and additionally contains functionality to build and install this project as a Debian package, run it as a user service and manage further hardware components with an Arduino.
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
- Should JSON file not work: Authentication Generation with Google Cli instructions: https://cloud.google.com/docs/authentication/external/set-up-adc
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


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Technical Details -->
## Technical Details

### Building the Debian package

Building a Debian package allows easy installation and upgrades of the Dialogbank application and all system dependencies on Raspberry Pis running Debian (or Raspberry Pi OS which is based on Debian).

The Dockerfile in this repository contains the necessary prerequisites in order to build the Debian package, in particular [`fpm`](https://fpm.readthedocs.io/en/latest/) (a tool to build OS packages for different distributions from different source formats) as well as Python 3.11, the default Python version for Debian Bookworm.

In order to build the Debian package run the following command:

```
docker compose run --rm dev make
```

The binary Debian package will be written to `dist/dialogbank.deb`.

### Interacting with dialogbank user service

Get status: `systemctl --user status dialogbank`

Start service: `systemctl --user start dialogbank`

Stop service: `systemctl --user stop dialogbank` 

Reload service manager after changes to dialogbank service file: `systemctl --user daemon-reload` 

Reset failed services (e.g. after uninstalling package): `systemctl --user reset-failed`

### Development notes
- If you add new dependencies to the project, make sure to add them to the `requirements.txt` file **and** in the `setup.py` file.

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