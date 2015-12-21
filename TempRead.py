#!/usr/bin/env python

import random
import time

def readTemp(): #program does nothing as written
    return  random.uniform (1,10)



import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='temp_queue', durable=True)

while True: 
    
    temp = readTemp ()
    message = {}

    message ['temp'] = str(temp)
    message ['time'] = str(time.time())
    message ['sensor'] = "sensorID"
    message ['type'] = "temperature"

    channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=repr(message),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
    print " [x] Sent %r" % (message,)
    time.sleep (10)

connection.close()

def readTemp(): #program does nothing as written
    return  random.random (1,10)

