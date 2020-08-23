#include <ArduinoJson.h>
#include <ESP8266WebServer.h>
#include <ESP8266WebServerSecure.h>
extern "C" {
#include "user_interface.h"
}
// includes
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "raspberryFi";
const char* passwd = "@teamBTG";

const int output0 = 4;

// Web server port number to 80
ESP8266WebServer server(80);


void setup()
{
  Serial.begin(115200);

  // initialize pin
  pinMode(output0, OUTPUT);
  analogWrite(output0, 0);  
  WiFi.begin("raspberryFi","@teamBTG"); // connect to WiFi client
  Serial.println("Waiting to connect to pi...");
  while(WiFi.status()!=WL_CONNECTED) // while connection isn't there
  {  
    delay(2000);
    Serial.println("...");
  }

  Serial.print("IP ADDRESS: ");
  Serial.println(WiFi.localIP()); // Print designated IP from client

  server.on("/Python", handleBody);  
  server.begin(); // Start server
  Serial.println("Server ready...");
}

void loop()
{
  server.handleClient(); // handles incoming requests from Pi

  uint32_t free = system_get_free_heap_size();
}

void handleBody() // Handler for the body path
{
  
  

  if(server.hasArg("plain") == false) // Check is body received
  {
    server.send(200, "text/json", "{\"success\":\"false\"}");
    return;
  }
  StaticJsonBuffer<128> newBuffer;
  JsonObject& newjson = newBuffer.parseObject(server.arg("plain"));
  
  server.send(200, "text/json", "{\"success\":\"true\"}");

  //newjson.containsKey(

  Serial.println("-- request received --");

  String MODE = newjson["ON"];
  String INTENSITY = newjson["INTENSITY"];
  String HOST = newjson["HOST"];
  int intensity = INTENSITY.toInt();
  int onOff = MODE.toInt();
  Serial.println("New setting(s) for host: ");

  String hostName = "host name: " + HOST;
  Serial.println(hostName);

  String printonOff = "on(1) / off(0): " + MODE;
  Serial.println(printonOff);

  String printIntens = "intensity(0-10): " + INTENSITY;
  Serial.println(printIntens);

  if(onOff == 1)
  {
    switch (intensity) 
    {
      case 0:
        analogWrite(output0, 0);
        break;
      case 1:
        analogWrite(output0, 51);
        break;
      case 2:
        analogWrite(output0, 102);
        break;
      case 3:
        analogWrite(output0, 153);
        break;
      case 4:
        analogWrite(output0, 204);
        break;
      case 5:
        analogWrite(output0, 255);
        break;
    }
    
  }
  else
  {
    analogWrite(output0, 0);
  }
  //uint32_t freeheap = system_get_free_heap_size();
  //Serial.println(freeheap);
}


//void handlePath()
//{
//  server.send(200, "text/plain", "Hello Python");
//}
