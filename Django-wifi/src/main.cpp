#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Configuration Wi-Fi fixe
const char* ssid = "UNIFI_IDO2";
const char* password = "99Bidules!";

// Adresse IP de ton serveur Django
String server = "http://192.168.20.220:8000";

// Intervalle d’envoi (en millisecondes)
const unsigned long sensorInterval = 10000;
unsigned long lastSensor = 0;

void setup() {
  Serial.begin(115200);
  delay(100);
  Serial.println();
  Serial.println("--- Boot ESP32 ---");

  WiFi.begin(ssid, password);
  Serial.print("Connexion à ");
  Serial.print(ssid);
  Serial.print("...");

  int tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries++ < 20) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnecté !");
    Serial.print("IP locale : ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nÉchec de connexion");
  }
}

void sendSensorData(float value) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi non connecté, envoi annulé");
    return;
  }

  HTTPClient http;
  // http.begin(server + "/api/sensor/");
  http.begin(server + "/api/receive_sensor_data/");

  http.addHeader("Content-Type", "application/json");

  DynamicJsonDocument doc(256);
  doc["sensor_type"] = "temperature";
  doc["value"] = value;
  doc["unit"] = "°C";

  String payload;
  serializeJson(doc, payload);

  int code = http.POST(payload);
  Serial.print("POST capteur code : ");
  Serial.println(code);

  http.end();
}

void loop() {
  if (millis() - lastSensor > sensorInterval) {
    float fakeTemp = random(200, 300) / 10.0; // 20.0 à 30.0 °C
    Serial.print("Température simulée : ");
    Serial.println(fakeTemp);
    sendSensorData(fakeTemp);
    lastSensor = millis();
  }
}