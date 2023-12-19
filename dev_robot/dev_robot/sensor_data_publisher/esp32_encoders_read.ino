#include <Arduino.h>

#define enc_RA  15
#define enc_RB  4

#define enc_LA  16
#define enc_LB  2
volatile int count_R = 0;
volatile int count_L = 0;

unsigned long lastPrintTime = 0;
const unsigned long printInterval = 300;  // Interval for serial print in milliseconds

void setup() {
  Serial.begin(115200);
  enc_def();
}

void loop() {
   unsigned long currentTime = millis();
  if (currentTime - lastPrintTime >= printInterval) {
    lastPrintTime = currentTime;

    noInterrupts();  // Start of critical section
    int localCountL = count_L;
    int localCountR = count_R;
    interrupts();  // End of critical section

//    Serial.print("Left Encoder Count: ");/
    Serial.print(localCountL);Serial.print(",");
//    Serial.print(" | Right Encoder Count: ");/
    Serial.println(localCountR);
  }
}


void Update_encR() {
   if (digitalRead(enc_RA) == digitalRead(enc_RB)) count_R--;
   else count_R++;
}

void Update_encL() {
  if (digitalRead(enc_LA) == digitalRead(enc_LB)) count_L--;
  else count_L++;
}

void enc_def() {
  pinMode(enc_RA, INPUT);
  pinMode(enc_RB, INPUT);
  pinMode(enc_LA, INPUT);
  pinMode(enc_LB, INPUT);
  attachInterrupt(digitalPinToInterrupt(enc_RA), Update_encR, RISING);
  attachInterrupt(digitalPinToInterrupt(enc_LA), Update_encL, RISING);
}