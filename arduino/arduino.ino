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
int motor_speed = 10;
int left_motor_steps = 0;
int right_motor_steps = 0;

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
    digitalWrite(enablePin, HIGH);
    return;
  }

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
      while (1); 
    }

    if (!dataFile.isDirectory()) {
      Serial.print("Odczytywanie pliku ");
      Serial.println(dataFile.name());
      break;  
    }
  }

  delay(1200);
}

void loop() {
  if (fileEnd) {
    return;
  }

  if (dataFile.available()) {
    String couple = dataFile.readStringUntil('\n');
    sscanf(couple.c_str(), "%d %d", &left_motor_steps, &right_motor_steps);

    Serial.println(left_motor_steps);
    Serial.println(right_motor_steps);
  } else {
    Serial.println("Koniec danych do wczytania!");
    digitalWrite(enablePin, HIGH);
    dataFile.close();
    fileEnd = true;
  }

  execute_steps(left_motor_steps, right_motor_steps, motor_speed);
}

void execute_steps(int &left_steps, int &right_steps, int &time) {
  int left_direction = LOW;
  int right_direction = LOW;

  if (left_steps < 0) {
    left_direction = HIGH;
  } if (right_steps > 0) {
    right_direction = HIGH;
  }

  left_steps = abs(left_steps);
  right_steps = abs(right_steps);

  if (left_steps > 0) {
    digitalWrite(dirPinx, left_direction);
    digitalWrite(stepPinx, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPinx, LOW);
    delayMicroseconds(1000);
    delay(time);
    left_steps--;
  }

  if (right_steps > 0) {
    digitalWrite(dirPiny, right_direction);
    digitalWrite(stepPiny, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPiny, LOW);
    delayMicroseconds(1000);
    delay(time);
    right_steps--;
  }
}