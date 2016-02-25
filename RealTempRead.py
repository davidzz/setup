#!/usr/bin/env python

import random
import time
import Adafruit_DHT
import pika
import sys


sensor = Adafruit_DHT.DHT11
pin = 23

def readTemp(): #program does nothing as written
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	return temperature*(9/5)+32;


import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='temp_queue', durable=True)

while True: 
    
    temp = readTemp ()
    message = {}

    message ['reading'] = str(temp)
    message ['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
    message ['sensor'] = "RPI"
    message ['type'] = "temperature"

    channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=repr(message),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
    print " [x] Sent %r" % (message,)
    time.sleep (1)

connection.close()

def readTemp(): #program does nothing as written
    return  random.random (1,10)

