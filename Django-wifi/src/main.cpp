// #include <Arduino.h>
// #include <WiFi.h>
// #include <HTTPClient.h>
// #include <ArduinoJson.h>

// // Adresse IP de ton serveur Django (remplace par l’IP locale de ton PC)
// String server = "http://192.168.1.23:8000";  

// // Réseau par défaut pour démarrer
// const char* defaultSSID = "ESP32-Access-Point";
// const char* defaultPASS = "abcdefgh";

// // Intervalle de polling (en millisecondes)
// const unsigned long pollingInterval = 30000;
// unsigned long lastPoll = 0;

// // Fonction pour récupérer la config Wi-Fi depuis Django
// void getWifiConfig(String &ssid, String &password) {
//   if (WiFi.status() != WL_CONNECTED) {
//     Serial.println("getWifiConfig: WiFi non connecté, requête ignorée");
//     return;
//   }

//   HTTPClient http;
//   http.begin(server + "/api/wifi/");
//   int code = http.GET();
//   if (code == HTTP_CODE_OK) {
//     DynamicJsonDocument doc(256);
//     DeserializationError err = deserializeJson(doc, http.getString());
//     if (!err) {
//       ssid = doc["ssid"].as<String>();
//       password = doc["password"].as<String>();
//       Serial.println("Config Django reçue :");
//       Serial.println("SSID: " + ssid);
//     } else {
//       Serial.print("Erreur JSON : ");
//       Serial.println(err.c_str());
//     }
//   } else {
//     Serial.print("Erreur HTTP GET : ");
//     Serial.println(code);
//   }
//   http.end();
// }

// // Fonction pour envoyer le statut à Django
// void postStatus(bool connected, String ip, String message) {
//   if (WiFi.status() != WL_CONNECTED) {
//     Serial.println("postStatus: WiFi non connecté, requête ignorée");
//     return;
//   }

//   HTTPClient http;
//   http.begin(server + "/api/status/");
//   http.addHeader("Content-Type", "application/json");

//   DynamicJsonDocument doc(256);
//   doc["connected"] = connected;
//   doc["ip_address"] = ip;
//   doc["message"] = message;

//   String payload;
//   serializeJson(doc, payload);

//   int code = http.POST(payload);
//   Serial.print("POST statut code : ");
//   Serial.println(code);

//   http.end();
// }

// // Fonction pour se connecter à un réseau donné
// bool connectToWifi(String ssid, String password) {
//   WiFi.disconnect();
//   WiFi.begin(ssid.c_str(), password.c_str());
//   Serial.print("Connexion à " + ssid + "...");
//   int tries = 0;
//   while (WiFi.status() != WL_CONNECTED && tries++ < 20) {
//     delay(500);
//     Serial.print(".");
//   }
//   Serial.println();

//   if (WiFi.status() == WL_CONNECTED) {
//     Serial.println("Connecté !");
//     Serial.print("IP locale : ");
//     Serial.println(WiFi.localIP());
//     return true;
//   } else {
//     Serial.println("Échec de connexion");
//     return false;
//   }
// }

// // Fonction principale de polling
// void connectWifiFromServer() {
//   String ssid, password;
//   getWifiConfig(ssid, password);

//   if (ssid.isEmpty()) {
//     Serial.println("Pas de config Django, on garde le réseau actuel.");
//     return;
//   }

//   bool ok = connectToWifi(ssid, password);
//   postStatus(ok, ok ? WiFi.localIP().toString() : "", ok ? "Connecté (Django)" : "Échec Wi-Fi (Django)");
// }

// void setup() {
//   Serial.begin(115200);
//   delay(100);
//   Serial.println();
//   Serial.println("--- Boot ESP32 ---");

//   // Connexion initiale au réseau par défaut
//   bool ok = connectToWifi(defaultSSID, defaultPASS);
//   postStatus(ok, ok ? WiFi.localIP().toString() : "", ok ? "Connecté (défaut)" : "Échec Wi-Fi (défaut)");

//   // Premier polling immédiat
//   connectWifiFromServer();
// }

// void sendAvailableNetworks() {
//   int n = WiFi.scanNetworks();
//   Serial.println(" Scan des réseaux Wi-Fi...");

//   DynamicJsonDocument doc(1024);
//   JsonArray networks = doc.createNestedArray("networks");

//   for (int i = 0; i < n; ++i) {
//     JsonObject net = networks.createNestedObject();
//     net["ssid"] = WiFi.SSID(i);
//     net["rssi"] = WiFi.RSSI(i);
//     net["secure"] = WiFi.encryptionType(i) != WIFI_AUTH_OPEN;
//   }

//   String payload;
//   serializeJson(doc, payload);

//   HTTPClient http;
//   http.begin("http://192.168.1.23:8000/api/networks/"); 
//   http.addHeader("Content-Type", "application/json");
//   int code = http.POST(payload);
//   Serial.print("POST réseaux code : ");
//   Serial.println(code);
//   http.end();
// }
// void loop() {
//   // Heartbeat pour suivi dans le moniteur série
//   static unsigned long lastHeartbeat = 0;
//   if (millis() - lastHeartbeat > 5000) {
//     Serial.println("Heartbeat: alive");
//     lastHeartbeat = millis();
//   }

//   // Polling toutes les 30 secondes
//   if (millis() - lastPoll > pollingInterval) {
//     connectWifiFromServer();
//     lastPoll = millis();
//   }

//   static unsigned long lastScan = 0;
// if (millis() - lastScan > 60000) {
//   sendAvailableNetworks();
//   lastScan = millis();
// }
// }


#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Adresse IP de ton serveur Django
String server = "http://192.168.1.23:8000";

// Réseau par défaut pour démarrer
const char* defaultSSID = "ESP32-Access-Point";
const char* defaultPASS = "abcdefgh";

// Intervalles en millisecondes
const unsigned long pollingInterval = 30000;
const unsigned long scanInterval = 60000;
const unsigned long sensorInterval = 10000;
const unsigned long heartbeatInterval = 5000;

// Timers
unsigned long lastPoll = 0;
unsigned long lastScan = 0;
unsigned long lastSensor = 0;
unsigned long lastHeartbeat = 0;

// 🔌 Connexion à un réseau donné
bool connectToWifi(String ssid, String password) {
  WiFi.disconnect();
  WiFi.begin(ssid.c_str(), password.c_str());
  Serial.print("Connexion à " + ssid + "...");
  int tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries++ < 20) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Connecté !");
    Serial.print("IP locale : ");
    Serial.println(WiFi.localIP());
    return true;
  } else {
    Serial.println("Échec de connexion");
    return false;
  }
}

// Récupérer la config Wi-Fi depuis Django
void getWifiConfig(String &ssid, String &password) {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(server + "/api/wifi/");
  int code = http.GET();
  if (code == HTTP_CODE_OK) {
    DynamicJsonDocument doc(256);
    DeserializationError err = deserializeJson(doc, http.getString());
    if (!err) {
      ssid = doc["ssid"].as<String>();
      password = doc["password"].as<String>();
      Serial.println("Config Django reçue : " + ssid);
    } else {
      Serial.print("Erreur JSON : ");
      Serial.println(err.c_str());
    }
  } else {
    Serial.print("Erreur HTTP GET : ");
    Serial.println(code);
  }
  http.end();
}

// Envoyer le statut ESP32
void postStatus(bool connected, String ip, String message) {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(server + "/api/status/");
  http.addHeader("Content-Type", "application/json");

  DynamicJsonDocument doc(256);
  doc["connected"] = connected;
  doc["ip_address"] = ip;
  doc["message"] = message;

  String payload;
  serializeJson(doc, payload);

  int code = http.POST(payload);
  Serial.print("POST statut code : ");
  Serial.println(code);

  http.end();
}

// Connexion via config Django
void connectWifiFromServer() {
  String ssid, password;
  getWifiConfig(ssid, password);

  if (ssid.isEmpty()) {
    Serial.println("Pas de config Django, on garde le réseau actuel.");
    return;
  }

  bool ok = connectToWifi(ssid, password);
  postStatus(ok, ok ? WiFi.localIP().toString() : "", ok ? "Connecté (Django)" : "Échec Wi-Fi (Django)");
}

// Scan des réseaux disponibles
void sendAvailableNetworks() {
  int n = WiFi.scanNetworks();
  Serial.println("Scan des réseaux Wi-Fi...");

  DynamicJsonDocument doc(1024);
  JsonArray networks = doc.createNestedArray("networks");

  for (int i = 0; i < n; ++i) {
    JsonObject net = networks.createNestedObject();
    net["ssid"] = WiFi.SSID(i);
    net["rssi"] = WiFi.RSSI(i);
    net["secure"] = WiFi.encryptionType(i) != WIFI_AUTH_OPEN;
  }

  String payload;
  serializeJson(doc, payload);

  HTTPClient http;
  http.begin(server + "/api/networks/");
  http.addHeader("Content-Type", "application/json");
  int code = http.POST(payload);
  Serial.print("POST réseaux code : ");
  Serial.println(code);
  http.end();
}

// Envoi de données capteur simulées
void sendSensorData(float value) {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(server + "/api/sensor/");
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

void setup() {
  Serial.begin(115200);
  delay(100);
  Serial.println();
  Serial.println("--- Boot ESP32 ---");

  bool ok = connectToWifi(defaultSSID, defaultPASS);
  postStatus(ok, ok ? WiFi.localIP().toString() : "", ok ? "Connecté (défaut)" : "Échec Wi-Fi (défaut)");

  connectWifiFromServer();  // premier polling
}

void loop() {
  // Heartbeat
  if (millis() - lastHeartbeat > heartbeatInterval) {
    Serial.println("Heartbeat: alive");
    lastHeartbeat = millis();
  }

  // Polling config Wi-Fi
  if (millis() - lastPoll > pollingInterval) {
    connectWifiFromServer();
    lastPoll = millis();
  }

  // Scan réseaux
  if (millis() - lastScan > scanInterval) {
    sendAvailableNetworks();
    lastScan = millis();
  }

  // Envoi capteur simulé
  if (millis() - lastSensor > sensorInterval) {
    float fakeTemp = random(200, 300) / 10.0; // 20.0 à 30.0 °C
    sendSensorData(fakeTemp);
    lastSensor = millis();
  }
}