# ===========================================================================
#
# file     : gf_tm16xx.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
# 
# This file contains the tm16_base class.
#
# ===========================================================================

from micropython import const
import framebuf

from godafoss.gf_time import *
from godafoss.gf_tools import *


# ===========================================================================

class tm16xx:
    """
    interface to tm16xx chips
    
    This class provides the interface to tm16xx
    LED and keypad interface chips.
    """
    
    # =======================================================================

    class commands: 
        MODE       = const( 0x40 ) # 0b1000 = test, 0b0100 = fixed address
        OFF        = const( 0x80 )      
        BRIGHTNESS = const( 0x88 ) # + 3 bit level        
        ADDRESS    = const( 0xC0 ) # + 4 bit address    
        READ       = const( 0x42 ) # + 4 bit address    

    # =======================================================================

    def __init__( 
        self,
        size : xy,
        brightness: int
    ) -> None:      
        self._brightness = clamp( brightness, 0, 7 )
        self._enabled = True
        self.brightness( brightness )
        self.write_command( self.commands.MODE | 0 )
        
        self._buffer = bytearray(( size.y // 8 ) * size.x )
        self._framebuf = framebuf.FrameBuffer(
            self._buffer, size.x, size.y, framebuf.MONO_VLSB 
        )       

    # =======================================================================

    def _start( self ) -> None:
        raise NotImplementedError  
        
    # =======================================================================

    def _stop( self ) -> None:
        raise NotImplementedError  
            
    # =======================================================================

    def _ack( self ) -> None:
        pass  
            
    # =======================================================================
        
    def _write_byte(
        self,
        b: int
    ) -> None:
        # write 8 bits, start with LSB
        for _ in range( 8 ):
            self._dio.write( ( b & 0x01 ) != 0 )
            b = b >> 1
            sleep_us( 1 )
            self._slk.write( 1 )
            sleep_us( 10 )
            self._slk.write( 0 )
            sleep_us( 10 )
        self._ack()
            
    # =======================================================================
        
    def _read_byte( self ) -> int:
        # read 8 bits, start with LSB
        self._dio.write( 1 )
        sleep_us( 10 )
        result = 0
        for _ in range( 32 ):
            result = result >> 1
            if self._dio.read():
                result |= 0x8000_0000
            sleep_us( 1 )
            self._slk.write( 1 )
            sleep_us( 1 )
            self._slk.write( 0 )
            sleep_us( 1 )
        self._ack()
        return result
            
    # =======================================================================

    def write_command(
        self,
        cmd: int,
        data # : Iterable[ int ] = ()
    ) -> None:
        """
        send command and optional data
        
        This method sends a the command and optional data
        to the chip.
        """
        
        self._start()
        self._write_byte( cmd )
        for d in data:
            self._write_byte( d )
        self._stop()
        
    # =======================================================================

    def read_chip( self ) -> int:
        """
        read
        
        This method sends a the command and optional data
        to the chip.
        """
        
        self._start()
        self._write_byte( self.commands.READ )
        result = self._read_byte()
        self._stop()
        return result        
        
    # =======================================================================

    def enable(
        self,
        v: bool
    ) -> None:
        self._enabled = v
        self._write_enable_and_brightness()
        
    # =======================================================================

    def brightness(
        self,
        v: int
    ) -> None:
        self._brightness = clamp( v, 0, 7 )
        self._write_enable_and_brightness()
        
    # =======================================================================

    def _write_enable_and_brightness( self ) -> None:
        if self._enabled:
            self.write_command( self.commands.BRIGHTNESS | self._brightness )
        else:    
            self.write_command( self.commands.OFF )
            
    # =======================================================================

    def _clear_implementation(
        self,
        ink: bool = False
    ) -> None:
        self._framebuf.fill( 0xFF if ink else 0x00 )                

    # =======================================================================

    def _flush_implementation( self ) -> None:      
        
        # set write pointer(s); write pixel data
        self.write_command( self.commands.ADDRESS | 0, self._buffer )            

    # =======================================================================


# ===========================================================================