import paho.mqtt.client as mqtt
from datetime import datetime
from pymongo import MongoClient
import json
import redis


# Connect to the Redis server
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

# MongoDB connection parameters
host = "mongodb://mongodb:27017/"
port = 27017
username = "myusername"
password = "mypassword"

# Create a MongoClient with authentication
db_client = MongoClient(host, username=username, password=password)




def on_message(client, userdata, message):

    print(f"Received message: {message.payload.decode()} on topic {message.topic}")

    list_key = 'latest_temperature_data' if message.topic == 'sensors/temperature' else 'latest_humidity_data'
    redis_client.lpush(list_key, message.payload.decode())

    Received_message=json.loads(message.payload.decode())

    max_list_size = 10

    # Check the List size and remove the oldest entry if needed
    if redis_client.llen(list_key) > max_list_size:
        print(redis_client.llen(list_key))
        redis_client.rpop(list_key)

    # Date String in dd/mm/yyyy HH:MM:SS format
    dt_string = Received_message["timestamp"]

    # Convert string to datetime object
    dt_object = datetime.strptime(dt_string, "%d-%m-%Y %H:%M:%S")
    print(dt_object)

   
    Received_message['topic']=message.topic
    Received_message["timestamp"]=dt_object
    print(Received_message)
    db = db_client["sensors"]
    collection = db["sensor_readings"]
    result = collection.insert_one(Received_message)    


client = mqtt.Client()
client.on_message = on_message

broker_address = "mosquitto"  # Replace with your broker's address
broker_port = 1883  # Replace with your broker's port
client.connect(broker_address, broker_port)

client.subscribe('sensors/humidity')
client.subscribe('sensors/temperature')
client.loop_forever()
