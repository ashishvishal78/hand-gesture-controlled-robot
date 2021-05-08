#include<Servo.h>
#include <ESP8266WiFi.h> 
#include <ESP8266mDNS.h>
#include <WiFiClient.h>// Include the Wi-Fi library
WiFiServer server(80);
WiFiClient client;

/* WIFI settings */
const char* ssid     = "samsung";         // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "12345678";

/* data received from application */
//String  data ="";
/* define L298N or L293D motor control pins */
int leftMotorForward = 2;     /* GPIO2(D4) -> IN3   */
int rightMotorForward = 15;   /* GPIO15(D8) -> IN1  */
int leftMotorBackward = 0;    /* GPIO0(D3) -> IN4   */
int rightMotorBackward = 13;  /* GPIO13(D7) -> IN2  */
/* define L298N or L293D enable pins */
int rightMotorENB = 14; /* GPIO14(D5) -> Motor-A Enable */
int leftMotorENB = 12;  /* GPIO12(D6) -> Motor-B Enable */
int speedl=0;
int speedr=0;
char data;
/********************************************* FORWARD *****************************************************/
void MotorForward(void)  
{
  analogWrite(leftMotorENB,speedl);
  analogWrite(rightMotorENB,speedr);
  digitalWrite(leftMotorForward,HIGH);
  digitalWrite(rightMotorForward,HIGH);
  digitalWrite(leftMotorBackward,LOW);
  digitalWrite(rightMotorBackward,LOW);
}
/********************************************* BACKWARD *****************************************************/
void MotorBackward(void)  
{
  Serial.println("mb");
  analogWrite(leftMotorENB,speedl);
  analogWrite(rightMotorENB,speedr);
  digitalWrite(leftMotorBackward,HIGH);
  digitalWrite(rightMotorBackward,HIGH);
  digitalWrite(leftMotorForward,LOW);
  digitalWrite(rightMotorForward,LOW);
}
/********************************************* TURN LEFT *****************************************************/
void TurnLeft(void)  
{
  Serial.println("mr");
  analogWrite(leftMotorENB,speedl);
  analogWrite(rightMotorENB,speedr);
  digitalWrite(leftMotorForward,LOW);
  digitalWrite(rightMotorForward,HIGH);
  digitalWrite(rightMotorBackward,LOW);
  digitalWrite(leftMotorBackward,HIGH);  
}
/********************************************* TURN RIGHT *****************************************************/
void TurnRight(void)  
{
  Serial.println("ml");
  analogWrite(leftMotorENB,speedl);
  analogWrite(rightMotorENB,speedr);
  digitalWrite(leftMotorForward,HIGH);
  digitalWrite(rightMotorForward,LOW);
  digitalWrite(rightMotorBackward,HIGH);
  digitalWrite(leftMotorBackward,LOW);
}
/********************************************* STOP *****************************************************/
void MotorStop(void)  
{
  Serial.println("ms");
  analogWrite(leftMotorENB,speedl);
  analogWrite(rightMotorENB,speedr);
  digitalWrite(leftMotorForward,LOW);
  digitalWrite(leftMotorBackward,LOW);
  digitalWrite(rightMotorForward,LOW);
  digitalWrite(rightMotorBackward,LOW);
}
/********************************** RECEIVE DATA FROM the APP ******************************************/
void checkClient (void)
{
  while(!client.available()) delay(1);
  String request = client.readStringUntil('\r');
  Serial.println(request);
  request.remove(0, 5);
  request.remove(request.length()-9,9);
  Serial.println(request);

 
  data=request[0];
  speedl=request.substring(2,5).toInt();
  speedr=request.substring(6,9).toInt();
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
void setup()
{
  Serial.begin(115200);
  start(ssid,password); // Wifi details connec to
  /* initialize motor control pins as output */
  pinMode(leftMotorForward, OUTPUT);
  pinMode(rightMotorForward, OUTPUT);
  pinMode(leftMotorBackward, OUTPUT);  
  pinMode(rightMotorBackward, OUTPUT);
  /* initialize motor enable pins as output */
  pinMode(leftMotorENB, OUTPUT);
  pinMode(rightMotorENB, OUTPUT);
  /* start server communication */
  server.begin();
}
void loop()
{
    /* If the server available, run the "checkClient" function */  
    client = server.available();
    if (!client) return;
//    data = checkClient ();
    checkClient ();
    Serial.println(data);
    Serial.println(speedl);
    Serial.println(speedr);
    
/************************ Run function according to incoming data from application *************************/
    /* If the incoming data is "forward", run the "MotorForward" function */
    if (data == 'f') MotorForward();
    /* If the incoming data is "backward", run the "MotorBackward" function */
    else if (data == 'b') MotorBackward();
    /* If the incoming data is "left", run the "TurnLeft" function */
    else if (data == 'l') TurnLeft();
    /* If the incoming data is "right", run the "TurnRight" function */
    else if (data == 'r') TurnRight();
    /* If the incoming data is "stop", run the "MotorStop" function */
    else if (data == 's') MotorStop();
}
