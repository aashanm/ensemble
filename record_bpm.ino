/*
 * Created by ArduinoGetStarted.com
 *
 * This example code is in the public domain
 *
 * Tutorial page: https://arduinogetstarted.com/tutorials/arduino-light-sensor
 */

#define USE_ARDUINO_INTERRUPTS true    // Set-up low-level interrupts for most acurate BPM math.
#include <PulseSensorPlayground.h>     // Includes the PulseSensorPlayground Library.   

//  Variables
const int PulseWire = 0;       // PulseSensor PURPLE WIRE connected to ANALOG PIN 0
const int LED;          // The on-board Arduino LED, close to PIN 13.
int Threshold = 550;           // Determine which Signal to "count as a beat" and which to ignore.

const int numReadings = 3;
int readings[numReadings];
int index = 0;
int total = 0;
                        
                               
PulseSensorPlayground pulseSensor;

void setup() {
  Serial.begin(9600);

  pulseSensor.analogInput(PulseWire);   
  pulseSensor.blinkOnPulse(LED);       
  pulseSensor.setThreshold(Threshold);

  if (pulseSensor.begin()) {
    //Serial.println("We created a pulseSensor Object !");  //This prints one time at Arduino power-up,  or on Arduino reset.  
  }
}

void loop() {

  int analogValue = analogRead(A1);
  
   if (analogValue < 550) {

    if (pulseSensor.sawStartOfBeat()) {           
      int myBPM = pulseSensor.getBeatsPerMinute();  

      if (myBPM >= 45 && myBPM <= 120) {
        total = total + myBPM;
        readings[index] = myBPM;
        index = index + 1;

        if (numReadings == index){
          int myAverageBPM = total / numReadings;
          if (myAverageBPM >= 45 && myAverageBPM <= 120) {
            Serial.println(myAverageBPM);
          }
          total = 0;
          index = 0;
        }

      }
    }
  } 
}
