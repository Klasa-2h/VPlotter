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
File variant;

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
    return;
  }

  Serial.println("Inicjalizacja powiodła się pomyślnie!");
  variant = SD.open("/");
  if (!variant){
    Serial.println("Nie można otworzyć katalogu głównego!");
    while(1);
  } 

  while (true) {
    dataFile = variant.openNextFile();  

    if (!dataFile) {
      Serial.println("Nie znaleziono plików!");
      while (1); 
    }

    if (!dataFile.isDirectory()) {
      Serial.print("Odczytywanie pliku ");
      Serial.println(dataFile.name());
      break;  
    }
  }

  delay(1000);
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

        if (left_motor_steps == 0 || right_motor_steps == 0 || left_motor_steps == right_motor_steps){
          delay_left = motor_speed;
          delay_right = motor_speed;
        } else {
          if (left_motor_steps > right_motor_steps){
            delay_left = abs(left_motor_steps / right_motor_steps) * motor_speed;
            delay_right = motor_speed;
          } if (right_motor_steps > left_motor_steps){
            delay_right = abs(right_motor_steps / left_motor_steps) * motor_speed;
            delay_left = motor_speed;
          }
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
  if (steps == 0){
    return true;
  }

  if (steps > 0) {
      digitalWrite(dirPiny, LOW);
    for (int i = 0; i < steps; i++){
      digitalWrite(stepPiny, HIGH);
      delayMicroseconds(1000); 
      digitalWrite(stepPiny, LOW);
      delayMicroseconds(1000);
      delay(delay_time); 
    }
  } else {
      digitalWrite(dirPiny, HIGH); 
      for (int i = 0; i < abs(steps); i++){
        digitalWrite(stepPiny, HIGH);
        delayMicroseconds(1000); 
        digitalWrite(stepPiny, LOW);
        delayMicroseconds(1000); 
        delay(delay_time);
      }
  }
  return true;
}


int right_motor(int steps, int delay_time){
  if (steps == 0){
    return true;
  }

  if (steps > 0) {
    digitalWrite(dirPinx, LOW);
    for (int i = 0; i < steps; i++){
      digitalWrite(stepPinx, HIGH);
      delayMicroseconds(1000); 
      digitalWrite(stepPinx, LOW);
      delayMicroseconds(1000); 
      delay(delay_time);
    }
  } else {
      digitalWrite(dirPinx, HIGH); 
      for (int i = 0; i < abs(steps); i++){
        digitalWrite(stepPinx, HIGH);
        delayMicroseconds(1000); 
        digitalWrite(stepPinx, LOW);
        delayMicroseconds(1000); 
        delay(delay_time);
      }
  } 
  return true;
}