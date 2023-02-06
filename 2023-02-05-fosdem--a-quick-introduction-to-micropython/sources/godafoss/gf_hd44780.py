# ===========================================================================
#
# file     : gf_hd44780.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the hd44780 character LCD driver class.
#
# ===========================================================================

import time

from godafoss.gf_terminal import *
from godafoss.gf_pins import *
from godafoss.gf_make_pins import *


# ===========================================================================

class hd44780( terminal ):
    """
    hd44780 character LCD interface
    
    This class implements an interface to an hd44780 character LCD.
    
    .. figure::  ../images/hd44780-picture.jpg
    
    The hd44780 is the standard chip for interfacing small dot-character
    LCD interfaces.
    It can display the ASCII table characters, 8 characters (0..7)
    that can be user-defined as 5x7 pixels, and a an upper 128 characters
    (128...255) that vary with the chip variant, often Japanese characters.
    
    The chip and its digital pins run at 5V.
    The contrast input can in most cases be connected to 0V (ground), but
    better is to use a 10k potentiometer between 0V and 5V. Some
    displays (mostly extended-temperature-range types) need the lower
    size of this potentiometer tied to a negative voltage, for instance -5V.
    
    The digital interface to the chip has 8 data lines, but the chip can be
    configured to use only 4. This adds some complexity to the driver
    software and slows it down a little, but the saving of 4 micro-controller
    more than compensates for this, hence nearly all software
    (including this driver) for is for the 4-bit interface.
    Note for the 4-bit interface the 4 highest data pins (D4..D7) are used.
    The lower 4 can be left unconnected.
    
    The chip has some locations that can be writen and also read back,
    but this offers little advantage, so most software (including this driver)
    only writes to the chip, thus saving another pin.
    Hence 6 pins (+ ground and 5V)
    are needed to interface to an hd44780 display:
    4 data lines, the R/S line (selects between command and data),
    and the E line (a strobe for the command).
    
    .. figure::  ../images/hd44780-connection.png
    
    (Some larger displays use not one but two hd44780 chips.
    This interface is not compatible with such LCDs.)
    
    Most hd44780 LCDs have a single row of connections,
    with the following pinout:
    
    .. figure::  ../images/hd44780-pinout.jpg
    
    But as always, check the datasheet (in this case of the LCD) to be sure!
    
    The hd44780 implements the ostream interface, but it doesn't scroll:
    while the cursor is outside the visible characters 
    (beyond the end of the line,
    or beyond the number of lines) any character writes will be ignored.
    Some characters are treated special:
       - '\\n' clears the rest of the line, and then
         moves to the first position of the next line
       - '\\r' puts the cursor at the start of the current line
       - '\\c' moves the cursor to the top-left position
    
    The best way to get a flicker-free display is to overwite
    instead of clear-and-then-write:
    use '\\c' to got to the 'origin', then rewrite the whole display,
    using '\\n' to go to a next line 
    (because it clears the remainder of the line).
    """

    # =======================================================================    

    def __init__( 
        self, 
        size, 
        data: [ port_out, port_in_out, port_oc ],
        rs : [ int, pin_out, pin_in_out, pin_oc ], 
        e: [ int, pin_out, pin_in_out, pin_oc ], 
        rw: [ int, pin_out, pin_in_out, pin_oc ], 
        backlight
    ):
        terminal.__init__( self, size )

        self._data = data.as_port_out()
        self._rs = make_pin_out( rs )
        self._e = make_pin_out( e )
        self._rw = make_pin_out( rw )
        self.backlight = backlight
        self.init()

    # =======================================================================    

    def init( self ):
        """initialize the hd44780 chip to 4-bit mode"""
        self._rw.write( 0 )
        self.backlight.write( 1 )

        # give LCD time to wake up
        self._e.write( 0 )
        self._rs.write( 0 )
        time.sleep_ms( 100  )

        # interface initialization: make sure the LCD is in 4 bit mode
        # (magical sequence, taken from the HD44780 data-sheet)
        self._write4( 0x03 )
        time.sleep_ms( 15 )
        self._write4( 0x03 )
        time.sleep_us( 100 )
        self._write4( 0x03 )
        self._write4( 0x02 )            # 4 bit mode

        # functional initialization
        self.command( 0x28 )            # 4 bit mode, 2 lines, 5x8 font
        self.command( 0x0C )            # display on, no cursor, no blink
        self.clear()                    # clear display, 'cursor' home
        self.cursor_set( xy( 0, 0 ) )   # 'cursor' home

    # =======================================================================    

    def _write4( self, data: int ):
        time.sleep_us( 10 )
        self._data.write( data )
        time.sleep_us( 20 )
        self._e.write( 1 )
        time.sleep_us( 20 )
        self._e.write( 0 )
        time.sleep_us( 100 )

    # =======================================================================    

    def data( self, data: int ):
        """write a data byte to the hd44780"""
        self._rs.write( 1 )
        self._write4( data >> 4 )
        self._write4( data )

    # =======================================================================    

    def command( self, data: int ):
        """write a command to the hd44780"""
        self._rs.write( 0 )
        self._write4( data >> 4 )
        self._write4( data )

    # =======================================================================    

    def clear( self ):
        """clear the display and put the cursor at xy( 0, 0 ) """
        self.command( 0x01 )
        time.sleep_ms( 5 )
        self.cursor_set( xy( 0, 0 ) )

    # =======================================================================    

    def _cursor_set_implementation( self ):
        # the NVI cursor_set() method has already set the cursor attribute

        if self.size.y == 1:
            if self.cursor.x < 8:
                self.command( 0x80 + self.cursor.x )
            else:
                self.command( 0x80 + 0x40 + ( self.cursor.x - 8 ) )
        else:
            if self.size.y == 2:
                self.command(
                    0x80
                    + choose( self.cursor.y > 0, 0x00, 0x40 )
                    + self.cursor.x
                )
            else:
                self.command(
                    0x80
                     + choose( ( self.cursor.y & 0x01 ) != 0, 0x00, 0x40 )
                     + choose( ( self.cursor.y & 0x02 ) != 0, 0x00, 0x14  )
                     + self.cursor.x
                )

    # =======================================================================    

    def _write_implementation( self, c: chr ):

        # the NVI write() method handles the cursor update

        # handle the gap for 1-line displays
        if ( self.size.y == 1 ) and ( self.cursor.x == 8 ):
            self.cursor_set( self.cursor )

        self.data( ord( c ) )
        
    # =======================================================================    

    def demo( self ):
        print( "hd44780 demo: blink Hello world!" )
        self.clear()
        self.write( "Hello world!\n2\n3\n4" )
        
# =========================================================================== 
