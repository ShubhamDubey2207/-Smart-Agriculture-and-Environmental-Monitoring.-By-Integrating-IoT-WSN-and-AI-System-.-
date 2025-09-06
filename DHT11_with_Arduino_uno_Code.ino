#include <DHT11.h>

/***
  Author: Giridhar Urkude

  Date: 31-Jan-2019
  (Last updated )

  ***************************************************************************************************************************************
  Summary:

 

  ****************************************************************************************************************************************


*/
#include <DHT11.h>

// Create an instance of the DHT11 class.
// - For Arduino: Connect the sensor to Digital I/O Pin A0.
// - For ESP32: Connect the sensor to pin GPIO2 or P2.
// - For ESP8266: Connect the sensor to GPIO2 or D4.
DHT11 dht11(A0);

void setup(){     // Setting up the baud-rate for the xbee communication.
  
    Serial.begin(9600);  // 9600 bit per second transmission rate (it should be same for all arduino devices).
    delay(1000);
    Serial.println("start");

}

void loop() {
    int temperature = 0;
    int humidity = 0;

    // Attempt to read the temperature and humidity values from the DHT11 sensor.
    int result = dht11.readTemperatureHumidity(temperature, humidity);

    // Check the results of the readings.
    // If the reading is successful, print the temperature and humidity values.
    // If there are errors, print the appropriate error messages.
    if (result == 0) {
        Serial.print("Temperature: ");
        Serial.print(temperature);
        Serial.print(" °C\tHumidity: ");
        Serial.print(humidity);
        Serial.println(" %");
    } else {
        // Print error message based on the error code.
        Serial.println(DHT11::getErrorString(result));
    }
    delay(2000);
}
