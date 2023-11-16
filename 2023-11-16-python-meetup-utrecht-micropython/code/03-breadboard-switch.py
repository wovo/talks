from machine import Pin
from time import sleep_us

led = Pin( 16, Pin.OUT )
switch = Pin( 15, Pin.IN )
last = False
while True:
    new = not switch.value()
    if new and not last:
        led.value( not led.value() )
    last = new
    sleep_us( 50_000 )