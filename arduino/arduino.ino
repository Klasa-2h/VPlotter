#include <SPI.h>
#include <SD.h>

#define stepPinx 2
#define dirPinx 5
#define stepPiny 3
#define dirPiny 6

#define enablePin 8
#define pinSD 10

#define button 9

File dataFile;
File variant;

int motor_speed = 10;
int left_motor_steps = 0;
int right_motor_steps = 0;

void setup() {
  pinMode(enablePin, OUTPUT);
  digitalWrite(enablePin, LOW);
  
  pinMode(button, INPUT_PULLUP);

  pinMode(stepPinx, OUTPUT);
  pinMode(dirPinx, OUTPUT);
  pinMode(stepPiny, OUTPUT);
  pinMode(dirPiny, OUTPUT);


  if (!SD.begin(pinSD)) {
    stopAll();
  }

  variant = SD.open("/");
  if (!variant){
    stopAll();
  } 

  while (true) {
    dataFile = variant.openNextFile();  

    if (!dataFile) {
      stopAll();
    }

    if (!dataFile.isDirectory()) {
      break;  
    }
  }

  load_data();

  while (digitalRead(button) == HIGH){

  }

  delay(200);
}

void loop() {
  if (digitalRead(button) == LOW){
    stopAll();
  }

  int left_direction = LOW;
  int right_direction = LOW;

  if (left_motor_steps < 0) {
    left_direction = HIGH;
  } if (right_motor_steps > 0) {
    right_direction = HIGH;
  }

  left_motor_steps = abs(left_motor_steps);
  right_motor_steps = abs(right_motor_steps);

  if (left_motor_steps > 0) {
    digitalWrite(dirPinx, left_direction);
    digitalWrite(stepPinx, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPinx, LOW);
    delayMicroseconds(1000);
    left_motor_steps--;
  }
  if (right_motor_steps > 0) {
    digitalWrite(dirPiny, right_direction);
    digitalWrite(stepPiny, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPiny, LOW);
    delayMicroseconds(1000);
    right_motor_steps--;
  }
  load_data();
  delay(motor_speed);
}

void load_data(){
  if (dataFile.available()) {
    String couple = dataFile.readStringUntil('\n');
    sscanf(couple.c_str(), "%d %d", &left_motor_steps, &right_motor_steps);
  } else {
    stopAll();
  }
}

void stopAll(){
  digitalWrite(enablePin, HIGH);
  dataFile.close();
  while(1);
}