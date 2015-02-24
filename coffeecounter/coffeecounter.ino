/*
 AKQA is coffee powered. This is the proof
 */

// include the library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
// LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

int countLength = 3;
int coffeeCount = 0;
int soundCount = 0;
char coffeeCountString[3];

const int analogPin = A0;
const int digitalPin = 0; //UNO,Mega pin 2, Leonardo pin 3
volatile int sensorState = -1;
int soundVolume = -1;

const int ledPin =  13;      // the number of the LED pin

// Variables will change:
int ledState = LOW;             // ledState used to set the LED
long previousMillis = 0;        // will store last time LED was updated

// the follow variables is a long because the time, measured in miliseconds,
// will quickly become a bigger number than can be stored in an int.
long interval = 1000;

// void soundTriggered()
// {
//     sensorState = 1; //Sound treshold is broken.
// }

void clearCoffeeCountString()
{
    for (int i = 0; i < countLength; i++)
    {
        coffeeCountString[i] = '\0';
    }
}

void setup()
{
    // setup heartbeat led
    pinMode(ledPin, OUTPUT);

    // set up the LCD's number of columns and rows:
    lcd.begin(16, 2);

    // Print a message to the LCD.
    lcd.setCursor(4, 0);
    lcd.print("cups of java");

    lcd.setCursor(1, 1);
    lcd.print("powering AKQA");

    // 000 cups of java
    // running creative

    Serial.begin(115200);
    // attachInterrupt(digitalPin, soundTriggered, RISING);
}

void loop()
{
    //Read microphone voltage = sound volume
    soundVolume = analogRead(analogPin);
    //Serial.print("Sound volume: ");
    // Serial.println(soundVolume);
    if (sensorState == 1)
    {
        //Serial.println("Sound triggered");
        sensorState = 0; // start waiting for next sound trigger.
    }
    else if (soundVolume > 512)
    {
        // Serial.println("Sound detected");
    }

    unsigned long currentMillis = millis();

    if (currentMillis - previousMillis > interval)
    {
        // save the last time you blinked the LED
        previousMillis = currentMillis;

        // if the LED is off turn it on and vice-versa:
        ledState == !ledState;

        // set the LED with the ledState of the variable:
        digitalWrite(ledPin, ledState);

        clearCoffeeCountString();

        if (soundVolume > 512)
        {
            soundCount ++;
        }
        else
        {
            soundCount = 0;
        }

        if (soundCount == 18)
        {
            coffeeCount++;
        }

        if (soundCount > 18)
        {
            soundCount = 0;
        }

        Serial.print(soundVolume, DEC);
        Serial.print("\t");
        Serial.print(soundCount, DEC);
        Serial.print("\t");
        Serial.println(coffeeCount, DEC);

        // coffeeCount = millis() / 1000;

        sprintf (coffeeCountString, "%03d\0", coffeeCount);

        // set the cursor to column 0, line 0
        // (note: line 1 is the second row, since counting begins with 0):
        lcd.setCursor(0, 0);

        // print the number of seconds since reset:
        lcd.print(coffeeCountString);

        //Serial.println(millis(), DEC);
    }
}
