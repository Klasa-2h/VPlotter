#include <Servo.h>
#include <SPI.h>
#include <SD.h>

#define stepPinx 2
#define dirPinx 5
#define stepPiny 3
#define dirPiny 6

#define enablePin 8
#define pinSD 10
#define servoPin 9 

#define stepsPerRevolution 200  

Servo myServo;

File dataFile;

const int delayTime = 100; 
unsigned long lastReadTime = 0;
bool fileEnd = false;

void setup() {
  Serial.begin(9600);

  pinMode(enablePin, OUTPUT);

  pinMode(stepPinx, OUTPUT);
  pinMode(dirPinx, OUTPUT);
  pinMode(stepPiny, OUTPUT);
  pinMode(dirPiny, OUTPUT);

  digitalWrite(enablePin, LOW);

  myServo.attach(servoPin);
  myServo.write(0);

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

  if (millis() - lastReadTime >= delayTime) {
    lastReadTime = millis();

    if (dataFile) {
      if (dataFile.available()) {
        String step = dataFile.readStringUntil('\n');
        step.trim();
        Serial.println(step);

        if (step == "10") {
          digitalWrite(dirPinx, LOW);
          digitalWrite(stepPinx, HIGH);
          delayMicroseconds(1000); 
          digitalWrite(stepPinx, LOW);
          delayMicroseconds(1000); 
        } else if (step == "11") {
          digitalWrite(dirPinx, HIGH); 
          digitalWrite(stepPinx, HIGH);
          delayMicroseconds(1000); 
          digitalWrite(stepPinx, LOW);
          delayMicroseconds(1000); 
        } else if (step == "01") {
          digitalWrite(dirPiny, LOW);
          digitalWrite(stepPiny, HIGH);
          delayMicroseconds(1000); 
          digitalWrite(stepPiny, LOW);
          delayMicroseconds(1000); 
        } else if (step == "00") {
          digitalWrite(dirPiny, HIGH); 
          digitalWrite(stepPiny, HIGH);
          delayMicroseconds(1000); 
          digitalWrite(stepPiny, LOW);
          delayMicroseconds(1000); 
        } else if (step == "1") {
          myServo.write(90);
        } else if (step == "0") {
          myServo.write(0);
        } else {
          Serial.println("Nieznana komenda");
        }
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
