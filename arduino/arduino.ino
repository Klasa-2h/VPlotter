#include <SPI.h>
#include <SD.h>

#define stepPinx 2
#define dirPinx 5
#define stepPiny 3
#define dirPiny 6

#define enablePin 8
#define pinSD 10

#define stepsPerRevolution 200  

File dataFile;

bool fileEnd = false;
bool motor_right_status = true;
bool motor_left_status = true;
int motor_speed = 100;

void setup() {
  Serial.begin(9600);

  pinMode(enablePin, OUTPUT);

  pinMode(stepPinx, OUTPUT);
  pinMode(dirPinx, OUTPUT);
  pinMode(stepPiny, OUTPUT);
  pinMode(dirPiny, OUTPUT);

  digitalWrite(enablePin, LOW);

  Serial.println("Inicjalizacja karty SD...");
  if (!SD.begin(pinSD)) {
    Serial.println("Błąd inicjalizacji karty SD!");
    while (1);
  }
  Serial.println("Inicjalizacja powiodła się pomyślnie!");

  Serial.println("Weryfikacja zgodności plików...");
  if (SD.exists("Dane.txt")) {
    dataFile = SD.open("Dane.txt");
    Serial.println("Weryfikacja powiodła się!");
  } else {
    Serial.println("Weryfikacja nie powiodła się/Brak pliku!");
    while (1);
  }
  Serial.println("Dane: ");

  delay(1500);
}

void loop() {
  if (fileEnd) {
    return;
  }

  if (motor_right_status == true && motor_left_status == true) {
    motor_right_status = false;
    motor_left_status = false;

    if (dataFile) {
      if (dataFile.available()) {
        int left_motor_steps = 0;
        int right_motor_steps = 0;
        int delay_left = 0;
        int delay_right = 0;
        String couple = dataFile.readStringUntil('\n');

        sscanf(couple.c_str(), "%d %d", &left_motor_steps, &right_motor_steps);

        Serial.println(left_motor_steps);
        Serial.println(right_motor_steps);

        if (left_motor_steps == right_motor_steps){
          delay_left = motor_speed;
          delay_right = motor_speed;
        } if (left_motor_steps > right_motor_steps){
          delay_left = (left_motor_steps / right_motor_steps) * motor_speed;
          delay_right = motor_speed;
        } if (right_motor_steps > left_motor_steps){
          delay_right = (right_motor_steps / left_motor_steps) * motor_speed;
          delay_left = motor_speed;
        }

        motor_left_status = left_motor(left_motor_steps, delay_left);
        motor_right_status = right_motor(right_motor_steps, delay_right);


      } else {
        Serial.println("Koniec danych do wczytania!");
        dataFile.close();
        fileEnd = true;
      }

    } else {
      Serial.println("Błąd otwarcia pliku!");
      fileEnd = true;
    }
  }
}


int left_motor(int steps, int delay_time){
  if (steps > 0) {
    for (int i = 0; i == steps; i++);
      digitalWrite(dirPiny, LOW);
      digitalWrite(stepPiny, HIGH);
      delayMicroseconds(1000); 
      digitalWrite(stepPiny, LOW);
      delayMicroseconds(1000);
      delay(delay_time); 
  } else {
      for (int i = 0; i == steps; i--);
        digitalWrite(dirPiny, HIGH); 
        digitalWrite(stepPiny, HIGH);
        delayMicroseconds(1000); 
        digitalWrite(stepPiny, LOW);
        delayMicroseconds(1000); 
        delay(delay_time);
  }
  return true;
}


int right_motor(int steps, int delay_time){
  if (steps > 0) {
    for (int i = 0; i == steps; i++);
      digitalWrite(dirPinx, LOW);
      digitalWrite(stepPinx, HIGH);
      delayMicroseconds(1000); 
      digitalWrite(stepPinx, LOW);
      delayMicroseconds(1000); 
      delay(delay_time);
  } else {
      for (int i = 0; i == steps; i--);
        digitalWrite(dirPinx, HIGH); 
        digitalWrite(stepPinx, HIGH);
        delayMicroseconds(1000); 
        digitalWrite(stepPinx, LOW);
        delayMicroseconds(1000); 
        delay(delay_time);
  } 
  return true;
}