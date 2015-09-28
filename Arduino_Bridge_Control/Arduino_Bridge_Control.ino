#include <AccelStepper.h>

#define STEP_PIN 9
#define DIR_PIN 8
#define ENABLE_PIN 7

int steps = 0;
int maxSteps = 250;

boolean isActivated = false;

void setup() {
    Serial.begin( 9600 );
    
    pinMode( DIR_PIN, OUTPUT );     
    pinMode( STEP_PIN, OUTPUT );
    
    digitalWrite( DIR_PIN, LOW );
    digitalWrite( STEP_PIN, LOW );
}

void readSerial () {
    String str = "";

    if( Serial.available() > 0 ) {
        str = Serial.readStringUntil( '\n' );
    }

    if ( str == "on=1" ) {
        isActivated = true;
        Serial.println( "activated" );
    } else if ( str == "on=0" ) {
        isActivated = false;
        Serial.println( "disabled" );
    }
}

void loop() {
    readSerial();
    
    if ( isActivated ) {
        if ( steps > maxSteps ) {
            digitalWrite( DIR_PIN, HIGH ); 
        }

        if ( steps > maxSteps * 2 ) {
            digitalWrite( DIR_PIN, LOW );
            steps = 0;
        }
    
        digitalWrite( STEP_PIN, HIGH );
        delay( 1 );

        digitalWrite( STEP_PIN, LOW );
        delay( 1 );

        steps = steps + 1;   
    }
}
