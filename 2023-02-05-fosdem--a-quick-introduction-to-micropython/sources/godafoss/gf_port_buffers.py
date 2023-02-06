# ===========================================================================
#
# file     : gf_port_buffers.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file implements gpio buffers.
#
# ===========================================================================

from godafoss.gf_tools import *
from godafoss.gf_pins import *
from godafoss.gf_ports import *


# ===========================================================================
#
# the port buffer read and write related methods are identical for all
# buffered ports (except for the write in a buffered open collector port),
# so the are factored out to the next classes.
#
# ===========================================================================

class _port_buffer_read_methods:

    def __init__( self ):
        pass

    def refresh( self ) -> None:
        raise NotImplementedError

    def read( self ) -> int:
        """refresh the port value buffer and return it"""
        self.refresh()
        return self._value


# ===========================================================================

class _port_buffer_write_methods:

    def __init__( self ):
        pass

    def flush( self ) -> None:
        raise NotImplementedError

    def write( self, value ) -> None:
        """update the port value buffer and flush it"""
        self._value = value
        self.flush()


# ===========================================================================
#
# the port buffer read and write methods are identical (except for
# the write in a buffered open collector port), so the are factored out.
#
# ===========================================================================

class _pin_from_buffer_read_method:

    def __init__( self ):
        pass

    def read( self ) -> bool:
        """trampoline for refreshing and returning one bit from the buffer"""
        self._port.refresh()
        return ( self._port._value & self._mask ) != 0


# ===========================================================================

class _pin_from_buffer_write_method:

    def __init__( self ):
        pass

    def write( self, value ) -> None:
        """trampoline updating a bit in the buffer and fushing it"""
        if value:
            self._port._value |= self._mask
        else:
            self._port._value &= ~ self._mask
        self._port.flush()


# ===========================================================================
#
# A read of an port_in_buffer calls refresh() to update its _value,
# and returns the updated _value.
# A concrete implementation must implement the refresh.
#
# ===========================================================================

class port_in_buffer(
    _port_buffer_read_methods,
    port_in
):
    """
    remote digital input port

    A port_in_from_buffer is a proxy for a port of remote pins that is
    read via some protocol.
    """

    def __init__( self, nr_of_pins: int ):
        self._value = 0
        port_in.__init__( self, nr_of_pins = nr_of_pins )
        _port_buffer_read_methods.__init__( self )


# ===========================================================================

class pin_in_from_buffer(
    _pin_from_buffer_read_method,
    pin_in
):
    """proxy for reading a single pin from a buffered port"""

    def __init__( self, port: port_in_buffer, n: int ):
        self._port = port
        self._mask = 0b1 << n
        pin_out.__init__( self )
        _pin_from_buffer_read_method.__init__( self )


# ===========================================================================
#
# A write of an port_out_buffer updates the _value, and calls
# flush() to update the remote pins.
# A concrete implementation must implement the flush().
#
# ===========================================================================

class port_out_buffer(
    _port_buffer_write_methods,
    port_out
):
    """
    remote digital output port

    A port_out_from_buffer is a proxy for a port of remote pins that is
    written via some protocol.
    """

    def __init__( self, nr_of_pins: int ):
        self._value = 0
        port_in.__init__( self, nr_of_pins = nr_of_pins )
        _port_buffer_write_methods.__init__( self )


# ===========================================================================

class pin_out_from_buffer(
    _pin_from_buffer_write_method,
    pin_in
):
    """proxy for writing a single pin to a buffered port"""

    def __init__( self, port: port_out_buffer, n: int ):
        self._port = port
        self._mask = 0b1 << n
        pin_out.__init__( self )
        _pin_from_buffer_write_method.__init__( self )


# ===========================================================================
#
# The read() and write() maintain, refresh and flush the _value,
# exactly like the in and out ports do.
#
# ===========================================================================

class port_in_out_buffer(
    _port_buffer_read_methods,
    _port_buffer_write_methods,
    port_in_out
):
    """
    remote digital input output port

    A port_in_out_from_buffer is a proxy for a port of remote input output
    pins that is read, written and direction controlled via some protocol.
    """

    def __init__( self, nr_of_pins: int ):
        self._value = 0
        self._direction = invert_bits( 0, nr_of_pins )
        port_in_out.__init__( self, nr_of_pins = nr_of_pins )
        _port_buffer_read_methods.__init__( self )
        _port_buffer_write_methods.__init__( self )

    def refresh( self ) -> None:
        raise NotImplementedError

    def flush( self ) -> None:
        raise NotImplementedError

    def _direction_flush( self ) -> None:
        raise NotImplementedError

    def direction_set( self, direction: int ) -> None:
        self._direction = direction
        self._direction_flush()


# ===========================================================================

class pin_in_out_from_buffer(
    _pin_from_buffer_read_method,
    _pin_from_buffer_write_method,
    pin_in_out
):
    """proxy for writing a single pin of a buffered port"""

    def __init__( self, port: port_in_out_buffer, n: int ):
        self._port = port
        self._mask = 0b1 << n
        pin_in_out.__init__( self )
        _pin_from_buffer_read_method.__init__( self )
        _pin_from_buffer_write_method.__init__( self )

    def direction_set_input( self ) -> None:
        self._port._direction |= self._mask
        self._port._direction_flush()

    def direction_set_output( self ) -> None:
        self._port._direction &= ~ self._mask
        self._port._direction_flush()


# ===========================================================================
#
# ===========================================================================

class port_oc_buffer(
    _port_buffer_read_methods,
    _port_buffer_write_methods,
    port_oc
):
    """
    digital open-collector input-output port

    A port_in_from_buffer is a proxy for a port of pins that is
    read via some protocol.

    A port_in is read as a whole,
    which gets the ads and returns the levels of the individual pins,
    the first pin as bit 0, the next pin as bit 1, etc.
    """
    def __init__( self, nr_of_pins: int ):
        self._value = 0
        port_oc.__init__( self, nr_of_pins = nr_of_pins )
        _port_buffer_read_methods.__init__( self )
        _port_buffer_write_methods.__init__( self )


# ===========================================================================

class pin_oc_from_buffer(
    _pin_from_buffer_read_method,
    _pin_from_buffer_write_method,
    pin_oc
):
    """proxy for writing a single pin of a buffered port"""

    def __init__( self, port: port_oc_buffer, n: int ):
        self._port = port
        self._mask = 0b1 << n
        pin_oc.__init__( self )
        _pin_from_buffer_read_method.__init__( self )
        _pin_from_buffer_write_method.__init__( self )


# ===========================================================================
