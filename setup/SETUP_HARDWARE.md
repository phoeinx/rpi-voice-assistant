# Setup Hardware

## Prerequisites
- Raspberry Pi 4 or 5 (4GB or 8GB RAM recommended)
  - The following setup instructions are tested with a Raspberry Pi 5. The system has worked completely on a RPi4, too, though.
- Arduino Micro 5V
  - In theory other Arduino boards that support they "keyboard.h" library should work, too. The setup has been tested with an Arduino Micro 5V.
- An USB-Audio Device
  - E.g. a Headset with an USB Audio Adapter or a USB Telephone Receiver
- Push Buttons for the Arduino and 

## Recommended Installation Steps
1. Install the software on the Raspberry Pi and test that it works using the USB Audio Adapter, headphones with a microphone and a keyboard (either a physical one connected directly to the Raspberry Pi or the one of your own device via SSH).
2. If you want to use the USB Telephone Receiver, connect it to the Raspberry Pi via an USB port and test that it works. You probably will have to adjust the audio settings in the Raspberry Pi OS and select the USB Telephone Receiver as the default audio input and output device. In the Desktop GUI you can do this via the audio settings in the task bar.
3. Setup the hardware components for the Arduino. We used a breadboard, resistors and jumper wires to connect the push buttons to the Arduino. If you have never done this before, check out a tutorial on how to connect a push button, e.g. [this one](https://docs.arduino.cc/built-in-examples/digital/Button/). Also connect the phone receiver button to the Arduino like you would connect a push button (you don't need an additional resistor for the phone receiver button). Check out the pins in the Arduino sketch in the `arduino` directory of this repository to see where to connect each button (or adapt the sketch to your setup). (TODO: CHECK IF TRUE FOR PHONE RECEIVER BUTTON)
4. Install the Arduino IDE on your computer and upload the sketch from the `arduino` directory of this repository to the Arduino. You can find a tutorial on how to upload a sketch to an Arduino [here](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-uploading-a-sketch/). Make sure to select the correct board and port in the Arduino IDE. To test that the installation was successful, open a text editor on your computer and press the push buttons. You should see the corresponding letters being typed in the text editor.
5. Connect the Arduino to the Raspberry Pi via an USB cable. The Arduino is now ready to send keyboard inputs to the Raspberry Pi. (You can again test this by opening a text editor on the Raspberry Pi and pressing the push buttons.) Start the dialogbank program and check that the buttons work as expected.
