#!/usr/bin/env python
import pika
import time
import ast
import os

def sendIoTMessage (message):
    
    command = "mosquitto_pub --cafile rootCA.pem --cert cert.pem --key privateKey.pem -h A3TNLWZ1LLGHU0.iot.us-east-1.amazonaws.com -p 8883 -q 1 -d -t topic/test3 -i clientid2 -m "

    print "Parse this: " + message
    theDict = ast.literal_eval (message)
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

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    sendIoTMessage (body) 
    time.sleep( body.count('.') )
    print " [x] Done"
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()

