#include <Wire.h>
#include <Adafruit_SGP30.h>

const int flameDigitalPin = 2; // Digital output pin
const int flameAnalogPin = A0; // Analog output pin
const int ledPin = 13;         // Built-in LED pin

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
    while (1);
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
  
  // Print the flame sensor values to the Serial Monitor
  Serial.print("Flame Digital Output: ");
  Serial.print(flameDigitalValue);
  Serial.print("\tFlame Analog Output: ");
  Serial.println(flameAnalogValue);

  // Turn the LED on or off based on the digital output of the flame sensor
  if (flameDigitalValue == LOW) {
    Serial.println("Flame detected!");
    digitalWrite(ledPin, HIGH);  // Turn LED on if flame detected
  } else {
    Serial.println("No flame detected.");
    digitalWrite(ledPin, LOW);   // Turn LED off if no flame detected
  }

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

  // Delay for a short while to observe the readings
  delay(2000);
}


