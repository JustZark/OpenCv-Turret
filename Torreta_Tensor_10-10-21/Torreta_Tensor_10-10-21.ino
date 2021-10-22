#include <Servo.h>
#include <pt.h>

struct pt hilo1;
struct pt hilo2;

Servo S1;
Servo S2;
Servo S3;

int comUx ,comUy ,comx=0, comy=0, value_x, value_y, value_y_2;

const byte numChars = 32;
char receivedChars[numChars];
boolean newData = false, start_a = false, detected = false,ended = false;
int integerFromPC = 0;

void setup() {
  PT_INIT(&hilo1);
  PT_INIT(&hilo2);

  Serial.begin(9600);
  S1.attach(3);
  S2.attach(4);
  S3.attach(5);
  S1.write(72);
  S2.write(100);
  S3.write(50);
  delay(2000);
}

// --------------------------------------------------------------------------------
void recvWithEndMarker() {
 char * strtokIndx;
 static byte ndx = 0;
 char endMarker = '\n';
 char rc;
 
 while (Serial.available() > 0 && newData == false) {
  rc = Serial.read(); 
  if (rc != endMarker) {
   receivedChars[ndx] = rc;
   ndx++;
  if (ndx >= numChars) {
   ndx = numChars - 1;
  }
  }
  else {
   receivedChars[ndx] = '\0'; 
   ndx = 0;
   newData = true;
   ended = true;
  }
 }
}
// --------------------------------------------------------------------------------------
void Parse() {
 char * strtokIndx;
 if (receivedChars != NULL && ended == true) {
  strtokIndx = strtok(receivedChars,",");      
  comx = atoi(strtokIndx);  
  strtokIndx = strtok(NULL, ",");
  comy = atoi(strtokIndx);   
  ended = false;
 } 
}
// --------------------------------------------------------------------------------------
void movimiento_x(struct pt *pt){
 PT_BEGIN(pt);
 static long t = 0;
 t = millis();  
 if(comx != comUx){     
  comUx = comx;
  value_x = map(comx,0,640,30,110);
  S1.write(value_x);
  PT_WAIT_UNTIL(pt, (millis()-t)>10);   
 }
 PT_END(pt);
}
// -------------------------------------------------------------------------------
void movimiento_y(struct pt *pt){
 PT_BEGIN(pt); 
 static long t = 0;
 t = millis();
 if(comy != comUy){ 
  comUy = comy;
  value_y = map(comy,0,480,30,120); // map(val, min_dat, max_dat, max_arriba, max_abajo)
  value_y_2 = map(comy,0,480,120,30);
  S2.write(value_y);
  S3.write(value_y_2);
  PT_WAIT_UNTIL(pt, (millis()-t)>10);
 }  
 PT_END(pt); 
}
// ---------------------------------------------------------------------------------------
void loop() {
  recvWithEndMarker();
  Parse();

  movimiento_x(&hilo1);
  movimiento_y(&hilo2);
   
  newData = false;
}
