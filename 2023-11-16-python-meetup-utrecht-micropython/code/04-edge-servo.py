from machine import Pin
from time import sleep_us
    
def pulse( pin, p, total = 20_000 ):
    pin.value( 1 )
    sleep_us( p )    
    pin.value( 0 )
    sleep_us( total - p )    
    
def wave( pin ):
    for i in range( 1000, 2000, 10 ):
        pulse( pin, i )
    for i in range( 2000, 1000, -10 ):
        pulse( pin, i )

print( "servo demo" )
servo = Pin( 26, Pin.OUT )
while True:
    wave( servo )