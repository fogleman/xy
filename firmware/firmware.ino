#include <EEPROM.h>
#include <Servo.h>
#include <SoftwareSerial.h>
#include <Wire.h>

// data stored in eeprom
static union{
    struct{
      char name[8];
      unsigned char motoADir;
      unsigned char motoBDir;
      unsigned char motorSwitch;
      int height;
      int width;
      int speed;
      int penUpPos;
      int penDownPos;
    }data;
    char buf[64];
}roboSetup;

float curX,curY,curZ;
float tarX,tarY,tarZ; // target xyz position
int tarA,tarB,posA,posB; // target stepper position
int8_t motorAfw,motorAbk;
int8_t motorBfw,motorBbk;

int ylimit_pin1 = 12;
int ylimit_pin2 = 13;
int xlimit_pin1 = A2;
int xlimit_pin2 = A3;
int servopin = A1;
Servo servoPen;

/************** motor movements ******************/
void stepperMoveA(int dir)
{
  if(dir>0){
    digitalWrite(11, LOW);
  }else{
    digitalWrite(11, HIGH);
  }
  digitalWrite(10, HIGH);
  digitalWrite(10, LOW);
}

void stepperMoveB(int dir)
{
  if(dir>0){
    digitalWrite(3, LOW);
  }else{
    digitalWrite(3, HIGH);
  }
  digitalWrite(9, HIGH);
  digitalWrite(9, LOW);
}

/************** calculate movements ******************/
int stepAuxDelay=0;
int stepdelay_min=200;
int stepdelay_max=2000;
#define SPEED_STEP 1

void doMove()
{
  int mDelay=stepdelay_max;
  int speedDiff = -SPEED_STEP;
  int dA,dB,maxD;
  float stepA,stepB,cntA=0,cntB=0;
  int d;
  dA = tarA - posA;
  dB = tarB - posB;
  maxD = max(abs(dA),abs(dB));
  stepA = (float)abs(dA)/(float)maxD;
  stepB = (float)abs(dB)/(float)maxD;
  for(int i=0;(posA!=tarA)||(posB!=tarB);i++){
    // move A
    if(posA!=tarA){
      cntA+=stepA;
      if(cntA>=1){
        d = dA>0?motorAfw:motorAbk;
        posA+=(dA>0?1:-1);
        stepperMoveA(d);
        cntA-=1;
      }
    }
    // move B
    if(posB!=tarB){
      cntB+=stepB;
      if(cntB>=1){
        d = dB>0?motorBfw:motorBbk;
        posB+=(dB>0?1:-1);
        stepperMoveB(d);
        cntB-=1;
      }
    }
    mDelay=constrain(mDelay+speedDiff,stepdelay_min,stepdelay_max)+stepAuxDelay;
    delayMicroseconds(mDelay);
    if((maxD-i)<((stepdelay_max-stepdelay_min)/SPEED_STEP)){
      speedDiff=SPEED_STEP;
    }
  }
  posA = tarA;
  posB = tarB;
}

/******** mapping xy position to steps ******/
#define WIDTH 380
#define HEIGHT 310
#define STEPS_PER_MM 87.58 // the same as 3d printer
void prepareMove()
{
  float dx = tarX - curX;
  float dy = tarY - curY;
  float distance = sqrt(dx*dx+dy*dy);
  if (distance < 0.001)
    return;
  tarA = tarX*STEPS_PER_MM;
  tarB = tarY*STEPS_PER_MM;
  doMove();
  curX = tarX;
  curY = tarY;
}

void goHome()
{
  // stop on either endstop touches
  while(digitalRead(xlimit_pin2)==1 && digitalRead(xlimit_pin1)==1){
    stepperMoveA(motorAbk);
    delayMicroseconds(stepdelay_min);
  }
  while(digitalRead(ylimit_pin2)==1 && digitalRead(ylimit_pin1)==1){
    stepperMoveB(motorBbk);
    delayMicroseconds(stepdelay_min);
  }
  posA = 0;
  posB = 0;
  curX = 0;
  curY = 0;
}

void initPosition()
{
  curX=0; curY=0;
  posA = 0;posB = 0;
}

/************** calculate movements ******************/
void parseCoordinate(char * cmd)
{
  char * tmp;
  char * str;
  str = strtok_r(cmd, " ", &tmp);
  tarX = curX;
  tarY = curY;
  while(str!=NULL){
    str = strtok_r(0, " ", &tmp);
    if(str[0]=='X'){
      tarX = atof(str+1);
    }else if(str[0]=='Y'){
      tarY = atof(str+1);
    }else if(str[0]=='Z'){
      tarZ = atof(str+1);
    }else if(str[0]=='A'){
      stepAuxDelay = atoi(str+1);
    }
  }
  prepareMove();
}

void echoRobotSetup()
{
  Serial.print("M10 XY ");
  Serial.print(roboSetup.data.width);Serial.print(' ');
  Serial.print(roboSetup.data.height);Serial.print(' ');
  Serial.print(curX);Serial.print(' ');
  Serial.print(curY);Serial.print(' ');
  Serial.print("A");Serial.print((int)roboSetup.data.motoADir);
  Serial.print(" B");Serial.print((int)roboSetup.data.motoBDir);
  Serial.print(" H");Serial.print((int)roboSetup.data.motorSwitch);
  Serial.print(" S");Serial.print((int)roboSetup.data.speed);
  Serial.print(" U");Serial.print((int)roboSetup.data.penUpPos);
  Serial.print(" D");Serial.println((int)roboSetup.data.penDownPos);
}

void echoEndStop()
{
  Serial.print("M11 ");
  Serial.print(digitalRead(xlimit_pin1)); Serial.print(" ");
  Serial.print(digitalRead(xlimit_pin2)); Serial.print(" ");
  Serial.print(digitalRead(ylimit_pin1)); Serial.print(" ");
  Serial.println(digitalRead(ylimit_pin2));
}

void syncRobotSetup()
{
  int i;
  for(i=0;i<64;i++){
    EEPROM.write(i,roboSetup.buf[i]);
  }
}

void parseRobotSetup(char * cmd)
{
  char * tmp;
  char * str;
  str = strtok_r(cmd, " ", &tmp);
  while(str!=NULL){
    str = strtok_r(0, " ", &tmp);
    if(str[0]=='A'){
      roboSetup.data.motoADir = atoi(str+1);
    }else if(str[0]=='B'){
      roboSetup.data.motoBDir = atoi(str+1);
    }else if(str[0]=='H'){
      roboSetup.data.height = atoi(str+1);
    }else if(str[0]=='W'){
      roboSetup.data.width = atoi(str+1);
    }else if(str[0]=='S'){
      roboSetup.data.speed = atoi(str+1);
    }
  }
  syncRobotSetup();
}

void parseAuxDelay(char * cmd)
{
  char * tmp;
  strtok_r(cmd, " ", &tmp);
  stepAuxDelay = atoi(tmp);
}

void parsePen(char * cmd)
{
  char * tmp;
  strtok_r(cmd, " ", &tmp);
  int pos = atoi(tmp);
  servoPen.write(pos);
}

void parsePenPosSetup(char * cmd)
{
  char * tmp;
  char * str;
  str = strtok_r(cmd, " ", &tmp);
  while(str!=NULL){
    str = strtok_r(0, " ", &tmp);
    if(str[0]=='U'){
      roboSetup.data.penUpPos = atoi(str+1);
    }else if(str[0]=='D'){
      roboSetup.data.penDownPos = atoi(str+1);    
    }
  }
  syncRobotSetup();
}

void parseMcode(char * cmd)
{
  int code;
  code = atoi(cmd);
  switch(code){
    case 1:
      parsePen(cmd);
      break;
    case 2:
      parsePenPosSetup(cmd);
      break;
    case 3:
      parseAuxDelay(cmd);
      break;
    case 5:
      parseRobotSetup(cmd);
      break;      
    case 10:
      echoRobotSetup();
      break;
    case 11:
      echoEndStop();
      break;
  }
}

void parseGcode(char * cmd)
{
  int code;
  code = atoi(cmd);
  switch(code){
    case 0:
    case 1:
      parseCoordinate(cmd);
      break;
    case 28:
      tarX=0; tarY=0;
      goHome();
      break; 
  }
}

void parseCmd(char * cmd)
{
  if(cmd[0]=='G'){
    parseGcode(cmd+1);  
  }else if(cmd[0]=='M'){
    parseMcode(cmd+1);
  }else if(cmd[0]=='P'){
    Serial.print("POS X");Serial.print(curX);Serial.print(" Y");Serial.println(curY);
  }
  Serial.println("OK");
}

// local data
void initRobotSetup()
{
  int i;
  for(i=0;i<64;i++){
    roboSetup.buf[i] = EEPROM.read(i);
  }
  if(strncmp(roboSetup.data.name,"XY4",3)!=0){
    Serial.println("set to default setup");
    // set to default setup
    memset(roboSetup.buf,0,64);
    memcpy(roboSetup.data.name,"XY4",3);
    roboSetup.data.motoADir = 0;
    roboSetup.data.motoBDir = 0;
    roboSetup.data.width = WIDTH;
    roboSetup.data.height = HEIGHT;
    roboSetup.data.motorSwitch = 0;
    roboSetup.data.speed = 80;
    roboSetup.data.penUpPos = 160;
    roboSetup.data.penDownPos = 90;
    syncRobotSetup();
  }
  // init motor direction
  // yzj, match to standard connection of xy
  // A = x, B = y
  if(roboSetup.data.motoADir==0){
    motorAfw=-1;motorAbk=1;
  }else{
    motorAfw=1;motorAbk=-1;
  }
  if(roboSetup.data.motoBDir==0){
    motorBfw=-1;motorBbk=1;
  }else{
    motorBfw=1;motorBbk=-1;
  }
  int spd = 100 - roboSetup.data.speed;
//  stepdelay_min = spd*10;
//  stepdelay_max = spd*100;
}


/************** arduino ******************/
void setup() {
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(ylimit_pin1,INPUT_PULLUP);
  pinMode(ylimit_pin2,INPUT_PULLUP);
  pinMode(xlimit_pin1,INPUT_PULLUP);
  pinMode(xlimit_pin2,INPUT_PULLUP);
  Serial.begin(115200);
  initRobotSetup();
  initPosition();
  servoPen.attach(servopin);
  delay(100);
  servoPen.write(roboSetup.data.penUpPos);
}

char buf[64];
int8_t bufindex;

void loop() {
  if(Serial.available()){
    char c = Serial.read();
    buf[bufindex++]=c; 
    if(c=='\n'){
      buf[bufindex]='\0';
      parseCmd(buf);
      memset(buf,0,64);
      bufindex = 0;
    }
    if(bufindex>=64){
      bufindex=0;
    }
  }
}
