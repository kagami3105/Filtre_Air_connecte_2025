#include <WiFi.h> // Bibliothèque Wi-Fi pour ESP32
#include <HTTPClient.h> // Bibliothèque HTTP pour les requêtes
#include <ArduinoJson.h> // Bibliothèque pour manipuler JSON

// Configuration Wi-Fi fixe
const char* ssid = "UNIFI_IDO2"; 
const char* password = "99Bidules!";

// Adresse IP de mon serveur Django
String server = "http://192.168.20.220:8000"; 

// Intervalle d’envoi (en millisecondes)
const unsigned long sensorInterval = 10000; // 10 secondes
unsigned long lastSensor = 0; // Timestamp du dernier envoi. Mémorise la valeur de millis() lors du dernier envoi.

void setup() {
  Serial.begin(115200); // Initialisation de la communication série
  delay(100); 
  Serial.println();
  Serial.println("--- Boot ESP32 ---");

  WiFi.begin(ssid, password); // Connexion au réseau Wi-Fi. Démarre la tentative de connexion au réseau Wi-Fi.
  Serial.print("Connexion à ");
  Serial.print(ssid);
  Serial.print("...");

  int tries = 0;
  // Attendre la connexion Wi-Fi
  while (WiFi.status() != WL_CONNECTED && tries++ < 20) { // Limite à 20 tentatives
    delay(500);
    Serial.print("."); // Affiche un point pour chaque tentative
  }

  if (WiFi.status() == WL_CONNECTED) { // Vérifie si la connexion a réussi
    Serial.println("\nConnecté !"); // Affiche un message de succès
    Serial.print("IP locale : "); // Affiche l'adresse IP locale attribuée à l'ESP32
    Serial.println(WiFi.localIP()); // Affiche l'adresse IP locale
  } else { // Si la connexion a échoué après 20 tentatives
    Serial.println("\nÉchec de connexion"); // Affiche un message d'échec
  }
}

// Fonction pour envoyer les données du capteur au serveur Django
void sendSensorData(float value) { // Envoie les données du capteur au serveur Django
  if (WiFi.status() != WL_CONNECTED) { // Vérifie si le Wi-Fi est connecté
    Serial.println("Wi-Fi non connecté, envoi annulé"); // Affiche un message d'erreur si le Wi-Fi n'est pas connecté
    return; // Quitte la fonction si le Wi-Fi n'est pas connecté
  }

  HTTPClient http; // Crée une instance de HTTPClient pour gérer la requête HTTP
  // http.begin(server + "/api/sensor/");
  http.begin(server + "/api/receive_sensor_data/"); // Initialise la requête HTTP POST vers l'URL spécifiée

  http.addHeader("Content-Type", "application/json"); // Définit l'en-tête HTTP pour indiquer que le corps de la requête est au format JSON

  DynamicJsonDocument doc(256); // Crée un document JSON dynamique avec une capacité de 256 octets
  doc["sensor_type"] = "temperature"; // Ajoute le type de capteur au document JSON
  doc["value"] = value; // Ajoute la valeur du capteur au document JSON
  doc["unit"] = "°C"; // Ajoute l'unité de mesure au document JSON

  String payload; // Chaîne pour stocker le JSON sérialisé
  serializeJson(doc, payload); // Sérialise le document JSON dans la chaîne payload

  int code = http.POST(payload); // Envoie la requête HTTP POST avec le corps JSON et récupère le code de réponse
  Serial.print("POST capteur code : "); // Affiche le code de réponse HTTP
  Serial.println(code); // Affiche le code de réponse HTTP

  http.end(); // Termine la requête HTTP pour libérer les ressources
}

// Boucle principale
void loop() {
  if (millis() - lastSensor > sensorInterval) { // Vérifie si l'intervalle d'envoi est écoulé
    float fakeTemp = random(200, 300) / 10.0; // 20.0 à 30.0 °C
    Serial.print("Température simulée : ");
    Serial.println(fakeTemp); // Affiche la température simulée dans le moniteur série
    sendSensorData(fakeTemp); // Envoie les données du capteur au serveur Django
    lastSensor = millis(); // Met à jour le timestamp du dernier envoi
  }
}