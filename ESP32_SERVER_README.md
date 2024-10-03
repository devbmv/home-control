## ESP32 Integration

   The project integrates ESP32 devices to control and manage smart home appliances, such as lights, through a Wi-Fi connection. The ESP32 interacts with the Django backend over HTTP and WebSockets, allowing real-time control and monitoring of the devices. This interaction is crucial for sending and receiving commands, updating device states, and handling firmware updates remotely.

   It is important to note that this project represents an initial phase and is not a fully implemented, polished solution. While it demonstrates the basic functionality of smart home control, there are several areas that require further development, including enhanced security measures, performance optimizations, and additional features. Future iterations will address these aspects to ensure a more robust, secure, and scalable system.

### Key Features of the ESP32 Integration:

1. **Wi-Fi Communication**:
   - The ESP32 connects to the local Wi-Fi network using the SSID and password provided during setup.
   - Once connected, it communicates with the Django backend via HTTP requests to exchange device status and receive commands.

2. **HTTP Client**:
   - The ESP32 uses the `HTTPClient` library to send GET and POST requests to the Django server.
   - Basic authentication is implemented using Base64 encoding for secure communication.
   - Example: The device checks the light status from the Django server using:
     ```cpp
     http.begin(lightStatusUrl);
     addBasicAuth(http);
     int httpResponseCode = http.GET();
     ```

3. **Django Interaction**:
   - The ESP32 periodically pings the Django server to check whether it is online or offline using the `/lights_status/` endpoint.
   - It can send and receive commands related to controlling devices like turning lights on and off.
   - If the server is unavailable, the ESP32 attempts to reconnect and maintain device functionality.

4. **Firmware Updates**:
   - The ESP32 supports **OTA (Over-the-Air)** firmware updates, initiated from the Django backend.
   - The firmware is uploaded through the `/django_update_firmware/` endpoint, and the ESP32 handles the update process, including writing the firmware and restarting the device after a successful update.
   - Example of the firmware update process:
     ```cpp
         server.on("/django_update_firmware", HTTP_POST, [](AsyncWebServerRequest *request)
                  {
         if (!Update.hasError()) {
            AsyncWebServerResponse *response = request->beginResponse(200, "text/plain", "Update Success! Rebooting...");
            response->addHeader("Access-Control-Allow-Origin", "*");  // Allow access from any origin
            response->addHeader("Connection", "close");
            request->send(response);
            ESP.restart();
         } else {
            AsyncWebServerResponse *response = request->beginResponse(500, "text/plain", "Update Failed");
            response->addHeader("Access-Control-Allow-Origin", "*");  // Allow access from any origin
            request->send(response);
         } }, handleUpdateStart);
     ```

5. **Asynchronous Web Server**:
   - The ESP32 runs an asynchronous web server using the `ESPAsyncWebServer` library to handle HTTP requests.
   - The server handles different routes for checking device states, updating firmware, and receiving commands.
   - Example: A request to control a light:
     ```cpp
     server.on("/control_led", HTTP_GET, [](AsyncWebServerRequest *request) {
         String room = request->getParam("room")->value();
         String light = request->getParam("light")->value();
         String action = request->getParam("action")->value();
         // Handle the action (on/off) for the light
     });
     ```

6. **Local and Remote Operation**:
   - The ESP32 can operate in both local network mode (communicating directly with devices on the local network) and remote mode (communicating with the Django server deployed on Heroku or another cloud platform).
   - It dynamically switches between these modes based on the IP address and connection type.

### Functions and Features Overview:

- **Wi-Fi Reconnection**: Automatically attempts to reconnect to the Wi-Fi network if the connection is lost.
- **HTTP Requests**: Sends HTTP requests to interact with the Django server, fetching device states and sending control commands.
- **Base64 Authentication**: Secures communication between the ESP32 and the Django backend by encoding credentials.
- **SPIFFS**: The ESP32 uses SPIFFS (SPI Flash File System) to store SSL certificates and other configuration files.
- **Debugging and Logging**: The ESP32 outputs detailed logs to both the serial monitor and an M5Core2 display for easy debugging.
- **Real-time Monitoring**: Provides real-time monitoring of device states and updates via the Django server.

### Planned Features:

- **WebSocket Communication**: Future updates will implement WebSockets for even faster real-time communication between the ESP32 and the Django backend.
- **Advanced Error Handling**: Improvements in error handling for network issues and server downtime.
- **Two-way Data Sync**: Synchronizing device states between the ESP32 and Django server more efficiently using WebSockets.

### ESP32 Codebase:

The ESP32 code is written using the **Arduino framework**, with libraries such as:
- `WiFi.h` for network connectivity.
- `HTTPClient.h` for handling HTTP requests.
- `ESPAsyncWebServer.h` for running the asynchronous web server.
- `ArduinoJson.h` for parsing and handling JSON data.
- `SPIFFS.h` for filesystem handling.
- `Update.h` for OTA firmware updates.

This component is crucial for providing real-time control over smart devices from the Django-based web interface.

