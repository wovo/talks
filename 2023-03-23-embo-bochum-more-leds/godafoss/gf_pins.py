# ===========================================================================
#
# file     : gf_pins.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the functions that make pins.
#
# ===========================================================================

from godafoss.gf_time import *
from godafoss.gf_tools import *
from godafoss.gf_invertible import *


# ===========================================================================

class _pin( invertible ):
    """
    pin base clase

    All pin types are invertible.

    All pins types except pin_out can be and-ed together (& operator)
    to yield a pin_out that writes to both and-ed pins.
    """

    # =======================================================================

    def __init__( self ):
        invertible.__init__( self )

    # =======================================================================

    def __and__( self, other ) -> "pin_out":
        """write to both pins"""

        try:
            return _pin_out_from_pins(
                self.as_pin_out(),
                other.as_pin_out()
            )

        except AttributeError:
            # this method has no type hints because that would
            # make this line unreachable
            raise TypeError from None

    # =======================================================================


# ===========================================================================

class pin_in( _pin ):
    """
    digital input pin

    A pin_in is a digital input pin: an object from which you can
    read() a bool value.

    A pin can be negated (minus operator or inverted() function)
    to create a pin that will read the inverted level relative to the
    original pin.

    Input pins can be added together or to a port_in to create
    a (larger) port_in.

    The as_pin_in() function returns the pin itself.

    The input demo function reads and prints the pin value.
    """

    # =======================================================================

    def __init__( self ):
        _pin.__init__( self )

    # =======================================================================

    def read( self ) -> bool:
        """read the logical input level"""
        raise NotImplementedError

    # =======================================================================

    def inverted( self ) -> "pin_in":
        """pin that reads the inverted level"""
        return _pin_in_inverted( self )

    # =======================================================================

    def as_pin_in( self ) -> "pin_in":
        """return the pin itself"""
        return self

    # =======================================================================

    def demo(
        self,
        interval: int = 500_000,
        iterations = None
    ) -> None:
        """pin_in demo: show the pin value"""
        import godafoss.gf_pin_port_demos

        if iterations is not None:
            print( "pin_in demo" )

        godafoss.gf_pin_port_demos.show(
            self,
            interval = interval,
            iterations = iterations
        )

    # =======================================================================


class _pin_in_inverted( pin_in ):
    """proxy that invertes a pin_in"""

    def __init__( self, pin: "pin_in" ):
        pin_in.__init__( self )
        self._pin = pin

    def read( self ) -> bool:
        return not self._pin.read()

    def inverted( self ) -> pin_in:
        return self._pin


# ===========================================================================

class pin_out( _pin ):
    """
    digital output pin

    A pin_out is a digital output pin: an object to which you can
    write() a digital level.

    A pin can be inverted (minus operator or invert() function)
    to create a pin that will write the inverted level.

    Output pins can be added together or to a port_out to create
    a (larger) port_out.

    The as_output() function returns the pin itself.

    The demo of an output pin blinks the pin.
    """

    # =======================================================================

    def __init__( self ):
        _pin.__init__( self )

    # =======================================================================

    def write( self, value ) -> None:
        """write the value to the pin"""
        raise NotImplementedError

    # =======================================================================

    def inverted( self ) -> "_pin_out_inverted":
        """pin that writes the inverted value"""
        return _pin_out_inverted( self )

    # =======================================================================

    def as_pin_out( self ) -> "pin_out":
        """return the pin itself"""
        return self

    # =======================================================================

    def pulse(
        self,
        high_time: int,
        low_time: int = 0
    ) -> None:
        """
        high pulse on the pin

        Make the pin high, wait high_time, make the pin low, and
        wait for low_time.

        Times are in us (microseconds).
        """

        self.write( True )
        if high_time != 0:
            sleep_us( high_time )

        self.write( False )
        if low_time != 0:
            sleep_us( low_time )

    # =======================================================================

    def demo(
        self,
        interval: int = 200_000,
        iterations = None
    ) -> None:
        """pin_out demo: blink the pin"""
        import godafoss.gf_pin_port_demos

        if iterations is not None:
            print( "pin_out blink demo" )

        godafoss.gf_pin_port_demos.blink(
            self,
            high_time = interval // 2,
            iterations = iterations
        )

# ===========================================================================


class _pin_out_inverted( pin_out ):
    """proxy that inverses a pin_out"""

    def __init__( self, pin: pin_out ):
        pin_out.__init__( self )
        self._pin = pin

    def write( self, value ) -> None:
        self._pin.write( not value )

    def inverted( self ) -> "pin_out":
        return self._pin

# ===========================================================================


class _pin_out_from_pins( pin_out ):
    """proxy that writes to two output pins"""

    def __init__( self, a: pin_out, b: pin_out ):
        self._a = a
        self._b = b
        pin_out.__init__( self )

    def write( self, value ) -> None:
        self._a.write( value )
        self._b.write( value )


# ===========================================================================

class pin_in_out( _pin ):
    """
    digital input output pin

    A pin_in_out is a digital input output pin.

    The direction can be set to input or output.

    When the direction is output, the pin level can be written.

    When the direction is input, the pin level can be read.

    A pin can be inverted (minus operator or inverted() function)
    to create a pin that will read and write the inverted level.

    Input output pins can be added together or to a port_in_out to create
    a (larger) port_in_out.

    The as_pin_in function returns the input-only version of the pin.

    The as_pin_out function returns the output-only version of the pin.

    The as_pin_in_out function returns the pin itself.
    """

    # =======================================================================

    def __init__( self ):
        _pin.__init__( self )

    # =======================================================================

    def direction_set_input( self ) -> None:
        """make the pin an input"""
        raise NotImplementedError

    # =======================================================================

    def direction_set_output( self ) -> None:
        """make the pin an output"""
        raise NotImplementedError

    # =======================================================================

    def write( self, value ) -> None:
        """write the value to the pin"""
        raise NotImplementedError

    # =======================================================================

    def read( self ) -> bool:
        """read the logical input level"""
        raise NotImplementedError

    # =======================================================================

    def as_pin_out( self ) -> "pin_out":
        """pin_out version of the pin"""
        return self._as_pin_out( self )

    class _as_pin_out( pin_out ):

        def __init__( self, slave ):
            self._slave = slave
            self._slave.direction_set_output()
            pin_out.__init__( self )

        def write( self, value ) -> None:
            self._slave.write( value )

    # =======================================================================

    def as_pin_in( self ) -> "pin_in":
        """pin_in version of the pin"""
        return self._as_pin_in( self )

    class _as_pin_in( pin_in ):

        def __init__( self, slave ):
            self._slave = slave
            self._slave.direction_set_input()
            pin_out.__init__( self )

        def read( self ) -> bool:
            return self._slave.read()

    # =======================================================================

    def as_pin_in_out( self ) -> "pin_in_out":
        """the pin itself"""
        return self

    # =======================================================================

    def as_pin_oc( self ) -> "pin_oc":
        """
        pin_oc version of the pin

        This method returns a pin that behaves as a pin_oc.
        """
        return _pin_in_out_as_pin_oc( self )

    # =======================================================================

    def inverted( self ) -> "pin_in_out":
        """pin that reads and writes the inverted level"""
        return _pin_in_out_inverted( self )

    # =======================================================================


class _pin_in_out_inverted( pin_in_out ):
    """proxy that inverses a pin_in_out"""

    def __init__( self, pin: pin_in_out ):
        pin_in_out.__init__( self )
        self._pin = pin

    def direction_set_input( self ) -> None:
        self._pin.direction_set_input()

    def direction_set_output( self ) -> None:
        self._pin.direction_set_output()

    def write( self, value ) -> None:
        self._pin.write( not value )

    def read( self ) -> bool:
        return not self._pin.read()

    def inverted( self ) -> pin_in_out:
        return self._pin


# ===========================================================================

class pin_oc( _pin ):
    """
    open-collector input output pin

    A pin_oc is an open-collector (or more likely, open-drain)
    digital input output pin.

    The pin level can be written.
    When a 0 is written, the pin hardware will pull the output level low.
    When a 1 is written, the pin hardware will let the pin level float.

    The pin level can be read.
    When a 0 has been written to the pin, a 0 will be read unless
    there is some serious hardware trouble.
    When a 1 has been written, the level on the pin will be read.

    A pin can be negated to create a pin that will read and write
    the inverted level.

    The as_pin_in function returns the input-only version of the pin.

    The as_pin_out function returns the output-only version of the pin.

    The as_pin_in_out function returns the input-output version
    of the pin. Note that is a pseudo input-output: writing a zero to
    it will pull the output low, but writing a one to it will float
    the output (not pull it high, as a read input-output pin would).

    The as_pin_oc function returns the pin itself.

    Open collector pins can be added together or to a port_oc to create
    a (larger) port_oc.
    """

    # =======================================================================

    def __init__( self ):
        _pin.__init__( self )

    # =======================================================================

    def write( self, value ) -> None:
        """write the value to the pin"""
        raise NotImplementedError

    # =======================================================================

    def read( self ) -> bool:
        """read the logical input level"""
        raise NotImplementedError

    # =======================================================================

    def inverted( self ) -> "pin_oc":
        return _pin_oc_inverted( self )

    # =======================================================================

    def as_pin_in( self ) -> pin_in:
        return self._as_pin_in( self )

    class _as_pin_in( pin_in ):

        def __init__( self, slave ):
            self._slave = slave
            pin_in.__init__( self )
            self._slave.write( 1 )

        def read( self ):
            return self._slave.read()

    # =======================================================================

    def as_pin_out( self ) -> pin_out:
        return self._as_pin_out( self )

    class _as_pin_out( pin_out ):

        def __init__( self, slave ):
            self._slave = slave
            pin_out.__init__( self )

        def write( self, value ) -> None:
            self._slave.write( value )

    # =======================================================================

    def as_pin_in_out( self ) -> pin_in_out:
        return self._as_pin_in_out( self )

    class _as_pin_in_out( pin_in_out ):

        def __init__( self, slave ):
            self._slave = slave
            pin_in_out.__init__( self )

        def direction_set_input( self ) -> None:
            self._slave.write( 1 )

        def direction_set_output( self ) -> None:
            pass

        def read( self ) -> bool:
            return self._slave.read()

        def write( self, value ) -> None:
            self._slave.write( value )

    # =======================================================================

    def as_pin_oc( self ) -> "pin_oc":
        return self

    # =======================================================================


class _pin_oc_inverted( pin_oc ):
    """proxy that inverses a pin_oc"""

    def __init__( self, pin: pin_oc ):
        pin_oc.__init__( self )
        self._pin = pin

    def write( self, value ) -> None:
        self._pin.write( not value )

    def read( self ) -> bool:
        return not self._pin.read()

    def inverted( self ) -> pin_oc:
        return self._pin


# ===========================================================================

class _pin_in_out_as_pin_oc( pin_oc ):

    def __init__( self, slave ):
        self._slave = slave
        pin_oc.__init__( self )

    def read( self ) -> bool:
        return self._slave.read()

    def write( self, value ) -> None:
        if value:
            self._slave.direction_set_input()
        else:
            self._slave.direction_set_output()
            self._slave.write( False )

# ===========================================================================


class new_pin_in_out_dummy( pin_in_out ):
    """
    a dummy in-out pin

    This dummy pin just sets the is_output and value properties,
    or returns the value property.
    """

    def __init__( self ):
        pin_in_out.__init__( self )
        self.value = False
        self.is_output = None

    def direction_set_input( self ) -> None:
        self.is_output = False

    def direction_set_output( self ) -> None:
        self.is_output = True

    def write( self, value ) -> None:
        self.value = value

    def read( self ) -> bool:
        return True if self.value else False


pin_in_out_dummy = new_pin_in_out_dummy()
pin_in_dummy = pin_in_out_dummy.as_pin_in()
pin_out_dummy = pin_in_out_dummy.as_pin_out()
pin_oc_dummy = pin_in_out_dummy.as_pin_oc()


# ===========================================================================
