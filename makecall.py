import shlex
import os
from subprocess import call
call(["ls", "-l"])

d = {}
d['temp'] = "451"
d['msg'] = "yoyoyo"

print d

command = "mosquitto_pub --cafile rootCA.pem --cert cert.pem --key privateKey.pem -h A3TNLWZ1LLGHU0.iot.us-east-1.amazonaws.com -p 8883 -q 1 -d -t topic/test2 -i clientid2 -m "

command = command + "\"{\\\"msg\\\" : \\\"Happy hungry\\\", \\\"temperature\\\" : \\\"452\\\"}\""

os.system (command)

