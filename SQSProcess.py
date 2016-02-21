#!/usr/bin/env python

import sys, os, ConfigParser
import boto3, ast
import MySQLdb

def connectToDB ():

    print "1"
    Config = ConfigParser.ConfigParser()
    Config.read (os.path.expanduser('~/keys/rds_config.ini'))

    print "3"
    cnx= {'host': Config.get ('RDS', 'endpoint'),
      'username': Config.get ('RDS', 'username'),
      'password': Config.get ('RDS', 'password'),
      'db': Config.get ('RDS', 'db')}

    print "cnx: " + str(cnx)
    db = MySQLdb.connect(cnx['host'],cnx['username'],cnx['password'], cnx['db'], port=3306)
    
    return db


def createTable ():
    print "Create the table"
    db = connectToDB()
    try:
        cursor = db.cursor()
        sqlStatement = "CREATE TABLE sensorreads (sensor varchar(20), reading real, readingtype varchar(20), readattime TIMESTAMP)"
        cursor.execute (sqlStatement)
        print "Table created"
    except MySQLdb.OperationalError:
        print "Table already exists"
    except all:
        print "Error happened"
        sys.exit (1);
            
def invalidArgs ():
    print "Invalid arguments. Usage: SQSProcess (create | drop | process)"

def dropTable ():
    print "Dropping the table"


    db = connectToDB()
    try:
        cursor = db.cursor()
        sqlStatement = "drop TABLE sensorreads;"
        cursor.execute (sqlStatement)
        db.commit()
        print "Table dropped"
    except MySQLdb.OperationalError:
        print "Table doesn't exist"
    except all:
        print "Error happened"
        sys.exit (1);

def processSQS ():
    print "Processing the SQS"
    sqs = boto3.resource('sqs')
    client = boto3.client('sqs')
    queue = sqs.get_queue_by_name(QueueName='SensorQ')
    
    response = client.get_queue_attributes (QueueUrl='https://sqs.us-east-1.amazonaws.com/413241060769/SensorQ', AttributeNames=['ApproximateNumberOfMessages'])

    queueDepth = int(response['Attributes']['ApproximateNumberOfMessages'])

    print "Preconnect"
    db = connectToDB()
    print "Connect done"
 
    #while queueDepth > 0:
    while True:
        print "Queue Depth: " + str(queueDepth)

        print "inwhile"
        for message in queue.receive_messages ():
            messageDict = ast.literal_eval (message.body)
            print ("messageDict: " + str(messageDict))

            try: 
                cursor = db.cursor ()
                sqlStatement = "INSERT INTO  sensorreads (sensor, reading, readingtype, readattime) VALUES ('{0}',{1},'{2}','{3}')".format(messageDict["sensor"],messageDict["reading"], messageDict["type"], messageDict["time"])
                print "SQL: " + sqlStatement
                output = cursor.execute (sqlStatement)
                print "output: " + str(output)
                print "attempting commit"
                db.commit()
                print "committed"
            except all:
                print "Error happened"
                sys.exit (1); 


        message.delete()
        
        response = client.get_queue_attributes (QueueUrl='https://sqs.us-east-1.amazonaws.com/413241060769/SensorQ', AttributeNames=['ApproximateNumberOfMessages'])

        queueDepth = int(response['Attributes']['ApproximateNumberOfMessages'])
        print "Queue Depth: " + str(queueDepth)    


if len(sys.argv) != 2:
    invalidArgs ()
elif (sys.argv[1]) == "create":
    createTable()
elif (sys.argv[1]) == "drop":
    dropTable()
elif (sys.argv[1]) == "process":
    processSQS()
elif (sys.argv[1]) == "test":
    testSQS()
else:
    invalidArgs()


