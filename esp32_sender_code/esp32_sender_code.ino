#include <WiFi.h>
#include <esp_now.h>

#define RECIPIENT_MAC {0xA8, 0x48, 0xFA, 0xF0, 0x57, 0x9A} // Replace with the receiver's MAC address
// 48:3F:DA:4A:AB:9D
typedef struct struct_message {
  char command[10];
} struct_message;

struct_message myData;
uint8_t recipient_mac[6] = RECIPIENT_MAC;

void setup() {
  Serial.begin(115200);  // Initialize serial communication
  WiFi.mode(WIFI_STA);   // Set ESP32 to station mode

  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Add peer (receiver ESP8266)
  esp_now_peer_info_t peerInfo;
  memcpy(peerInfo.peer_addr, recipient_mac, 6);
  peerInfo.channel = 0;  // Use the same channel as the receiver
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer");
    return;
  }
}

void sendGesture(const char* gesture) {
  strcpy(myData.command, gesture);  // Copy the gesture into the struct
  esp_err_t result = esp_now_send(recipient_mac, (uint8_t*)&myData, sizeof(myData));  // Send data via ESP-NOW

  if (result == ESP_OK) {
    Serial.println("Sent successfully");
  } else {
    Serial.println("Send failed");
  }
}

void loop() {
  if (Serial.available()) {
    String gesture = Serial.readStringUntil('\n');  // Read incoming serial data
    gesture.trim();  // Remove any extra whitespace/newline characters

    if (gesture.length() > 0) {
      sendGesture(gesture.c_str());  // Send the received gesture command
    }
  }
}
