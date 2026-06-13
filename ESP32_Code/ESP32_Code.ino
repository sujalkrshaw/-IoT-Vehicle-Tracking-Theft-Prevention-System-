#include <WiFi.h>
#include <PubSubClient.h>

#define LED_PIN 27
#define BUZZER_PIN 26
#define BUTTON_PIN 25
#define RELAY_PIN 33

const char* ssid = "Wokwi-GUEST";
const char* password = "";

const char* mqtt_server = "broker.hivemq.com";

WiFiClient espClient;
PubSubClient client(espClient);

float latitude = 22.5726;
float longitude = 88.3639;

bool theftAlert = false;

void reconnect() {
  while (!client.connected()) {
    Serial.print("Connecting MQTT...");
    
    if (client.connect("ESP32VehicleTracker")) {
      Serial.println("Connected");
    } else {
      Serial.print(".");
      delay(1000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(RELAY_PIN, OUTPUT);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected");

  client.setServer(mqtt_server, 1883);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  if (digitalRead(BUTTON_PIN) == LOW) {
    theftAlert = true;
    latitude = 22.5900;
    longitude = 88.3900;
  }

  String payload;

  if (theftAlert) {

    digitalWrite(LED_PIN, HIGH);
    digitalWrite(RELAY_PIN, HIGH);

    payload =
      "{\"latitude\":" + String(latitude,4) +
      ",\"longitude\":" + String(longitude,4) +
      ",\"status\":\"THEFT ALERT\"}";
  }
  else {

    digitalWrite(LED_PIN, LOW);
    digitalWrite(RELAY_PIN, LOW);

    payload =
      "{\"latitude\":" + String(latitude,4) +
      ",\"longitude\":" + String(longitude,4) +
      ",\"status\":\"SAFE\"}";
  }

  client.publish("iot/vehicle/tracking", payload.c_str());

  Serial.println(payload);

  delay(2000);
}