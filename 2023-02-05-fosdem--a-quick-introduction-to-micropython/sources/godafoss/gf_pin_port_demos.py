# ===========================================================================
#
# file     : gf_pin_port_demos.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the pin and port demo functions.
#
# ===========================================================================

from godafoss.gf_time import *
from godafoss.gf_tools import *
from godafoss.gf_pins import *
from godafoss.gf_make_pins import *
from godafoss.gf_ports import *


# ===========================================================================

def blink(
    pin: [ int, pin_out, pin_in_out, pin_oc ],
    high_time = 500_000,
    low_time = None,
    iterations = None
) -> None:
    """
    blink on the pin
    
    Blink on the pin with high_time and low_time
    (defaults to high_time) for the specified number of iterations
    (defaults to infinite).
    
    Times are in us (microseconds).
    """

    p = make_pin_out( pin )
    n = 0
    for _ in repeater( iterations ):
        p.pulse(
            high_time,
            first_not_none( low_time, high_time )
        )


# ===========================================================================

def walk(
    port,
    interval = 100_000,
    iterations = None
) -> None:
    """
    walking display
    
    Walk on the port with the specified interval
    for the specified number of iterations
    (defaults to infinite).
    
    Times are in us (microseconds).    
    """    

    p = port.as_port_out()
    for _ in repeater( iterations ):
        for n in range( p.nr_of_pins ):
            p.write( 0b1 << n )
            sleep_us( interval )


# ===========================================================================

def kitt(
    port,
    interval = 100_000,
    iterations = None
) -> None:
    """   
    kitt display
    
    Show the Kitt on the port with the specified interval
    for the specified number of iterations
    (defaults to infinite).
    
    Times are in us (microseconds).    
    """

    p = port.as_port_out()
    for _ in repeater( iterations ):
        for n in range( p.nr_of_pins ):
            p.write( 0b1 << n )
            sleep_us( interval )
        for n in range( p.nr_of_pins - 2, 0, -1 ):
            p.write( 0b1 << n )
            sleep_us( interval )

# ===========================================================================
