# ===========================================================================
#
# file     : gf_servo.py.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the servo class.
#
# ===========================================================================

from godafoss.gf_time import *
from godafoss.gf_tools import *
from godafoss.gf_fraction import *
from godafoss.gf_pins import *
from godafoss.gf_make_pins import *


# ===========================================================================

class servo:
    """
    drive a hobby servo

    $insert_image( "servo-sg90", 1, 400 )

    This class drives a hobby servo.
    A hobby servo requires pulses with a width of 1.0 ... 2.0 ms
    (exact range might vary by servo) each 20 ms (this interval is
    not very critical).

    $insert_image( "servo-pulse", 1, 300 )

    These pulse will cause the servo to turn its axle and horn to
    a specific angle.
    Typically, the angle varies between 0 and 180 degrees for pulses
    of 1.0 .. 2.0 ms.

    $insert_image( "servo-angles", 1, 400 )

    Provided that it is called often enough (either write() or poll())
    a servo object will provide a pulse of the appropriate width on the pin.
    The pulse will be delivered by the write() or poll() function call,
    so that call can take up to the maximum pulse length.

    A hobby servo needs a 5V supply, from which it can draw a significant
    current.
    One small (SG90, as shown in the picture) servo can safely
    be powered from a USB port.
    For more and/or larger servos, a separate 5V power suply is advisable.

    $insert_image( "servo-connector", 1, 400 )

    A hobby servo expects a 5V pulse, but in practice a 3.3V GPIO
    pin works fine. If the micro-controller seems to work unreliable
    when driving a servo, adding a large decoupling capacitor on the
    5V power supply (1000uF) can help.
    """

    def __init__(
        self,
        pin: [ int, pin_out, pin_in_out, pin_oc ],
        minimum: int = 1_000,
        maximum: int = 2_000,
        interval: int = 20_000
    ):
        self._pin = make_pin_out( pin )
        self._minimum = minimum
        self._maximum = maximum
        self._interval = interval
        self._next = 0
        self._value = None

    def poll( self ) -> None:
        """
        output servo pulse when it is time to do so

        Write a pulse to the servo (corresponding to the last
        fraction written) if it is time to do so.
        The default (bit banged) implementation requires
        poll() to be called regularly.
        An implementation that uses hardware probbaly doesn't need
        poll() calls.
        """

        t = ticks_us()
        if t >= self._next:
            self._pin.pulse(
                self._value.scaled( self._minimum, self._maximum ),
                0
            )
            self._next = t + self._interval

    def write( self, value: fraction ) -> None:
        """
        set servo setpoint

        Write the fraction to the servo as setpoint,
        which causes the corresponding servo pulse to be output the servo
        whenever it is time to do so.

        The default implementation requires write() or poll()
        to be called regularly to create the servo pulses.
        """

        self._value = value
        self.poll()

    def demo( self, steps = 100, iterations = None ) -> None:
        """servo demo"""

        print( "servo demo" )
        for dummy in repeater( iterations ):
            for v in range( 0, steps ):
                self.write( fraction( v, steps ) )
                self.poll()
                sleep_us( self._interval + 1_000 )
            for v in range( steps, 0, -1 ):
                self.write( fraction( v, steps ) )
                self.poll()
                sleep_us( self._interval + 1_000 )
