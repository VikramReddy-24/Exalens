#!/bin/bash

echo "Command 1"
python main.py
echo "Command 3"
python mosquitto_pub.py
echo "Command 3"
python mosquitto_sub.py