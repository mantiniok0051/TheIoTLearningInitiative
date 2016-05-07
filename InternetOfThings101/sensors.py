import time
import pyupm_grove as grove
import pyupm_ttp223 as ttp223

# Create the button object using GPIO pin 2 button
# Create the TTP223 touch sensor object using GPIO pin 3 touch
# Create the light sensor object using AIO pin 0 light
# New knob on AIO pin 1 knob
# Create the temperature sensor object using AIO pin 2 temp

button = grove.GroveButton(2)
touch  = ttp223.TTP223(3)
light  = grove.GroveLight(0)
knob   = grove.GroveRotary(1) 
temp   = grove.GroveTemp(2)

while True:

      print 'Button----------',button.value() 
      if touch.isPressed():
		print 'Touch------',True 
      else:
		print'Touch----------',False
      print 'Light-----------',light.value() 
      print 'Celcius---------', temp.value()
      print 'Pot-------------',knob.abs_value()

      time.sleep(1) 

del button
del touch
del light
del temp
