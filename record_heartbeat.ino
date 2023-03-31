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
                               // Use the "Gettting Started Project" to fine-tune Threshold Value beyond default setting.
                               // Otherwise leave the default "550" value. 
const int numReadings = 3;
int readings[numReadings];
int index = 0;
int total = 0;
                        
                               
PulseSensorPlayground pulseSensor;  // Creates an instance of the PulseSensorPlayground object called "pulseSensor"

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);

  // Configure the PulseSensor object, by assigning our variables to it. 
  pulseSensor.analogInput(PulseWire);   
  pulseSensor.blinkOnPulse(LED);       //auto-magically blink Arduino's LED with heartbeat.
  pulseSensor.setThreshold(Threshold);

  //Double-check the "pulseSensor" object was created and "began" seeing a signal. 
  if (pulseSensor.begin()) {
    //Serial.println("We created a pulseSensor Object !");  //This prints one time at Arduino power-up,  or on Arduino reset.  
  }
}

void loop() {

  // reads the input on analog pin A1 (value between 0 and 1023)
  int analogValue = analogRead(A1);

  // Serial.println("Analog reading: ");
  // Serial.println(analogValue);   // the raw analog reading
  
  // 300 may need to be altered
   if (analogValue < 550) {
    //Serial.println(" Dark - place finger on sensor");

    if (pulseSensor.sawStartOfBeat()) {            // Constantly test to see if "a beat happened".
      int myBPM = pulseSensor.getBeatsPerMinute();  // Calls function on our pulseSensor object that returns BPM as an "int".
                                                // "myBPM" hold this BPM value now. 
      //Serial.println("♥  A HeartBeat Happened ! "); // If test is "true", print a message "a heartbeat happened".
      //Serial.print("BPM: ");                        // Print phrase "BPM: " 
      //Serial.println(myBPM);                        // Print the value inside of myBPM. 

      if (myBPM >= 45 && myBPM <= 120) {
        Serial.println(myBPM);
        Serial.println(total);
        Serial.println(index);
        total = total + myBPM;
        readings[index] = myBPM;
        index = index + 1;
        // Serial.print("index: ");
        // Serial.println(index);

        if (numReadings == index){
          int myAverageBPM = total / numReadings;
          // Serial.print("average: ");
          Serial.println(myAverageBPM);
          total = 0;
          index = 0;
        }

      }
    }
  } 
}
