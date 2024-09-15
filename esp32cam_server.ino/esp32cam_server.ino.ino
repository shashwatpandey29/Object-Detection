#include <WebServer.h>   // Include the WebServer library for handling HTTP requests
#include <WiFi.h>        // Include the WiFi library to connect to the network
#include <esp32cam.h>    // Include the ESP32-CAM library for camera functionality

// Replace with your WiFi credentials
const char* WIFI_SSID = "your_SSID";    // WiFi SSID
const char* WIFI_PASS = "your_PASSWORD"; // WiFi password

WebServer server(80); // Create a WebServer object that listens on port 80

// Define resolutions for the camera
static auto loRes = esp32cam::Resolution::find(320, 240);   // Low resolution
static auto midRes = esp32cam::Resolution::find(350, 530);  // Medium resolution
static auto hiRes = esp32cam::Resolution::find(800, 600);   // High resolution

// Function to serve JPEG images from the camera
void serveJpg() {
  auto frame = esp32cam::capture(); // Capture a frame from the camera
  if (frame == nullptr) {
    Serial.println("CAPTURE FAIL"); // Print error if capture fails
    server.send(503, "", "");       // Send HTTP 503 Service Unavailable
    return;
  }
  Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
                static_cast<int>(frame->size())); // Print capture details

  server.setContentLength(frame->size()); // Set the content length of the HTTP response
  server.send(200, "image/jpeg");         // Send HTTP 200 OK with JPEG content type
  WiFiClient client = server.client();    // Get the client connection
  frame->writeTo(client);                 // Send the frame data to the client
}

// Handlers for different image resolutions
void handleJpgLo() {
  if (!esp32cam::Camera.changeResolution(loRes)) {
    Serial.println("SET-LO-RES FAIL"); // Print error if resolution change fails
  }
  serveJpg(); // Serve the JPEG image
}

void handleJpgHi() {
  if (!esp32cam::Camera.changeResolution(hiRes)) {
    Serial.println("SET-HI-RES FAIL"); // Print error if resolution change fails
  }
  serveJpg(); // Serve the JPEG image
}

void handleJpgMid() {
  if (!esp32cam::Camera.changeResolution(midRes)) {
    Serial.println("SET-MID-RES FAIL"); // Print error if resolution change fails
  }
  serveJpg(); // Serve the JPEG image
}

void setup() {
  Serial.begin(115200);   // Start serial communication at 115200 baud
  Serial.println();       // Print a newline for readability

  {
    using namespace esp32cam; // Use the esp32cam namespace
    Config cfg;              // Create a configuration object for the camera
    cfg.setPins(pins::AiThinker); // Set the pin configuration for the AiThinker module
    cfg.setResolution(hiRes);     // Set the initial resolution to high resolution
    cfg.setBufferCount(2);       // Set the number of image buffers
    cfg.setJpeg(80);             // Set JPEG compression quality

    bool ok = Camera.begin(cfg); // Initialize the camera with the configuration
    Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL"); // Print initialization status
  }

  WiFi.persistent(false); // Disable WiFi persistence
  WiFi.mode(WIFI_STA);    // Set WiFi mode to Station
  WiFi.begin(WIFI_SSID, WIFI_PASS); // Connect to the WiFi network
  while (WiFi.status() != WL_CONNECTED) { // Wait for connection
    delay(500); // Wait for 500 ms
  }

  Serial.print("http://");             // Print the base URL
  Serial.println(WiFi.localIP());      // Print the local IP address of the ESP32
  Serial.println("  /cam-lo.jpg");     // Print URL for low resolution
  Serial.println("  /cam-hi.jpg");     // Print URL for high resolution
  Serial.println("  /cam-mid.jpg");    // Print URL for medium resolution

  // Set up HTTP request handlers
  server.on("/cam-lo.jpg", handleJpgLo); // Handler for low-resolution images
  server.on("/cam-hi.jpg", handleJpgHi"); // Handler for high-resolution images
  server.on("/cam-mid.jpg", handleJpgMid"); // Handler for medium-resolution images

  server.begin(); // Start the HTTP server
}

void loop() {
  server.handleClient(); // Handle incoming client requests
}
