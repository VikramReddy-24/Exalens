from fastapi import FastAPI
import uvicorn
import redis
import json
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pydantic import BaseModel

from datetime import datetime

app = FastAPI()

# Connect to the Redis server
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

# MongoDB connection parameters
host = "mongodb://mongodb:27017/"
port = 27017
username = "myusername"
password = "mypassword"



@app.get("/latest/{sensor}")
def latest(sensor):
    
    try:
        if sensor == 'temperature':
          list_key = 'latest_temperature_data'
        elif sensor == 'humidity':
          list_key = 'latest_humidity_data'  
        else:
          return JSONResponse(content="URL Not Found",status_code=404)  
        data=redis_client.lrange(list_key,0,10)
        print("latest_data:-",data)
        result=[]
        for i in data:
           result.append(json.loads(str(i, 'UTF-8')))

        print(result)   
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
       print(e)
       print("Exception Handling Error")
       return JSONResponse(content="Internal Server Error", status_code=500)


class Item(BaseModel):
        from_date: str
        to_date: str
        from_time:str
        to_time:str

@app.post("/readings")
def readings(item: Item):
    try:
        from_date = item.from_date
        to_date = item.to_date
        from_time = item.from_time
        to_time = item.to_time

        # Create a MongoClient with authentication
        db_client = MongoClient(host, username=username, password=password)  
        db = db_client["sensors"]
        collection = db["sensor_readings"]
        print(from_date.split("-")[0])
        start_date = datetime(int(from_date.split("-")[0]), int(from_date.split("-")[1]), int(from_date.split("-")[2]),int(from_time.split(":")[0]),int(from_time.split(":")[1]))
        end_date = datetime(int(to_date.split("-")[0]), int(to_date.split("-")[1]), int(to_date.split("-")[2]),int(to_time.split(":")[0]),int(to_time.split(":")[1]))
       
       
        query = {"timestamp": {"$gte": start_date, "$lte": end_date}}
        print(query)
        result = collection.find(query)
        data=[]
        for document in result:
          del document['_id']
          data.append(document)
        
        return data
    
    except Exception as e:
      print("Exception:",e)
      print("Exception Handling Error")
      return JSONResponse(content="Internal Server Error", status_code=500)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
