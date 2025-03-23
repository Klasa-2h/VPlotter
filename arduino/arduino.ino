#include <SPI.h>
#include <SD.h>

#define stepPinx 2
#define dirPinx 5
#define stepPiny 3
#define dirPiny 6

#define startStopButton A1
#define pauseButton A0

#define enablePin 8
#define pinSD 10

File dataFile;
File variant;

int motor_speed = 4;
int left_motor_steps = 0;
int right_motor_steps = 0;

void setup() {
  pinMode(enablePin, OUTPUT);
  digitalWrite(enablePin, HIGH);

  pinMode(startStopButton, INPUT_PULLUP);
  pinMode(pauseButton, INPUT_PULLUP);

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
 
  while (digitalRead(startStopButton) == HIGH){}

  digitalWrite(enablePin, LOW);
  delay(700);
}

void loop() {
  if (digitalRead(startStopButton) == LOW){stopAll();}
  if (digitalRead(pauseButton) == LOW){
    delay(200);
    while(true){
      if (digitalRead(pauseButton) == LOW){
        delay(300);
        break;
      }
    }
  }

  int left_direction = LOW;
  int right_direction = LOW;

  if (left_motor_steps < 0) {left_direction = HIGH;} 
  if (right_motor_steps > 0) {right_direction = HIGH;}

  // Left motor
  digitalWrite(dirPinx, left_direction);
  digitalWrite(stepPinx, HIGH);
  delayMicroseconds(1000);
  digitalWrite(stepPinx, LOW);
  delayMicroseconds(1000);

  // Right motor
  digitalWrite(dirPiny, right_direction);
  digitalWrite(stepPiny, HIGH);
  delayMicroseconds(1000);
  digitalWrite(stepPiny, LOW);
  delayMicroseconds(1000);

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