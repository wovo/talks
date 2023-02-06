# ===========================================================================
#
# file     : gf_gpio.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the gpio classes.
#
# ===========================================================================

import machine

from godafoss.gf_pins import *


# ===========================================================================

class gpio_in( pin_in ):
    """
    chip GPIO pin used as input

    :param pin_nr: (int)
        the chip pin number
    """

    # =======================================================================

    def __init__(
        self,
        pin_nr: int
    ) -> None:
        self._pin = machine.Pin( pin_nr, machine.Pin.IN )
        pin_in.__init__( self )

    # =======================================================================

    def read( self ) -> bool:
        """
        the pin value

        :result: (bool)
            the pin value (level)
        """
        return self._pin.value()

    # =======================================================================

# ===========================================================================


class gpio_out( pin_out ):
    """
    chip GPIO pin used as output

    :param pin_nr: (int)
        the chip pin number
    """

    # =======================================================================

    def __init__(
        self,
        pin_nr: int
    ) -> None:
        self._pin = machine.Pin( pin_nr, machine.Pin.OUT )
        pin_out.__init__( self )

    # =======================================================================

    def write(
        self,
        value: bool
    ) -> None:
        """
        set the pin value

        :param value: (bool)
            the new pin value (level)
        """
        self._pin.value( value )

    # =======================================================================

# ===========================================================================


class gpio_in_out( pin_in_out ):
    """
    chip GPIO pin used as input output

    :param pin_nr: (int)
        the chip pin number
    """

    # =======================================================================

    def __init__(
        self,
        pin_nr: int
    ) -> None:
        self._pin = machine.Pin( pin_nr, machine.Pin.IN )
        self._pin_nr = pin_nr
        pin_in_out.__init__( self )

    # =======================================================================

    def direction_set_input( self ) -> None:
        """
        make the pin an input
        """
        self._pin.init( machine.Pin.IN )

    # =======================================================================

    def direction_set_output( self ) -> None:
        """
        make the pin an output
        """
        self._pin.init( machine.Pin.OUT )

    # =======================================================================

    def write(
        self,
        value: bool
    ) -> None:
        """
        set the pin value

        :param value: (bool)
            the new pin value (level)
        """
        self._pin.value( value )

    # =======================================================================

    def read( self ) -> bool:
        """
        the pin value

        :result: (bool)
            the pin value (level)
        """
        return self._pin.value()

    # =======================================================================

# ===========================================================================


class gpio_oc( pin_oc ):
    """
    chip GPIO pin used as open-collector input output

    :param pin_nr: (int)
        the chip pin number
    """

    # =======================================================================

    def __init__(
        self,
        pin_nr
    ) -> None:
        import machine
        self._pin_nr = pin_nr
        self._pin = machine.Pin( pin_nr, machine.Pin.IN )
        pin_oc.__init__( self )

    # =======================================================================

    def write(
        self,
        value: bool
    ) -> None:
        """
        set the pin value

        :param value: (bool)
            the new pin value (level)
        """
        if value:
            self._pin.init( machine.Pin.IN )
        else:
            self._pin.value( False )
            self._pin.init( machine.Pin.OUT )

    # =======================================================================

    def read( self ) -> bool:
        """
        the pin value

        :result: (bool)
            the pin value (level)
        """
        return self._pin.value()

    # =======================================================================

# ===========================================================================
