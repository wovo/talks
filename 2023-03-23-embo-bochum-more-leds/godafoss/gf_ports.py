# ===========================================================================
#
# file     : gf_ports.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the port classes.
#
# ===========================================================================

from godafoss.gf_tools import *
from godafoss.gf_pins import *
from godafoss.gf_make_pins import *


# ===========================================================================
#
# _port provides the mechanism to modify (invert or mirror) a concrete
# port class.
# Each concrete class has a corresponding modifier class, which it
# passes to the _port constructor. This modifier class
# creates a decorated version of the original object.
# The decoration is the filter function, which is applied
# to the value before it is written, or after it has been read.
#
# ===========================================================================

class _port( invertible ):
    """
    digital port

    A port is an ordered set of digital pins,
    which can be read or written by one method call.
    The number of pins is available in the nr_of_pins attribute.

    There are four types of ports:
    - port_in
    - port_out
    - port_in_out
    - port_oc

    A port that supports reading (port_in, port_in_out, port_oc)
    can be read as a whole, which reads and returns the levels
    of the individual pins, the first pin as bit 0,
    the next pin as bit 1, etc.

    A port that supports writing(port_out, port_in_out,port_oc)
    can be written as a whole, which writes the bits of the
    written value to individual pins,
    bit 0 to the first pin, bit 1 to the next pin, etc.

    A port can be inverted (negated) to create a port with
    the read and write effect on all its pins inverted.

    The mirror() method returns a port where the bits are read
    or written mirored (pin order reversed).

    For a port that can be written, the as_pin_out() method returns
    a pin_out that writes to all pins in the port.
    """

    def __init__( self, pins, nr_of_pins, modifier ) -> None:
        self._pins = pins
        self.nr_of_pins = first_not_none(  nr_of_pins, len( self._pins ) )
        self._modifier = modifier
        invertible.__init__( self )

    def inverted( self ):
        """port with all pins inverted"""
        return self._modifier(
            self,
            lambda x: invert_bits( x, self.nr_of_pins )
        )

    def mirrored( self ):
        """port with the pins mirrored (pin order reversed)"""
        return self._modifier(
            self,
            lambda x: mirror_bits( x, self.nr_of_pins )
        )


# ===========================================================================
#
# The read and write functions are the same in the various port
# classes, so they are provided by the _port_resd_method and
# _port_write_methhod mixin classes.
#
# When these mixins are constructed with slave == None, they act on
# (read from of write to) the self._pins
#
# When they are constructed with slave != None they act on (delegate to)
# the read and write operations of the provided slave, and apply the
# filter to the value that is read or written.
# This mechanism is used to implement the port modifiers.
#
# ===========================================================================

class _port_read_method:

    def __init__( self, slave, filter ):
        self._slave = slave
        self._filter = filter

    def read( self ) -> int:
        """read and combine the pins that make up the port"""

        if self._slave is not None:
            return self._filter( self._slave.read() )

        else:
            result = 0
            for pin in self._pins[ :: -1 ]:
                result = result << 1
                if pin.read():
                    result |= 0b1
            return result


# ===========================================================================

class _port_write_method:

    def __init__( self, slave, filter ):
        self._slave = slave
        self._filter = filter

    def write( self, value ):
        """write the bits of value to the pins"""

        if self._slave is not None:
            return self._slave.write( self._filter( value ) )

        else:
            for pin in self._pins:
                pin.write( ( value & 0b1 ) == 0b1 )
                value = value >> 1

    def as_pin_out( self ):
        """pin_out that writes to all pins in the port"""
        return _pin_out_from_port_out( self.as_port_out() )


# ===========================================================================

class _pin_out_from_port_out( pin_out ):
    # proxy for writing to all pins of a port at once

    def __init__( self, slave ) -> None:
        self._slave = slave
        pin_out.__init__( self )

    def write( self, value ) -> None:
        """write the (same) logical value to all pins of the port"""
        if value:
            self._slave.write( invert_bits( 0, self._slave.nr_of_pins ) )
        else:
            self._slave.write( 0 )


# ===========================================================================
#
# port_in
#
# ===========================================================================

class port_in( _port, _port_read_method ):
    """
    digital input port

    A port_in is a port constructed from a number of pins that are
    inputs or can function as inputs.
    """

    def __init__(
        self,
        *args,
        nr_of_pins = None,
        slave = None,
        filter = None
    ):

        # create the list of the input pins
        try:
            pinset = [ make_pin_in( pin ) for pin in make_list( *args ) ]
        except AttributeError:
            raise AttributeError from None

        _port.__init__(
            self,
            pinset,
            nr_of_pins,
            _port_in_modifier
        )
        _port_read_method.__init__( self, slave, filter )

    def as_port_in( self ) -> "port_in":
        return self


# ===========================================================================

class _port_in_modifier( port_in ):

    def __init__( self, slave, filter ):
        port_in.__init__(
            self,
            nr_of_pins = slave.nr_of_pins,
            slave = slave,
            filter = filter
        )


# ===========================================================================
#
# port_out
#
# ===========================================================================

class port_out( _port, _port_write_method ):
    """
    digital output port

    A port_out is constructed from a number of pins that are outputs
    or can function as outputs.
    """

    def __init__(
        self,
        *args,
        nr_of_pins = None,
        slave = None,
        filter = None
    ):

        # create the list of the output pins
        try:
            pinset = [ make_pin_out( pin ) for pin in make_list( *args ) ]
        except AttributeError:
            raise AttributeError from None

        _port.__init__(
            self,
            pinset,
            nr_of_pins,
            _port_out_modifier
        )
        _port_write_method.__init__( self, slave, filter )

    def as_port_out( self ) -> "port_out":
        return self

    def demo( self, interval: int = 200_000, iterations = None ) -> None:
        """demo shows kitt display"""
        import godafoss.gf_pin_port_demos
        print( "port_out demo: kitt" )
        godafoss.gf_pin_port_demos.kitt(
            self,
            interval = interval,
            iterations = iterations
        )


# ===========================================================================

class _port_out_modifier( port_out ):

    def __init__( self, slave, filter ):
        port_out.__init__(
            self,
            nr_of_pins = slave.nr_of_pins,
            slave = slave,
            filter = filter
        )


# ===========================================================================
#
# port_in_out
#
# ===========================================================================

class port_in_out( _port, _port_read_method, _port_write_method ):
    """
    digital input output port

    A port_in_out is constructed from a number of pins that are
    input//outputs or can function as input//outputs.

    A port_in_out can be read or written as a whole, subject to the
    relevant pins being set to the correct direction:
    call direction_set_input() to prepare all pins
    for a read, call direction_set_output() to prepre
    all pins for a write.

    Individual pins cna be prepared for read or write by passing
    their number within the port to direction_set_input()
    or direction set_output().
    The pin value read for a pin that is output is not defined.
    A pin value written to a pin that is input might or might not
    have an effect once the pin is set to output.
    """

    def __init__(
        self,
        *args,
        nr_of_pins = None,
        slave = None,
        filter = None
    ):

        # create the list of the input output pins
        try:
            pinset = [ make_pin_in_out( pin ) for pin in make_list( *args ) ]
        except AttributeError:
            raise AttributeError from None

        _port.__init__(
            self,
            pinset,
            nr_of_pins,
            _port_in_out_modifier
        )
        _port_read_method.__init__( self, slave, filter )
        _port_write_method.__init__( self, slave, filter )

    def direction_set( self, directions: int ) -> None:
        for pin in self._pins:
            if ( directions & 0b1 ) == 0b0:
                pin.direction_set_output()
            else:
                pin.direction_set_input()
            directions = directions >> 1

    def direction_set_input( self ) -> None:
        self.direction_set( invert_bits( 0, self.nr_of_pins ) )

    def direction_set_output( self ) -> None:
        self.direction_set( 0 )

    def as_port_in( self ) -> "port_in":
        return _port_in_from_port_in_out( self )

    def as_port_out( self ) -> "port_out":
        return _port_out_from_port_in_out( self )

    def as_port_in_out( self ) -> "port_in_out":
        return self

    def as_port_oc( self ) -> "port_oc":
        return _port_oc_from_port_in_out( self )

    # no demo because in and out would have different demos


# ===========================================================================

class _port_in_out_modifier( port_in_out ):

    def __init__( self, slave, filter ):
        port_in_out.__init__(
            self,
            nr_of_pins = slave.nr_of_pins,
            slave = slave,
            filter = filter
        )


# ===========================================================================

class _port_in_from_port_in_out( port_in ):

    def __init__( self, slave ):
        self._slave = slave
        self._slave.direction_set_input()
        port_in.__init__(
            self,
            nr_of_pins = slave.nr_of_pins,
            slave = slave,
            filter = unity
        )

    def read( self ) -> int:
        return self._slave.read()


# ===========================================================================

class _port_out_from_port_in_out( port_out ):

    def __init__( self, slave ):
        self._slave = slave
        self._slave.direction_set_output()
        port_out.__init__(
            self,
            nr_of_pins = slave.nr_of_pins,
            slave = slave,
            filter = unity
        )

    def write( self, value: int ) -> None:
        self._slave.write( value )


# ===========================================================================
#
# port_oc
#
# ===========================================================================

class port_oc( _port, _port_read_method, _port_write_method ):
    """
    digital open-collector input output port

    A port_oc is constructed from a number of open-collector
    input output pins.

    A port_oc can be read or written as a whole.
    In practice, reading requires that all were previous writteb
    as 1 (high).
    """

    def __init__(
        self,
        *args,
        nr_of_pins = None,
        slave = None,
        filter = None
    ):

        # create the list of the input output pins
        try:
            pinset = [ make_pin_oc( pin ) for pin in make_list( *args ) ]
        except AttributeError:
            raise AttributeError from None

        _port.__init__(
            self,
            pinset,
            nr_of_pins,
            _port_oc_modifier
        )
        _port_read_method.__init__( self, slave, filter )
        _port_write_method.__init__( self, slave, filter )

    def as_port_in( self ) -> "port_in":
        return _port_in_from_port_oc( self )

    def as_port_out( self ) -> "port_out":
        return _port_out_from_port_oc( self )

    def as_port_in_out( self ) -> "port_in_out":
        return _port_in_out_from_port_oc( self )

    def as_port_oc( self ) -> "port_in_out":
        return self

    # no demo because in and out mode would have different demos


# ===========================================================================

class _port_oc_modifier( port_oc ):

    def __init__( self, slave, filter ):
        port_oc.__init__(
            self,
            nr_of_pins = slave.nr_of_pins,
            slave = slave,
            filter = filter
        )


# ===========================================================================

class _port_in_from_port_oc( port_in ):

    def __init__( self, slave ):
        self._slave = slave
        port_in.__init__(
            self,
            nr_of_pins = slave.nr_of_pins,
            slave = slave,
            filter = unity
        )
        self._slave.write( invert_bits( 0, self._slave.nr_of_pins ) )

    def read( self ) -> int:
        return self._slave.read()


# ===========================================================================

class _port_out_from_port_oc( port_out ):

    def __init__( self, slave ):
        self._slave = slave
        port_out.__init__(
            self,
            nr_of_pins = slave.nr_of_pins,
            slave = slave,
            filter = unity
        )

    def write( self, value: int ) -> None:
        self._slave.write( value )


# ===========================================================================

class _port_in_out_from_port_oc( port_in_out ):

    def __init__( self, slave ):
        self._slave = slave
        port_in_out.__init__(
            self,
            nr_of_pins = slave.nr_of_pins,
            slave = slave,
            filter = unity
        )

    def read( self ) -> int:
        return self._slave.read()

    def write( self, value: int ) -> None:
        self._slave.write( value )


# ===========================================================================

class _port_oc_from_port_in_out( port_oc ):

    def __init__( self, slave ):
        self._slave = slave
        port_oc.__init__(
            self,
            nr_of_pins = slave.nr_of_pins,
            slave = slave,
            filter = unity
        )

    def write( self, value: int ) -> None:
        self._slave.direction_set( value )
        self._slave.write( value )

    def read( self ) -> int:
        return self._slave.read()


# ===========================================================================
