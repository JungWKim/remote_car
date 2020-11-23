#include <MsTimer2.h>

#define encoderL 18
#define encoderR 21

const float ppr = 235;
volatile float pulseCountL = 0;
volatile float pulseCountR = 0;
volatile float rpmL, rpmR;

void pulseCounterL() { pulseCountL++; }
void pulseCounterR() { pulseCountR++; }

void rpmCalculation()
{
  rpmL = (pulseCountL / ppr) * (60.0 / 0.5);
  rpmR = (pulseCountR / ppr) * (60.0 / 0.5);

  Serial.println(rpmL - rpmR);

//  Serial.print("Left pulse: ");
//  Serial.println(pulseCountL);
//  Serial.print("Left rpm : ");
//  Serial.println(rpmL);
//  Serial.print("Right pulse: ");
//  Serial.println(pulseCountR);
//  Serial.print("Right rpm : ");
//  Serial.println(rpmR);

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
