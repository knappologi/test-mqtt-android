# Imports for MQTT
import time
import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# Using decimal to round the value for lux :)
from decimal import Decimal

# Imports for sensor
import board
import busio
import adafruit_tsl2591
 
# Initialize the I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
 
# Initialize the sensor.
sensor = adafruit_tsl2591.TSL2591(i2c)


broker = "test.mosquitto.org"	# Broker 

pub_topic = "hellocutie0"       # send messages to this topic


############### MQTT section ##################

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
	if rc==0:
		print("Connection established. Code: "+str(rc))
	else:
		print("Connection failed. Code: " + str(rc))
		
def on_publish(client, userdata, mid):
    print("Published: " + str(mid))
	
def on_disconnect(client, userdata, rc):
	if rc != 0:
		print ("Unexpected disonnection. Code: ", str(rc))
	else:
		print("Disconnected. Code: " + str(rc))
	
def on_log(client, userdata, level, buf):		# Message is in buf
    print("MQTT Log: " + str(buf))

# Fetching sensor data:
def get_lux():
	lux = sensor.lux

	# Rounds the lux value to 3 decimals, and prints it
	lux_value = round(Decimal(lux), 3)
	print('Total light: {0} lux'.format(lux_value))
	return lux_value
	
	
# Connect functions for MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_log = on_log

# Connect to MQTT 
print("Attempting to connect to broker " + broker)
client.connect(broker, 1883, 60)
client.loop_start()

# Loop that publishes message
while True:
	data_to_send = get_lux()
	client.publish(pub_topic, str(data_to_send))
	time.sleep(4.0)	# Set delay
