# ===========================================================================
#
# file     : gf_temperature.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the temperature class.
#
# ===========================================================================

from micropython import const

from godafoss.gf_tools import *


# ===========================================================================

class temperature( immutable ):
    """
    a temperature

    :param temp: int | float
        the temperaturee, interpreted according to the scale

    :param scale: int
        the scale

    This class holds a temperature as a float.
    When constructing a temperature, or retrieveing value
    from a temperature object,
    the scale (temperature.scale.Celcius, temperature.scale.Farenheit
    or temperature.scale.Kelvin) must be specified.

    $macro_insert immutable

    examples::
    $insert_example( "test_temperature.py", "temperature examples", 1 )
    """

    class scale:
        Kelvin     = const( 0 )
        Celcius    = const( 1 )
        Farenheit  = const( 2 )
        _names = ( "K", "C", "F" )

    def __init__(
        self,
        temp: int | float,
        scale: int
    ) -> None:
        self._scale = scale

        if self._scale == self.scale.Kelvin:
            self._kelvin = float( temp )

        elif self._scale == self.scale.Celcius:
            self._kelvin = temp + 273.15

        elif self._scale == self.scale.Farenheit:
            self._kelvin = ( temp + 459.67 ) * 5 / 9

        else:
            raise ValueError

        immutable.__init__( self )

    # =======================================================================

    def value(
        self,
        scale: int
    ) -> float:
        """
        the temperature in the specified scale

        :param scale: int
            the scale

        :result: float
            the temperature, excressed in the specified scale

        The temperature is return according to the specified scale,
        which must be one of temperature.scale.Celcius,
        temperature.scale.Farenheit or temperature.scale.Kelvin.

        This method returns the temperature in the requested scale.
        """

        if scale == self.scale.Kelvin:
            return self._kelvin

        elif scale == self.scale.Celcius:
            return self._kelvin - 273.15

        elif scale == self.scale.Farenheit:
            return 1.8 * ( self._kelvin - 273.15) + 32

        else:
            raise ValueError

    # =======================================================================

    def __repr__( self ) -> str:
        return "%f%s" % (
            self.value( self._scale ),
            self.scale._names[ self._scale ]
        )
    # =======================================================================

# ===========================================================================
