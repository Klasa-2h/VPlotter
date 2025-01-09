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
bool step_in_progress = false;

int motor_speed = 5;
int left_motor_steps = 0;
int right_motor_steps = 0;

// Bufor danych
const int buffer_size = 10;
int buffer_left[buffer_size];
int buffer_right[buffer_size];
int buffer_index = 0;  // Na którym elemencie bufora się znajduje
int buffer_count = 0;  // Ile obecnie elementów jest w bufforze

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
  if (!variant) {
    Serial.println("Nie można otworzyć katalogu głównego!");
    digitalWrite(enablePin, HIGH);
    while (1);
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

  fill_buffer();
  delay(1000);
}

void loop() {
  // Zakończ program, gdy wszystkie dane zostaną przetworzone
  if (fileEnd && buffer_index >= buffer_count) {
    return;
  }

  // Sprawdź, czy są dane do przetworzenia w buforze
  if (buffer_index < buffer_count) {
    if (!step_in_progress) {
      left_motor_steps = buffer_left[buffer_index];
      right_motor_steps = buffer_right[buffer_index];
      buffer_index++;  // Przejdź do kolejnych danych w buforze
      step_in_progress = true;
    }
  } else if (dataFile.available()) {
    // Wczytaj kolejne dane do bufora
    fill_buffer();
  }

  // Ruch silników
  if (step_in_progress) {
    step_in_progress = execute_steps(left_motor_steps, right_motor_steps, motor_speed);
  }

  // Zamknij plik, jeśli odczytano wszystkie dane
  if (!dataFile.available() && buffer_index >= buffer_count) {
    Serial.println("Koniec danych do wczytania!");
    digitalWrite(enablePin, HIGH);
    dataFile.close();
    fileEnd = true;
  }
}

bool execute_steps(int &left_steps, int &right_steps, int &time) {
  int left_direction = LOW;
  int right_direction = LOW;

  if (left_steps < 0) {
    left_direction = HIGH;
  } if (right_steps < 0) {
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

  return false;
}

void fill_buffer() {
  buffer_index = 0;
  buffer_count = 0;

  while (buffer_count < buffer_size && dataFile.available()) {
    String line = dataFile.readStringUntil('\n');
    sscanf(line.c_str(), "%d %d", &buffer_left[buffer_count], &buffer_right[buffer_count]);
    buffer_count++;
  }

  if (buffer_count == 0 && !dataFile.available()) {
    fileEnd = true;
  }
}