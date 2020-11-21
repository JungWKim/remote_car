#include <MsTimer2.h>

#define encoderL 18
#define encoderR 21

const int ppr = 235;
volatile int pulseCountL = 0;
volatile int pulseCountR = 0;
volatile int rpmL, rpmR;

void pulseCounterL() { pulseCountL++; }
void pulseCounterR() { pulseCountR++; }

void rpmCalculation()
{
  rpmL = (int)((pulseCountL / ppr) * (60.0 / 0.5));
  rpmR = (int)((pulseCountR / ppr) * (60.0 / 0.5));

  Serial.println(rpmL - rpmR);

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
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

}
