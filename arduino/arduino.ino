#include <SPI.h>
#include <SD.h>

#define stepPinx 2
#define dirPinx 5
#define stepPiny 3
#define dirPiny 6

#define enablePin 8
#define pinSD 10

File dataFile;
File variant;

bool fileEnd = false;
int motor_speed = 65;

void setup() {
  Serial.begin(9600);

  pinMode(enablePin, OUTPUT);
  digitalWrite(enablePin, LOW);

  pinMode(stepPinx, OUTPUT);
  pinMode(dirPinx, OUTPUT);
  pinMode(stepPiny, OUTPUT);
  pinMode(dirPiny, OUTPUT);

  Serial.println("Inicjalizacja karty SD...");
  if (!SD.begin(pinSD)) {
    Serial.println("Błąd inicjalizacji karty SD!");
    return;
  }

  Serial.println("Inicjalizacja powiodła się pomyślnie!");
  variant = SD.open("/");
  if (!variant){
    Serial.println("Nie można otworzyć katalogu głównego!");
    digitalWrite(enablePin, HIGH);
    while(1);
  } 

  while (true) {
    dataFile = variant.openNextFile();  

    if (!dataFile) {
      Serial.println("Nie znaleziono plików!");
      digitalWrite(enablePin, HIGH);
      while(1); 
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

  if (dataFile) {
    if (dataFile.available()) {
      int left_motor_steps = 0;
      int right_motor_steps = 0;
      String couple = dataFile.readStringUntil('\n');

      sscanf(couple.c_str(), "%d %d", &left_motor_steps, &right_motor_steps);

      Serial.println(left_motor_steps);
      Serial.println(right_motor_steps);

      left_motor(left_motor_steps, motor_speed);
      right_motor(right_motor_steps, motor_speed);

    } else {
      Serial.println("Koniec danych do wczytania!");
      dataFile.close();
      digitalWrite(enablePin, HIGH);
      fileEnd = true;
    }

  } else {
    Serial.println("Błąd otwarcia pliku!");
    digitalWrite(enablePin, HIGH);
    fileEnd = true;
  }
}


int left_motor(int steps, int delay_time){
  if (steps == 0){
    return true;
  }

  if (steps > 0) {
    digitalWrite(dirPinx, LOW);
    digitalWrite(stepPinx, HIGH);
    delayMicroseconds(1000); 
    digitalWrite(stepPinx, LOW);
    delayMicroseconds(1000);
    delay(delay_time); 
  } else {
      digitalWrite(dirPinx, HIGH); 
      digitalWrite(stepPinx, HIGH);
      delayMicroseconds(1000); 
      digitalWrite(stepPinx, LOW);
      delayMicroseconds(1000); 
      delay(delay_time);
  }
  return true;
}


int right_motor(int steps, int delay_time){
  if (steps == 0){
    return true;
  }

  if (steps > 0) {
    digitalWrite(dirPiny, HIGH);
    digitalWrite(stepPiny, HIGH);
    delayMicroseconds(1000); 
    digitalWrite(stepPiny, LOW);
    delayMicroseconds(1000); 
    delay(delay_time);
  } else {
      digitalWrite(dirPiny, LOW); 
      digitalWrite(stepPiny, HIGH);
      delayMicroseconds(1000); 
      digitalWrite(stepPiny, LOW);
      delayMicroseconds(1000); 
      delay(delay_time);
  } 
  return true;
}