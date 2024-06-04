#include "Keyboard.h"
bool btn = false;
bool aiphone = false;  // rot D2
bool resetbtn = false; // weiß D3
bool pwrbtn = false;   // D4

const int pinGabel = 2;
const int pinReset = 3;
const int pinPower = 4;

void setup() {

  pinMode(pinGabel, INPUT_PULLUP);
  pinMode(pinReset, INPUT_PULLUP);
  pinMode(pinPower, INPUT_PULLUP);

  // initialize control over the keyboard:
  Keyboard.begin();
}

void loop() {
  bool btn = !digitalRead(pinGabel); // Telefonhörergabel, I can hear you!
  if (btn != aiphone) {
    aiphone = btn;
    if (aiphone) // Telefongabel abgenommen
    {
      Keyboard.println("s");
      Keyboard.releaseAll();
      delay(1000);
    } else // Telfongabel aufgelegt
    {
      Keyboard.println("q");
      Keyboard.releaseAll();
      delay(1000);
    }
  }

  btn = !digitalRead(pinReset);
  if (btn != resetbtn) {
    resetbtn = btn;
    if (resetbtn) {
      Keyboard.press(KEY_LEFT_CTRL);
      Keyboard.press('c');
      Keyboard.releaseAll();
      Keyboard.println(
          "pzthon3 /m dialogbank.main"); // oder wie auch imemr man das Programm
                                         // neu startet
      delay(1000);
    }
  }

  btn = !digitalRead(pinPower); // Raspberry Pi fährt runter
  if (btn != pwrbtn) {
    pwrbtn = btn;
    if (pwrbtn) {
      Keyboard.press(KEY_LEFT_CTRL);
      Keyboard.releaseAll();
      Keyboard.println("shutdown");
      delay(1000);
    }
  }
}