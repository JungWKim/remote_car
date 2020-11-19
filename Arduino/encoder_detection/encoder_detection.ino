#include <MsTimer2.h>

#define encoderL 8
#define encoderR 9

const int ppr = 235;
const int target_rpm_gap = 500;
int pulseCountL = 0;
int pulseCountR = 0;
int rpmL, rpmR;

void pulseCounterL() { pulseCountL++; }
void pulseCounterR() { pulseCountR++; }

void rpmCalculation()
{
  rpmL = (int)((pulseCountL / ppr) * (60.0 / 0.5));
  rpmR = (int)((pulseCountR / ppr) * (60.0 / 0.5));

  pulseCountL = 0;
  pulseCountR = 0;
}

void setup() {
  // put your setup code here, to run once:
  pinMode(encoderL, INPUT);
  pinMode(encoderR, INPUT);

  attachInterrupt(digitalPinToInterrupt(encoderL), pulseCounterL, RISING);
  attachInterrupt(digitalPinToInterrupt(encoderR), pulseCounterR, RISING);

  MsTimer2::set(500, rpmCalculation);
  MsTimer2::start();
  Serial.begin(57600);
}

void loop() {
  // put your main code here, to run repeatedly:

}
