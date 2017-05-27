#! /bin/env python
from pylms.server import Server
from pylms.player import Player
import paho.mqtt.client as mqtt
import time

# lists
mac = []
knownmac = [("00e04d010ed0","kitchen"),("b827ebf58086","server"),("e84e0624bd7d","bathroom"),("48022a6bcbc5","spareroom")]
subtopic = []
plobj = []
datalist = []

# mqtt parameters
mqttBroker = "aclosehas.onodo.co.uk"
mqttPort = 1883
base = "lms/"
topicGrp = base + "#"

#lms parmeters
lmsServer = "m2pserver"
lmsPort = 9090

# mqtt callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topicGrp)
    
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# start mqtt
cl = mqtt.Client()
cl.on_connect = on_connect
cl.on_message = on_message

cl.connect(mqttBroker, mqttPort)
cl.loop_start()

# discover LMS data
lms = Server(hostname=lmsServer, port=lmsPort)
lms.connect()
pl = lms.get_players()
numpl = len(pl)
print(str(numpl)+" players.")

for x in range(0,numpl):
    mac.append(x)
    subtopic.append(x)
    plobj.append(x)
    datalist.append(x)
    t=str(pl[x])
    #print(t)
    mac[x] = t[8:10]+t[11:13]+t[14:16]+t[17:19]+t[20:22]+t[23:25]
    subtopic[x]=str(mac[x])[6:]
    #print mac[x]
    #print t[8:25]
    for y in range(0,len(knownmac)):
        if (mac[x]==knownmac[y][0]):
            subtopic[x] = knownmac[y][1]
    #print subtopic[x]
    
    plobj[x] = lms.get_player(t[8:25])
    print(plobj[x].get_name())
    datalist[x]=(["get_name",plobj[x].get_name()],["get_track_artist","none"],["get_track_title","none"])

for x in range(0,numpl):
    print(str(pl[x])+" Topic: lms/"+subtopic[x])
    

while True:
    
    print("looping...")
    for x in range(0,numpl):
        for y in range(1,3):
            last = datalist[x][y][1]
            new = getattr(plobj[x], datalist[x][y][0])()
            if (new != last):
                datalist[x][y][1] = new
                print(datalist[x][0][1]+": "+new)
                cl.publish(base+subtopic[x]+"/"+datalist[x][y][0][4:], datalist[x][y][1], 2, True)
    time.sleep(60)
