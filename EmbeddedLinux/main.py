'''
Created on 23/04/2016
@author: MARIANO
'''
#!/usr/bin/python

import paho.mqtt.client as paho
import psutil
import pywapi
import signal
import sys
import time
import socket
import fcntl
import struct
import pyupm_i2clcd as lcd
from threading import Thread
from random import randint
import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure


username = 'mantiniok0051'
api_key = 'yy89qc5xtd'
stream_token = 'dgq444duqa'

Lcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
    
def toLCD(msg1, msg2, r, g, b):
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
        mqttmessage =  idDevice +" ["+message+"]" 
        print idDevice +" ["+message+"]"
        mqttclient.publish("IoT101/Network", mqttmessage)
        toLCD( idDevice, lcdMessage,  randint(0,255), randint(0,255), randint(0,255))
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

def dataWeatherHandler():
    weather = pywapi.get_weather_from_weather_com('MXJO0043', 'metric')
    message = "Weather Report in " + weather['location']['name']
    message = message + ", Temperature " + weather['current_conditions']['temperature'] + " C"
    message = message + ", Atmospheric Pressure " + weather['current_conditions']['barometer']['reading'][:-3] + " mbar"
    print message

def dataPlotly():
    return dataNetwork()

def dataPlotlyHandler():

    py.sign_in(username, api_key)

    trace1 = Scatter(
        x=[],
        y=[],
        stream=dict(
            token=stream_token,
            maxpoints=200
        )
    )

    layout = Layout(
        title='Hello Internet of Things 101 Data'
    )

    fig = Figure(data=[trace1], layout=layout)

    print py.plot(fig, filename='Hello Internet of Things 101 Plotly')

    i = 0
    stream = py.Stream(stream_token)
    stream.open()

    while True:
        stream_data = dataPlotly()
        stream.write({'x': i, 'y': stream_data})
        i += 1
        time.sleep(0.25)    

if __name__ == '__main__':

    dataWeatherHandler()
    signal.signal(signal.SIGINT, interruptHandler)

    threadx = Thread(target=dataNetworkHandler)
    threadx.start()

    threadx = Thread(target=dataMessageHandler)
    threadx.start()


    while True:
        idDevice = getHwAddr('wlan0')
        print "Hello Internet of Things 101"
        toLCD("mantiniok@edison",idDevice,  randint(0,255), randint(0,255), randint(0,255))
        time.sleep(5)
        
        


# End of File

python -c "import plotly; plotly.tools.set_credentials_file(username='mantiniok0051', api_key='yy89qc5xtd', stream_ids=['dgq444duqa])"

   {
    "username":"mantiniok0051",
    "stream_ids": ["dgq444duqa"],
    "api_key": "yy89qc5xtd",
    "proxy_username": "",
    "proxy_password": ""
    }

    https://github.com/LuisEnVilla/BoardEdison/blob/master/sensor.py
    http://statusorel.ru/technology/boardedison-en-freeboard-con-dweet.html