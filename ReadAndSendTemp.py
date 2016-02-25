#!/usr/bin/env python

import random
import time
import Adafruit_DHT
import pika
import sys
import ast
import os
def sendIoTMessage (message):

    command = "mosquitto_pub --cafile /home/pi/setup/rootCA.pem --cert /home/pi/setup/cert.pem --key /home/pi/setup/privateKey.pem -h A3TNLWZ1LLGHU0.iot.us-east-1.amazonaws.com -p 8883 -q 1 -d -t topic/test3 -i clientid2 -m "

    print "Parse this: " + str(message)
    print message
#    theDict = ast.literal_eval (message)

    theDict = message
    msgStr = "\"{"
    count = 0
    for key in theDict:
        if count > 0:
            msgStr = msgStr + ", "

        msgStr = msgStr + "\\\"" + str(key) + "\\\" : \\\"" + theDict[key] + "\\\""
        count = count + 1

    msgStr = msgStr + "}\""

    command = command + msgStr
    print command
    os.system (command)


sensor = Adafruit_DHT.DHT11
pin = 23
os.environ['TZ'] = 'US/Eastern'
time.tzset()

def readTemp(): #program does nothing as written
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	print "temp in C: " + str(temperature)
	return (float(temperature)*(1.8))+32;


#connection = pika.BlockingConnection(pika.ConnectionParameters(
#        host='localhost'))
#channel = connection.channel()

#channel.queue_declare(queue='temp_queue', durable=True)

try:
	temp = readTemp ()
	message = {}

	message ['reading'] = str(temp)
	message ['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
	message ['sensor'] = "RPI"
	message ['type'] = "temperature"

	sendIoTMessage (message)
except:
	print "Read error"
