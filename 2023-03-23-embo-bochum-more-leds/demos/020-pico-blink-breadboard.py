from machine import Pin
from time import sleep_us

led = Pin( 28, Pin.OUT )
while True:
    led.value( 1 )
    sleep_us( 500_000 )    
    led.value( 0 )
    sleep_us( 500_000 )