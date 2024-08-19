#include <Wire.h>
#include <Adafruit_SGP30.h>

const int flameDigitalPin = 2; // Digital output pin
const int flameAnalogPin = A0; // Analog output pin
const int ledPin = 13;         // Built-in LED pin

// Define thresholds for harmful levels
const int tvocThreshold = 1000;   // TVOC threshold (ppb)
const int co2Threshold = 10000;   // eCO2 threshold (ppm)

Adafruit_SGP30 sgp;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Set the digital pin as input
  pinMode(flameDigitalPin, INPUT);
  
  // Set the built-in LED pin as output
  pinMode(ledPin, OUTPUT);

  // Initialize SGP30 sensor
  if (!sgp.begin()) {
    Serial.println("Sensor not found :(");
    while (1);  // Stop execution if sensor is not found
  }

  Serial.println("Found SGP30 sensor");

  // Initialize SGP30 baseline measurement
  sgp.IAQinit();
}

void loop() {
  // Read the digital output of the flame sensor
  int flameDigitalValue = digitalRead(flameDigitalPin);
  
  // Read the analog output of the flame sensor
  int flameAnalogValue = analogRead(flameAnalogPin);

  // Read SGP30 sensor values
  if (!sgp.IAQmeasure()) {
    Serial.println("Measurement failed");
    return;
  }

  // Print the SGP30 sensor values to the Serial Monitor
  Serial.print("TVOC: ");
  Serial.print(sgp.TVOC);
  Serial.print(" ppb\tCO2: ");
  Serial.print(sgp.eCO2);
  Serial.println(" ppm");

  // Check for harmful levels
  bool isHarmful = (sgp.TVOC >= tvocThreshold) || (sgp.eCO2 >= co2Threshold);

  // Check flame detection
  if (flameDigitalValue == LOW) {
    Serial.println("Flame detected!");
  } else {
    Serial.println("No flame detected.");
  }

  // Determine emergency status
  if (flameDigitalValue == LOW || isHarmful) {
    Serial.println("Emergency");
    digitalWrite(ledPin, HIGH);  // Turn LED on if emergency
    while (1);  // Stop execution if emergency detected
  } else {
    Serial.println("No emergency");
    digitalWrite(ledPin, LOW);   // Turn LED off if no emergency
  }

  // Delay for a short while to observe the readings
  delay(3000);
}
