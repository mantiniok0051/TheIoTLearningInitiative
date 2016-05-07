'''
Created on 02/05/2016

@author: MARIANO
'''
import time
import pyupm_grove as grove
import pyupm_ttp223 as ttp223
import dweepy

# Create the button object using GPIO pin 2
button = grove.GroveButton(2)
# Create the TTP223 touch sensor object using GPIO pin 3
touch = ttp223.TTP223(3)
# Create the light sensor object using AIO pin 0
light = grove.GroveLight(0)
# New knob on AIO pin 1
knob = grove.GroveRotary(1)
# Create the temperature sensor object using AIO pin 2
temp = grove.GroveTemp(2)


while 1:
    print ' Button ------------------ ', button.value()
    if button.value():
        buttonBool = True
    else: 
        buttonBool = False
    if touch.isPressed():
        print ' Touch ------------------- ', True
        touchBool = True
    else: 
        print ' Touch ------------------- ', False
        touchBool = False
    print ' Light ------------------- ',light.value()
    print ' Celsius ----------------- ',temp.value()
    print ' Pot --------------------- ',knob.abs_value()
    json= {
        'Button':buttonBool,
        'Touch':touchBool,
        'Light' : light.value(), 
        'Celsius' : temp.value(), 
        'Pot' : knob.abs_value()
          }
    dweepy.dweet_for('mantiniok.edison.intel', json)
    time.sleep(1)

# Delete the button object
del button
# Delete the touch sensor object
del touch
# Delete the light sensor object
del light
# Delete the temperature sensor object
del temp
