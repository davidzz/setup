#!/usr/bin/env python

import sys
import boto3, ast

def createTable ():
    print "Create the table"

def invalidArgs ():
    print "Invalid arguments. Usage: SQSProcess (create | drop | process)"

def dropTable ():
    print "Dropping the table"

def processSQS ():
    print "Processing the SQS"
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='SensorQ')
   
    for message in queue.receive_messages ():
        messageDict = ast.literal_eval (message.body)
        print messageDict
 

    



if len(sys.argv) != 2:
    invalidArgs ()
elif (sys.argv[1]) == "create":
    createTable()
elif (sys.argv[1]) == "drop":
    dropTable()
elif (sys.argv[1]) == "process":
    processSQS()
else:
    invalidArgs()

import MySQLdb

cnx= {'host': 'dbname.xxxxxxxxxxxx.us-west-1.rds.amazonaws.com',
  'username': 'username',
  'password': 'password',
  'db': 'dbname'}

db = MySQLdb.connect(cnx['host'],cnx['username'],cnx['password'], cnx['db'])

