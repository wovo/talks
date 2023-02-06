# ===========================================================================
#
# file     : gf_sr04.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the sr04 distance sensor class.
#
# ===========================================================================

from godafoss.gf_time import *
from godafoss.gf_tools import *
from godafoss.gf_pins import *
from godafoss.gf_make_pins import *


# ===========================================================================

class sr04:
    """
    SR04 ultrasonic distance sensor

    $insert_image( "sr04-module", 1, 300 )

    This classs interfaces to an sr04 ultrasonic distance sensor.

    An sr04 measures distance by outputting a short burst
    of utrasonic sound, and listening for an echo caused
    by the reflection of the sound by an object.
    An sr04 requires 5V power.

    $insert_image( "sr04-timing", 1, 400 )

    A measuremment cycle starts with the micro-controller
    putting a short (10us) pulse on the trigger pin.
    This causes the sr04 to output the ultrasonic sound burst
    and listen to the echo.
    The sr04 outputs a pulse that starts with the sound burst,
    and ends with the receiving of the echo.
    The duration of this pulse is proportional to the distance.
    """

    def __init__(
        self,
        trigger: [ int, pin_out, pin_in_out, pin_oc ],
        echo: [ int, pin_in, pin_in_out, pin_oc ],
        speed_of_sound: int = 343,
        minimum_waiting: int = 100_000,
        timeout: int = 100_000
    ):
        """
        sr04 driver constructor

        An sr04 requires a trigger pin (output) and an echo pin (input).
        The trigger input theoretically requires a 5V pulse,
        but in practice a 3.3V works fine.
        The echo output is a 5V pulse.
        Most micro-controller input pins are not 5V compatible,
        so a level shift is needed.
        In practice a simple 1k / 2k2 resistor voltage divider
        works fine.

        To calculate the distance form the echo,
        the speed of sound in air is required.
        The default is 343 m/s, which is
        the value for 20 degrees and standard atmospheric pressure.
        This is probably OK for all practical use.

        After a measurement a minumum waiting interval is required,
        otherwise the previous echo could be picked up.
        The default minimum waiting interval is 100 ms.

        When no pulse is received from the sr04 within the timeout
        a measurement is assumed to have failed.
        The default timeput is 100 ms.
        """

        self._trigger = make_pin_out( trigger )
        self._echo = make_pin_in( echo )
        self.speed_of_sound = speed_of_sound
        self.minimum_waiting = minimum_waiting
        self.timeout = timeout
        self._timeout = 0
        self._result = None
        self._trigger.write( 0 )

    def read(
            self,
            default: int | None = None
        ) -> int | None:

        """
        the distance im mm as integer

        This function measures and returns the distance in mm,
        or the default (by default, None) specied by the caller
        if no valid measurement could be made.

        If less than mimimum waiting interval has expired since
        the previous measurement, no new measurement is taken
        and the previous result is returned.

        When the start or end of the measurement pulse is not seen within
        the timeout, the default value (by default: None) is returned.

        The measurement and waiting for the pulse (or the timeout)
        is done in the function, so a function call can take up to
        the timout time to return.

        Outputting the pulse and listening for the echo is
        done in the function call, so a call can take up to the
        timeout time to return.
        """

        if self._timeout > ticks_us():
            # print( 'too quick' )
            return self._result

        # don't attempt to measure again within the minimum interval
        self._timeout = ticks_us() + self.minimum_waiting

        # echo should be zero before trigger
        if self._echo.read():
            print( 'not zero' )
            return default

        # send 10us trigger
        self._trigger.pulse( 10, 0 )

        # wait for start of measurement pulse
        t1 = ticks_us()
        while not self._echo.read():
            t2 = ticks_us()
            if ( t2 - t1 ) > self.timeout:
                print( 'no start' )
                return default

        # wait for end of measurement pulse
        t1 = ticks_us()
        # print( "echo", self._echo.read() )
        while self._echo.read():
            t2 = ticks_us()
            if ( t2 - t1 ) > self.timeout:
                print( 'no end' )
                return default
        t2 = ticks_us()

        # print( "pulse=", t1, t2, t2 - t1 )
        self._result = (( t2 - t1 ) * self.speed_of_sound ) // ( 2 * 1_000 )
        # print( "res=", self._result )
        return self._result

    def demo( self, interval: int = 500_000, iterations = None ):
        """sr04 demo"""
        print( "sr04 ultrasonic distance sensor demo" )
        for _ in repeater( iterations ):
            # print( 'measure' )
            print( "%d mm" % self.read( default = 9999 ) )
            sleep_us( interval )


# ===========================================================================
