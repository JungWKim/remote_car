
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly
//  Serial.println(data);
//  delay(100);

    String data = Serial.readStringUntil('\n');
    int long_data = data.toInt(); 
    Serial.println(long_data);
}
