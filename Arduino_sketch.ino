#include <Servo.h>

int statusLed = 22;
int arrowRightLed = 24;
int arrowUpLed = 26;
int arrowLeftLed = 28;
int arrowDownLed = 30;
int circleLed = 29;
int xLed = 31;
int squareLed = 33;
int triangleLed = 35;
int pos = 0;
int commands;
bool toggle = false;

//finish building and implement command rejected LED 

int ledArray[9]={statusLed,arrowRightLed,arrowUpLed,arrowLeftLed,arrowDownLed,circleLed,xLed,squareLed,triangleLed};
Servo lB;     //Left-bottom servo
Servo lT;     //Left-top servo
Servo rT;     //Right-top servo
Servo rB;     //Right-bottom servo
Servo servoArray[4] = {lB,lT,rT,rB};

void setup() {
 rT.attach(4);
 rB.attach(5);
 lB.attach(3);
 lT.attach(6);
 pinMode(statusLed, OUTPUT);
 pinMode(arrowRightLed, OUTPUT);
 pinMode(arrowUpLed, OUTPUT);
 pinMode(arrowLeftLed, OUTPUT);
 pinMode(arrowDownLed, OUTPUT);
 pinMode(circleLed, OUTPUT);
 pinMode(xLed, OUTPUT);
 pinMode(squareLed, OUTPUT);
 pinMode(triangleLed, OUTPUT);
 pinMode(LED_BUILTIN, OUTPUT);

 Serial.begin(9600);
// bootUp();

  }

void loop() {
 commands = Serial.read();

//
   if(commands == '8') {
    toggle = true;}


   if (commands == '9') {
    toggle = false;
    servoReset(lT);
    servoReset(lB);
   }

  if (toggle == true) {
    if(commands == '2'){
      turnOnLed(statusLed);
      turnOnLed(arrowUpLed);
      toggleLeft(lT);
      }
  
    else if(commands == '1'){
      turnOnLed(statusLed);
      turnOnLed(arrowRightLed);
      toggleRight(lT);
      }
  
    else if(commands == '0'){
      turnOnLed(statusLed);
      turnOnLed(arrowLeftLed);
      toggleLeft(lB);
      }
  
    else if(commands == '3'){
      turnOnLed(statusLed);
      turnOnLed(arrowDownLed);
      toggleRight(lB);
      }
    } else {
      
      if(commands == '1'){
      turnOnLed(statusLed);
      turnOnLed(arrowUpLed);
      servoMoveRight(lT);
    }
  
    else if(commands == '2'){
      turnOnLed(statusLed);
      turnOnLed(arrowRightLed);
      servoMoveLeft(lT);
    }
  
    else if(commands == '0'){
      turnOnLed(statusLed);
      turnOnLed(arrowLeftLed);
      servoMoveLeft(lB);
    }
  
    else if(commands == '3'){
      turnOnLed(statusLed);
      turnOnLed(arrowDownLed);
      servoMoveRight(lB);
    }
  }
  if(commands == '4'){
  //Square icon
    turnOnLed(statusLed);
    turnOnLed(triangleLed);
    servoMoveRight(rT);
  }

  else if(commands == '5'){
    //Triangle icon
    turnOnLed(statusLed);
    turnOnLed(squareLed);
    servoMoveLeft(rT);
  }

  else if(commands == '7'){
    //Cross icon
    turnOnLed(statusLed);
    turnOnLed(xLed);
    servoMoveLeft(rB);
  }

  else if(commands == '6'){
//Round icon
    turnOnLed(statusLed);
    turnOnLed(circleLed);
    servoMoveRight(rB);
  }
  Serial.println(toggle);
}

void bootUp(){                                // A "boot-up" sequence for the LED's and servos
  for(int i = 0; i <= sizeof(ledArray); i++){   
    digitalWrite(ledArray[i], HIGH);   
      delay(100);                       
    digitalWrite(ledArray[i], LOW);
     delay(100);

for(int i = 0; i <= sizeof(servoArray); i++){
    servosWarmUp(servoArray[i]);
    delay(1000);   
          }
      }
  }

void turnOnLed(int led){          //Turns on a specific LED         
    digitalWrite(led, HIGH);   
      delay(100);                       
    digitalWrite(led, LOW);
    // delay(1000);
      
  }

void servoTest(Servo s){
  for (pos = 0; pos <= 90; pos += 1) {
    s.write(pos);             
    delay(15);                       
    }
  for (pos = 90; pos >= 0; pos -= 1) { 
    s.write(pos);           
    delay(15);                    
    }
  }

void servoReset(Servo s){       //Resets the servo to the initial position
    s.write(90);
  }
 
void servosWarmUp(Servo s) {    //Moves one servo at a time to make sure they work
  servoTest(s);
  servoReset(s);
  delay(2000);
  }  

void servoMoveLeft(Servo s){
  s.write(45);
  delay(300);
  servoReset(s);
  }

void toggleLeft(Servo s){
  s.write(45);
  }

void toggleRight(Servo s){
  s.write(135);
  }
    
void servoMoveRight(Servo s){
  s.write(135);
  delay(300);
  servoReset(s);
  }
  
