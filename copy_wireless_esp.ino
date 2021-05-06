/*Motor Driver Configuration-
MOTOR-A
Pin 1- High-Clockwise
Pin 2- High- Anticlockwise
MOTOR-B
Pin 3- High-Clockwise
Pin 4- High- Anticlockwise
myservo1-LEFT SERVO
myservo2-RIGHT SERVO*/

#include<Servo.h>
#include <ESP8266WiFi.h> 
#include <ESP8266mDNS.h>
#include <WiFiClient.h>// Include the Wi-Fi library
WiFiServer server(80);
WiFiClient client;
int l;
int r;
Servo myservo1, myservo2;
const char* ssid     = "samsung";         // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "12345678";     // The password of the Wi-Fi network

int pos=0; //Initial Position of both the servos
int l1=2; // Connect l1 to Pin 1 of Motor Driver
int l2=0; //Connect l2 to pin 2 
int r1=15; //connect r1 to pin 3
int r2=13;//connect r2 to pin 4
int ena=14; //Enable A, Pin 5 is PWM for controlling speed
int enb=12;//Enable B, Pin 11 is PWM for controlling speed of motor
int speedr=150; //Chenge the values in order to configure perfectly of sppedl and speedr
int speedl=150;
char  val;
int rled=13; 
int bled=2;
char data;
int lm;
int rm;
int f;
int b;
void reverse()
{
  //Both motors will run clockwise here
  analogWrite(ena,speedl); //These tell motor with which speed it needs to move
  analogWrite(enb,speedr);
  digitalWrite(l1,HIGH);
  digitalWrite(l2,LOW);
  digitalWrite(r1,LOW);
  digitalWrite(r2,HIGH);
}

void forward()
{
  //Both motors will run anti clockwise here
  analogWrite(ena,speedl-5);
  analogWrite(enb,speedr-5);
  digitalWrite(l1,LOW);
  digitalWrite(l2,HIGH);
  digitalWrite(r1,HIGH);
  digitalWrite(r2,LOW);
}

void right()
{
  //Similar to right()
  //speedl=125;
  analogWrite(ena,speedl+2);
  analogWrite(enb,speedr+2);
  digitalWrite(l1,LOW);
  digitalWrite(l2,HIGH);
  digitalWrite(r1,LOW);
  digitalWrite(r2,HIGH); 
}


void left()
{//speedr=90;
  //Motor A goes clockwise and Motor B goes anti clockwise for very fast turning (keeping bot steady, it turns)
  analogWrite(ena,speedl+2);
  analogWrite(enb,speedr+2);
  digitalWrite(l1,HIGH);
  digitalWrite(l2,LOW);
  digitalWrite(r1,HIGH);
  digitalWrite(r2,LOW); 
}


void stop()
{
  //Stop the bot
  analogWrite(ena,0);
  analogWrite(enb,0);
  digitalWrite(l1,LOW);
  digitalWrite(l2,LOW);
  digitalWrite(r1,LOW);
  digitalWrite(r2,LOW);
}
void u2d()
{ //For servo movement from up to down
  for (pos = 70; pos <= 120; pos += 1) { // goes from intial degrees to final degrees
    // in steps of 1 degree
    myservo1.write(pos);
    delay(20); 
    myservo2.write(180-pos); // tell servo to go to position in variable 'pos'
    delay(20);                       
  }
}

void d2u()
{
  //For servo movement from down to up
  for (pos = 120; pos >= 70; pos -= 1) { // goes from final degrees to initial degrees
    myservo1.write(pos);
    delay(20);
    myservo2.write(180-pos);// tell servo to go to position in variable 'pos'
    delay(20);                       
  }
}

void start(String ssid, String pass){
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid.c_str(),pass.c_str());

  Serial.println("");
// Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
// Setting up mDNS responder
  if (!MDNS.begin("esp8266")) {
    Serial.println("Error setting up MDNS responder!");
    while (1) {
      delay(1000);
    }
  }
  Serial.println("mDNS responder started");
// Start TCP (HTTP) server
  server.begin();
  Serial.println("TCP server started");
// Add service to MDNS-SD
  MDNS.addService("http", "tcp", 80);
}

void setup() {
  Serial.begin(115200);
  start(ssid,password); // Wifi details connec to
  myservo1.attach(5);
  myservo2.attach(4);
  pinMode(l1,OUTPUT);
  pinMode(l2,OUTPUT);
  pinMode(r1,OUTPUT);
  pinMode(r2,OUTPUT);
  pinMode(ena,OUTPUT);
  pinMode(enb,OUTPUT);
  /*pinMode(3,OUTPUT);
  pinMode(rled,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(bled,OUTPUT);
  pinMode(10,OUTPUT);*/
}

void loop() {
    //right();
    //stop();
    //delay(1000);
    //bright();
    //delay(5000);
    //forward();
    //d2u();
    //u2d();
    //LEFT();
    if(server.available())
    {
      String req = client.readStringUntil('\r');
      Serial.println(req);
      int addr_start = req.indexOf(' ');
      addr_start+=1;
      int addr_end = req.indexOf(' ', addr_start + 1);
      Serial.println(addr_start);
      Serial.println(addr_end);
      if (addr_start == -1 || addr_end == -1) {
        Serial.print("Invalid request: ");
        Serial.println(req);
        return;
      }
      req = req.substring(addr_start + 1, addr_end);
      speedr=req.toInt();
      addr_start=req.indexOf(' ', addr_end + 1);
      addr_end = req.indexOf(' ', addr_start + 1);
      req = req.substring(addr_start + 1, addr_end);
      speedl=req.toInt();
      addr_start=req.indexOf(' ', addr_end + 1);
      addr_end = req.indexOf(' ', addr_start + 1);
      req = req.substring(addr_start + 1, addr_end);
      r=req.toInt();
      addr_start=req.indexOf(' ', addr_end + 1);
      addr_end = req.indexOf(' ', addr_start + 1);
      req = req.substring(addr_start + 1, addr_end);
      l=req.toInt();
      Serial.println(speedr);
      Serial.println(speedl);
      Serial.println(r);
      Serial.println(l);
    

    /*if(getPath() == "/f"){
      forward();
      //digitalWrite(rled,HIGH);
    }

    else if(getPath() == "/b"){
      reverse();
      //digitalWrite(rled,LOW);
    }

    else if(getPath() == "/r"){
      right();
      //Serial.println(data);
      //delay(90); // 
      //stop();
    
    }
    else if(getPath()== "/l"){
      left();
      //delay(60); //45
      //stop();
    
    }
    else if(getPath() == "/U"){           //to move servo up
      d2u();
      //delay(60); //45
      stop();
    
    }
    
    else if(getPath() == "/D"){
      u2d();
      //delay(60); //45
      stop();
    
    }
    else if(getPath() == "/s")
    {
      stop();
      }
      */
    }
  }
