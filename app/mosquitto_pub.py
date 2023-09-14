import paho.mqtt.client as mqtt
import random
from datetime import datetime
import time
import json

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed")

client = mqtt.Client()
client.on_connect = on_connect
print("client-:",client.is_connected)

broker_address = "mosquitto"  # Replace with your broker's address
broker_port = 1883  # Replace with your broker's port

repeat=1
client.connect(broker_address, broker_port)
client.loop_start()

while repeat>0: 
    current_datetime = datetime.now()
    print("current_date_time-:",current_datetime)
    current_time = current_datetime.date()
    print("Current Time:", current_time)
    formatted_time = current_time.strftime("%H:%M:%S")
    
    # current dateTime
    now = datetime.now()

    # convert to string
    formatted_time = now.strftime("%d-%m-%Y %H:%M:%S")
    print('DateTime String:', formatted_time)

    random_number = random.randint(1, 100)
    topic= 'sensors/temperature' 
    unique_sensor_id=100
    message = json.dumps( {"sensor_id": unique_sensor_id, "value": f"{random_number} c", "timestamp": formatted_time} )
    # message="Hello"
    print("message:",message)
    client.publish(topic, message)

    topic = 'sensors/humidity'
    random_number = random.randint(1, 1000)
    unique_sensor_id=200
    message = json.dumps({ "sensor_id": unique_sensor_id, "value": f"{random_number}", "timestamp": formatted_time })
    print("message:",message)
    client.publish(topic, message)

    time.sleep(10)

client.disconnect()
client.loop_stop()
