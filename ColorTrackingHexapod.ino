#define DXL_BUS_SERIAL1 1 //Dynamixel on Serial1(USART1) <-OpenCM9.04 
#define DXL_BUS_SERIAL2 3 //Dynamixel on Serial2(USART2) <-LN101,BT210 
#define DXL_BUS_SERIAL3 3 //Dynamixel on Serial3(USART3) <-OpenCM 485EXP

Dynamixel Dxl(DXL_BUS_SERIAL1);

char inChar;
byte index = 0;
int maxspeed = 400;

void setup() {
  // Set up the pin 10 as an output:
  pinMode(BOARD_LED_PIN, OUTPUT);
  Serial3.begin(9600);
  Dxl.begin(3);
  Dxl.wheelMode(1); //LEFT WHEEL
  Dxl.wheelMode(3); //RIGHT WHEEL
  Dxl.jointMode(5); //CLAW
}


void loop() {
  //initial condition
  Dxl.goalSpeed(1, 0);
  Dxl.goalSpeed(3, 0);
  
  //initial condition for claw
  Dxl.goalPosition(5, 700); // open
  //Dxl.goalPosition(5,450); // close
  
  
  if(SerialUSB.available() > 0){
    char inData[20];
    while(SerialUSB.available()>0){
      if(index < 19){
        inChar = SerialUSB.read(); //read a character
        inData[index] = inChar;
        index++;
        inData[index] = '\0';
      }
    }
  
    index = 0;
  
 
    //forward
    if(inData[0] >= char(0)) {
    //&& inData[0] <= char(30) && inData[0] > char(120) && inData[0] <= char(147))
      Dxl.goalSpeed(1, maxspeed); 
      Dxl.goalSpeed(3, maxspeed | 0x400);
    }
    //left
    if(inData[0] > char(30) && inData[0] <= char(120)){
      Dxl.goalSpeed(1, maxspeed | 0x400);
      Dxl.goalSpeed(3, maxspeed | 0x400);
    }
    //right
    if(inData[0] > char(147) && inData[0] <= char(245)){
      Dxl.goalSpeed(1, maxspeed);
      Dxl.goalSpeed(3, maxspeed);
    }
    delay(100);
  

    if (Serial3.available() > 0){
      char inData[20];
      while(Serial3.available()>0){
        if(index < 19){
          inChar = Serial3.read(); //read a character
          inData[index] = inChar;
          index++;
          inData[index] = '\0';
        }
      }
    
      index = 0;
   
    
      //close claw
      if(inData[0] > char(195)){
        Dxl.goalPosition(5, 300);
        //Dxl.goalSpeed(1, maxspeed | 0x400);
        //Dxl.goalSpeed(3, maxspeed);
        delay(5000);
      }
      delay(100);
    }
  }
}
