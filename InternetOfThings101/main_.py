'''
Created on 23/04/2016

@author: MARIANO
'''
#!/usr/bin/python

import paho.mqtt.client as paho
import psutil
import signal
import sys
import time
import socket
import fcntl
import struct
import pyupm_i2clcd as lcd
from threading import Thread
from random import randint



Lcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

def toLCD(msg, r, g, b):
    Lcd.setCursor(0,0)
    Lcd.write('               ')
    Lcd.setColor(r, g, b)
    Lcd.setCursor(0,0)
    Lcd.write(msg)
    time.sleep(3)

    
    
def LCD2(msg1, msg2, r, g, b):
    Lcd.setCursor(0,0)
    Lcd.setColor(r, g, b)
    Lcd.write('                ')
    Lcd.setCursor(0,0)
    Lcd.write(msg1)
    Lcd.setCursor(1,0)
    Lcd.write('                ')
    Lcd.setCursor(1,0)
    Lcd.write(msg2)
    time.sleep(1)

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

def interruptHandler(signal, frame):
    sys.exit(0)

def on_publish(mosq, obj, msg):
    pass

def dataNetwork():
    netdata = psutil.net_io_counters()
    return netdata.packets_sent + netdata.packets_recv

def dataNetworkHandler():
    idDevice = getHwAddr('wlan0')
    mqttclient = paho.Client()
    mqttclient.on_publish = on_publish
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    while True:
        packets = dataNetwork()
        message =  str(packets)
	lcdMessage = "["+message+"]PacketsIO"
        print idDevice +" ["+message+"]"
        mqttclient.publish("IoT101/Network", message)
        LCD2( idDevice, lcdMessage,  randint(0,255), randint(0,255), randint(0,255))
	time.sleep(1)

def on_message(mosq, obj, msg):
    print "MQTT dataMessageHandler %s %s" % (msg.topic, msg.payload)

def dataMessageHandler():
    mqttclient = paho.Client()
    mqttclient.on_message = on_message
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    mqttclient.subscribe("IoT101/Message", 0)
    while mqttclient.loop() == 0:
        pass

if __name__ == '__main__':

    signal.signal(signal.SIGINT, interruptHandler)

    threadx = Thread(target=dataNetworkHandler)
    threadx.start()

    threadx = Thread(target=dataMessageHandler)
    threadx.start()

    while True:
	idDevice = getHwAddr('wlan0')
        print "Hello Internet of Things 101"
        LCD2("mantiniok@edison",idDevice,  randint(0,255), randint(0,255), randint(0,255))
        time.sleep(4)


# End of File
