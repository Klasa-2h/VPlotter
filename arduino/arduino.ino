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
bool motor_right_status = true;
bool motor_left_status = true;
int motor_speed = 125;

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

  delay(2000);
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
            if (abs(left_motor_steps) > abs(right_motor_steps)){
              delay_left = calculate_delay(left_motor_steps, right_motor_steps, motor_speed, true);
              delay_right = motor_speed;             
            } if (abs(right_motor_steps) > abs(left_motor_steps)){
              delay_right = calculate_delay(left_motor_steps, right_motor_steps, motor_speed, false);
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


int calculate_delay(float stepsL, float stepsR, int basic_speed_value, bool bigger_left){
  float delay_value = 0;
  stepsL = abs(stepsL);
  stepsR = abs(stepsR);

  if (bigger_left == true){
    delay_value = (stepsL / stepsR) * basic_speed_value;
  } else {
    delay_value = (stepsR / stepsL) * basic_speed_value;
  }
  return delay_value;
}


int left_motor(int steps, int delay_time){
  if (steps == 0){
    return true;
  }

  if (steps > 0) {
      digitalWrite(dirPiny, LOW);
    for (int i = 0; i <= steps; i++){
      digitalWrite(stepPiny, HIGH);
      delayMicroseconds(1000); 
      digitalWrite(stepPiny, LOW);
      delayMicroseconds(1000);
      delay(delay_time); 
    }
  } else {
      digitalWrite(dirPiny, HIGH); 
      for (int i = 0; i <= abs(steps); i++){
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
    for (int i = 0; i <= steps; i++){
      digitalWrite(stepPinx, HIGH);
      delayMicroseconds(1000); 
      digitalWrite(stepPinx, LOW);
      delayMicroseconds(1000); 
      delay(delay_time);
    }
  } else {
      digitalWrite(dirPinx, HIGH); 
      for (int i = 0; i <= abs(steps); i++){
        digitalWrite(stepPinx, HIGH);
        delayMicroseconds(1000); 
        digitalWrite(stepPinx, LOW);
        delayMicroseconds(1000); 
        delay(delay_time);
      }
  } 
  return true;
}