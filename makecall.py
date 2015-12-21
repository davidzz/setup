import shlex
import os
from subprocess import call
call(["ls", "-l"])

command = "mosquitto_pub --cafile rootCA.pem --cert cert.pem --key privateKey.pem -h A3TNLWZ1LLGHU0.iot.us-east-1.amazonaws.com -p 8883 -q 1 -d -t topic/test2 -i clientid2 -m \"{\\\"msg\\\" : \\\"Happy hungry\\\"}\""
#\"{\"key2\" : \"Hello2, World\"}\""

os.system (command)

