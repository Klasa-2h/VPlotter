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
bool marker_right = true;
bool marker_left = true;

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

  if (marker_right == true && marker_left == true) {
    marker_right = false;
    marker_left = false;

    if (dataFile) {
      if (dataFile.available()) {
        int left_motor = 0;
        int right_motor = 0;
        String couple = dataFile.readStringUntil('\n');

        sscanf(couple.c_str(), "%d %d", &left_motor, &right_motor);

        Serial.println(left_motor);
        Serial.println(right_motor);

        if (right_motor > 0) {
          for (int i = 0; i == right_motor; i++);
            digitalWrite(dirPinx, LOW);
            digitalWrite(stepPinx, HIGH);
            delayMicroseconds(1000); 
            digitalWrite(stepPinx, LOW);
            delayMicroseconds(1000); 
        } else {
            for (int i = 0; i == right_motor; i--);
              digitalWrite(dirPinx, HIGH); 
              digitalWrite(stepPinx, HIGH);
              delayMicroseconds(1000); 
              digitalWrite(stepPinx, LOW);
              delayMicroseconds(1000); 
        } 
        marker_right = true;

        if (left_motor > 0) {
          for (int i = 0; i == left_motor; i++);
            digitalWrite(dirPiny, LOW);
            digitalWrite(stepPiny, HIGH);
            delayMicroseconds(1000); 
            digitalWrite(stepPiny, LOW);
            delayMicroseconds(1000); 
        } else {
            for (int i = 0; i == left_motor; i--);
              digitalWrite(dirPiny, HIGH); 
              digitalWrite(stepPiny, HIGH);
              delayMicroseconds(1000); 
              digitalWrite(stepPiny, LOW);
              delayMicroseconds(1000); 
        }
        marker_left = true;

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
