// #include <WiFi.h> // Bibliothèque Wi-Fi pour ESP32
// #include <HTTPClient.h> // Bibliothèque HTTP pour les requêtes
// #include <ArduinoJson.h> // Bibliothèque pour manipuler JSON

// // Configuration Wi-Fi fixe
// const char* ssid = "UNIFI_IDO2"; 
// const char* password = "99Bidules!";

// // Adresse IP de mon serveur Django
// String server = "http://192.168.20.220:8000"; 

// // Intervalle d’envoi (en millisecondes)
// const unsigned long sensorInterval = 10000; // 10 secondes
// unsigned long lastSensor = 0; // Timestamp du dernier envoi. Mémorise la valeur de millis() lors du dernier envoi.

// void setup() {
//   Serial.begin(115200); // Initialisation de la communication série
//   delay(100); 
//   Serial.println();
//   Serial.println("--- Boot ESP32 ---");

//   WiFi.begin(ssid, password); // Connexion au réseau Wi-Fi. Démarre la tentative de connexion au réseau Wi-Fi.
//   Serial.print("Connexion à ");
//   Serial.print(ssid);
//   Serial.print("...");

//   int tries = 0;
//   // Attendre la connexion Wi-Fi
//   while (WiFi.status() != WL_CONNECTED && tries++ < 20) { // Limite à 20 tentatives
//     delay(500);
//     Serial.print("."); // Affiche un point pour chaque tentative
//   }

//   if (WiFi.status() == WL_CONNECTED) { // Vérifie si la connexion a réussi
//     Serial.println("\nConnecté !"); // Affiche un message de succès
//     Serial.print("IP locale : "); // Affiche l'adresse IP locale attribuée à l'ESP32
//     Serial.println(WiFi.localIP()); // Affiche l'adresse IP locale
//   } else { // Si la connexion a échoué après 20 tentatives
//     Serial.println("\nÉchec de connexion"); // Affiche un message d'échec
//   }
// }

// // Fonction pour envoyer les données du capteur au serveur Django
// void sendSensorData(float value) { // Envoie les données du capteur au serveur Django
//   if (WiFi.status() != WL_CONNECTED) { // Vérifie si le Wi-Fi est connecté
//     Serial.println("Wi-Fi non connecté, envoi annulé"); // Affiche un message d'erreur si le Wi-Fi n'est pas connecté
//     return; // Quitte la fonction si le Wi-Fi n'est pas connecté
//   }

//   HTTPClient http; // Crée une instance de HTTPClient pour gérer la requête HTTP
//   // http.begin(server + "/api/sensor/");
//   http.begin(server + "/api/receive_sensor_data/"); // Initialise la requête HTTP POST vers l'URL spécifiée

//   http.addHeader("Content-Type", "application/json"); // Définit l'en-tête HTTP pour indiquer que le corps de la requête est au format JSON

//   DynamicJsonDocument doc(256); // Crée un document JSON dynamique avec une capacité de 256 octets
//   doc["sensor_type"] = "temperature"; // Ajoute le type de capteur au document JSON
//   doc["value"] = value; // Ajoute la valeur du capteur au document JSON
//   doc["unit"] = "°C"; // Ajoute l'unité de mesure au document JSON

//   String payload; // Chaîne pour stocker le JSON sérialisé
//   serializeJson(doc, payload); // Sérialise le document JSON dans la chaîne payload

//   int code = http.POST(payload); // Envoie la requête HTTP POST avec le corps JSON et récupère le code de réponse
//   Serial.print("POST capteur code : "); // Affiche le code de réponse HTTP
//   Serial.println(code); // Affiche le code de réponse HTTP

//   http.end(); // Termine la requête HTTP pour libérer les ressources
// }

// // Boucle principale
// void loop() {
//   if (millis() - lastSensor > sensorInterval) { // Vérifie si l'intervalle d'envoi est écoulé
//     float fakeTemp = random(200, 300) / 10.0; // 20.0 à 30.0 °C
//     Serial.print("Température simulée : ");
//     Serial.println(fakeTemp); // Affiche la température simulée dans le moniteur série
//     sendSensorData(fakeTemp); // Envoie les données du capteur au serveur Django
//     lastSensor = millis(); // Met à jour le timestamp du dernier envoi
//   }
// }


// #include <WiFi.h>
// #include <HTTPClient.h>
// #include <ArduinoJson.h>
// #include "DHT.h"

// // ==== Configuration Wi-Fi ====
// const char* ssid = "UNIFI_IDO2";
// const char* password = "99Bidules!";

// // ==== Adresse du serveur Django ====
// String server = "http://192.168.20.220:8000/api/receive_sensor_data/";  // Remplace par ton IP

// // ==== Capteur DHT22 ====
// #define DHTPIN 4         // Broche de données DHT22 (ex: GPIO4)
// #define DHTTYPE DHT22
// DHT dht(DHTPIN, DHTTYPE);

// // ==== Intervalle d’envoi ====
// const unsigned long sensorInterval = 10000; // 10 secondes
// unsigned long lastSensor = 0;

// // ==== Setup ====
// void setup() {
//   Serial.begin(115200);
//   delay(100);
//   Serial.println();
//   Serial.println("--- Démarrage ESP32 + DHT22 ---");

//   // Initialisation du capteur
//   dht.begin();

//   // Connexion Wi-Fi
//   WiFi.begin(ssid, password);
//   Serial.print("Connexion à ");
//   Serial.println(ssid);

//   int tries = 0;
//   while (WiFi.status() != WL_CONNECTED && tries++ < 20) {
//     delay(500);
//     Serial.print(".");
//   }

//   if (WiFi.status() == WL_CONNECTED) {
//     Serial.println("\nConnecté !");
//     Serial.print("Adresse IP : ");
//     Serial.println(WiFi.localIP());
//   } else {
//     Serial.println("\nÉchec de connexion Wi-Fi");
//   }
// }

// // ==== Fonction d’envoi des données ====
// void sendSensorData(String type, float value, String unit) {
//   if (WiFi.status() != WL_CONNECTED) {
//     Serial.println("Wi-Fi non connecté, envoi annulé");
//     return;
//   }

//   HTTPClient http;
//   http.begin(server);
//   http.addHeader("Content-Type", "application/json");

//   DynamicJsonDocument doc(256);
//   doc["sensor_type"] = type;
//   doc["value"] = value;
//   doc["unit"] = unit;

//   String payload;
//   serializeJson(doc, payload);

//   int code = http.POST(payload);
//   Serial.print("POST ");
//   Serial.print(type);
//   Serial.print(" → Code ");
//   Serial.println(code);

//   http.end();
// }

// // ==== Boucle principale ====
// void loop() {
//   if (millis() - lastSensor > sensorInterval) {
//     float temperature = dht.readTemperature();  // en °C
//     float humidity = dht.readHumidity();        // en %

//     if (isnan(temperature) || isnan(humidity)) {
//       Serial.println("Erreur lecture DHT22");
//       return;
//     }

//     Serial.print("Température : ");
//     Serial.print(temperature);
//     Serial.print(" °C | Humidité : ");
//     Serial.print(humidity);
//     Serial.println(" %");

//     sendSensorData("temperature", temperature, "°C");
//     sendSensorData("humidity", humidity, "%");

//     lastSensor = millis();
//   }
// }


#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

// ==== WiFi ====
const char* ssid = "UNIFI_IDO2";
const char* password = "99Bidules!";

// ==== Serveur Django ====
String SERVER_URL = "http://192.168.20.220:8000/api/";
String SEND_ENDPOINT = SERVER_URL + "receive_sensor_data/";
String SPEED_ENDPOINT = SERVER_URL + "fan_speed/";

// ==== DHT22 ====
#define DHTPIN 27
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// ==== Ventilateur (PWM) ====
#define FAN_PIN 18
#define PWM_CHANNEL 0
#define PWM_FREQ 25000   // 25 kHz recommandé pour PWM silencieux
#define PWM_RESOLUTION 8 // 8 bits = 0–255
int fanSpeed = 0;        // 0–255 (0%–100%)

unsigned long lastSensorSend = 0;
unsigned long lastSpeedCheck = 0;
const unsigned long sensorInterval = 10000; // 10 s
const unsigned long speedInterval = 5000;   // 5 s

// ==== Setup ====
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n--- ESP32 Filtration Connectée ---");

  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Connexion à ");
  Serial.println(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnecté !");
  Serial.print("Adresse IP : ");
  Serial.println(WiFi.localIP());

  // Configuration PWM
  ledcSetup(PWM_CHANNEL, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(FAN_PIN, PWM_CHANNEL);
  ledcWrite(PWM_CHANNEL, fanSpeed);
  Serial.println("PWM initialisé pour le ventilateur.");
}

// ==== Envoi des données capteurs ====
void sendSensorData(String type, float value, String unit) {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(SEND_ENDPOINT);
  http.addHeader("Content-Type", "application/json");

  DynamicJsonDocument doc(256);
  doc["sensor_type"] = type;
  doc["value"] = value;
  doc["unit"] = unit;
  String payload;
  serializeJson(doc, payload);

  int code = http.POST(payload);
  Serial.printf("Envoi %s → %d\n", type.c_str(), code);
  http.end();
}

// ==== Lecture de la vitesse depuis Django ====
void updateFanSpeed() {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(SPEED_ENDPOINT);
  int code = http.GET();

  if (code == 200) {
    String response = http.getString();
    DynamicJsonDocument doc(256);
    deserializeJson(doc, response);
    int newSpeed = doc["fan_speed"];

    if (newSpeed != fanSpeed) {
      fanSpeed = map(newSpeed, 0, 100, 0, 255);
      ledcWrite(PWM_CHANNEL, fanSpeed);
      Serial.printf("Nouvelle vitesse : %d%% → PWM %d\n", newSpeed, fanSpeed);
    }
  }
  http.end();
}

// ==== Boucle ====
void loop() {
  unsigned long now = millis();

  // Lecture capteur
  if (now - lastSensorSend > sensorInterval) {
    float t = dht.readTemperature();
    float h = dht.readHumidity();

    if (isnan(t) || isnan(h)) {
      Serial.println("Erreur lecture DHT22");
    } else {
      Serial.printf("Température: %.2f °C | Humidité: %.2f %%\n", t, h);
      sendSensorData("temperature", t, "°C");
      sendSensorData("humidity", h, "%");
    }
    lastSensorSend = now;
  }

  // Vérifie vitesse toutes les 5 secondes
  if (now - lastSpeedCheck > speedInterval) {
    updateFanSpeed();
    lastSpeedCheck = now;
  }
}
