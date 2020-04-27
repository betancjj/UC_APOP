
float currStepYaw = 0.0;
float currStepPitch = 0.0;
float desiredStepYaw = 0.0;
float desiredStepPitch = 0.0;

const int stepPinYaw = 8; 
const int dirPinYaw = 9; 
const int stepPinPitch = 5; 
const int dirPinPitch = 6; 

int yawDelay = 0;
int pitchDelay = 0;

void setup() {
  // nothing to do
  Serial.begin(9600);
  // Sets the two pins as Outputs
  pinMode(stepPinYaw,OUTPUT); 
  pinMode(dirPinYaw,OUTPUT);
  pinMode(stepPinPitch,OUTPUT); 
  pinMode(dirPinPitch,OUTPUT);
}

void loop() {
  char buffer[] = {' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',}; // Receive up to 7 bytes
  if (Serial.available() > 0) {
    // read the incoming byte:
    Serial.readBytesUntil('\n',buffer,20);

    char * strtokIndx; // this is used by strtok() as an index
  
    strtokIndx = strtok(buffer,",");      // get the first part - the string
    desiredStepYaw = atof(strtokIndx); // copy it to desiredAngleYaw
    
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    desiredStepPitch = atof(strtokIndx);     // convert this part to an integer
    
    //int incomingValue = atof(buffer);
    //desiredAngle = incomingValue;
    
    // say what you got:

    Serial.print("currStepPitch: ");
    Serial.println(currStepPitch);
    Serial.print("desiredStepPitch: ");
    Serial.println(desiredStepPitch);
    
    moveToAngle(currStepYaw, desiredStepYaw, currStepPitch, desiredStepPitch);
    currStepYaw = desiredStepYaw;
    currStepPitch = desiredStepPitch;
  }
}

void moveToAngle(float currStepYaw, float desiredStepYaw, float currStepPitch, float desiredStepPitch){
  int delStepsYaw = desiredStepYaw - currStepYaw;
  int delStepsPitch = desiredStepPitch - currStepPitch;
  Serial.println("INSIDE OF FUNCTION");
  if(delStepsYaw < 0){
    digitalWrite(dirPinYaw,LOW);
    delStepsYaw = delStepsYaw * -1;
    Serial.println("Reversing Direction.");
  }
  else{
    digitalWrite(dirPinYaw,HIGH);
  }

  if(delStepsPitch < 0){
    digitalWrite(dirPinPitch,LOW);
    delStepsPitch = delStepsPitch * -1;
    Serial.println("Reversing Direction.");
  }
  else{
    digitalWrite(dirPinPitch,HIGH);
  }
  
  Serial.print("delStepsYaw: ");
  Serial.println(delStepsYaw);
  Serial.print("delStepsPitch: ");
  Serial.println(delStepsPitch);
  Serial.println();

  if(delStepsYaw > 10){
    yawDelay = 0;
  }
  else{
    yawDelay = 0;
  }
  if(delStepsPitch > 10){
    pitchDelay = 0;
  }
  else{
    pitchDelay = 0;
  }
  
  for(int x = 0; x < delStepsYaw*2.0; x++) {
    digitalWrite(stepPinYaw,HIGH);
    delay(10);
    digitalWrite(stepPinYaw,LOW);
    delay(10);
    delay(yawDelay);
  }
  for(int x = 0; x < delStepsPitch*2.0; x++) {
    digitalWrite(stepPinPitch,HIGH);
    delay(10);
    digitalWrite(stepPinPitch,LOW);
    delay(10);
    delay(pitchDelay);
  }
  delay(1000);
}
