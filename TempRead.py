#!/usr/bin/env python

import random

def readTemp(): #program does nothing as written
    return  random.uniform (1,10)



import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='temp_queue', durable=True)

temp = readTemp ()

message = "Temp of " + str(temp) + "added." 
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print " [x] Sent %r" % (message,)
connection.close()

def readTemp(): #program does nothing as written
    return  random.random (1,10)

