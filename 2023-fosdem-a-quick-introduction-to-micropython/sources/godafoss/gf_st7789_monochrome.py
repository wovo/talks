# ===========================================================================
#
# file     : gf_st7789_monochrome.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the st7789 LCD driver class.
#
# ===========================================================================

from micropython import const
import framebuf
import machine

from godafoss.gf_time import *
from godafoss.gf_benchmark import *
from godafoss.gf_xy import *
from godafoss.gf_pins import *
from godafoss.gf_canvas import *
from godafoss.gf_lcd_spi import *
from godafoss.gf_lcd_reset_backlight_power import *


# ===========================================================================

class st7789_monochrome( canvas, lcd_spi, lcd_reset_backlight_power ):
    """
    st7789 SPI color lcd controller driver
    
    The parameters are the canvas size and (default) background,
    the spi pins, and the optional reset, power and backlight pins.
    
    Cheap st7735 lcd modules often have a deadband margin 
    around the displayed pixels. 
    Start is the location of the first to-be-displayed pixel.
    End is the location of the 
    
    This driver uses a RAM canvas of 2 bytes per pixel, 
    which can be more than your target has available.
    
    max 60 MHz
    """
    
    class cmd: # klopt van geen kanten
        NOP        = const( 0x00 )
        SWRESET    = const( 0x01 )
        RDDID      = const( 0x04 )
        RDDST      = const( 0x09 )
        
        RDDPM      = const( 0x0A )
        RDDMADCTL  = const( 0x0B )
        RDDIM      = const( 0x0D )
        RDDSEM     = const( 0x0E )
        RDDSDR     = const( 0x0F )
        SLPIN      = const( 0x10 )
        SLPOUT     = const( 0x11 )
        PTLON      = const( 0x12 )
        NORON      = const( 0x13 )
        INVOFF     = const( 0x20 )
        INVON      = const( 0x21 )
        GAMSET     = const( 0x26 )
        DISPOFF    = const( 0x28 )
        DISPON     = const( 0x29 )
        CASET      = const( 0x2A )
        RASET      = const( 0x2B )
        RAMWR      = const( 0x2C )
        RAMRD      = const( 0x2E )
        PTLAR      = const( 0x30 )
        VSCRDEF    = const( 0x33 )
        TEOFF      = const( 0x34 )
        TEON       = const( 0x35 )
        MADCTL     = const( 0x36 )
        COLMOD     = const( 0x3A )

    def __init__( 
        self, 
        size, 
        spi, 
        data_command: [ int, pin_out, pin_in_out, pin_oc ],
        chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
        reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
        backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
        power: [ int, pin_out, pin_in_out, pin_oc ] = None,
        background = False, 
        invert = False,
        x_reverse = False,
        y_reverse = False,
        xy_swap = False,
        offset = xy( 0, 0 ),
        x_deadband = 0,        
    ):
        self._offset = offset
        canvas.__init__(
            self,
            size = size,
            is_color = False,
            background = background
        )

        lcd_reset_backlight_power.__init__( 
            self, 
            reset = - make_pin_out( reset ), 
            backlight = backlight, 
            power = power,
            
            # 10 us low, 120 ms wait for reset to effectuate
            # ST7735 datasheet 9.16            
            reset_duration = 10,
            reset_wait = 120_000
        )
        
        lcd_spi.__init__(
            self,
            spi = spi,
            data_command = data_command,
            chip_select = chip_select,
        )  
            

        self._buffer = bytearray( ( self.size.x + x_deadband ) * ( self.size.y + 7 ) // 8 )
        self._framebuffer = framebuf.FrameBuffer(
            self._buffer, self.size.x + x_deadband, self.size.y, framebuf.MONO_VLSB )
        self._line_buffer = bytearray( 2 * self.size.x )        

        #self.write_command( self.cmd.SWRESET )
        self.write_command( self.cmd.SLPOUT )
        sleep_us(120_000)        
           
        self.write_command( self.cmd.COLMOD, [ 0x05 ] ) # was 66
        sleep_us(120_000)  
      
        self.write_command( self.cmd.MADCTL, [ 0x10 ] );  # was 10                    
        self.write_command( self.cmd.CASET, [
            0, 0, self.size.x >> 8, self.size.x & 0xFF ])
        self.write_command( self.cmd.RASET, [
            0, 0, self.size.y >> 8, self.size.y & 0xFF ])
      
        self.write_command( self.cmd.INVON )
        #time.sleep_ms( 10 )
        self.write_command( self.cmd.NORON )
        #time.sleep_ms( 100 )
        self.write_command( self.cmd.DISPON )
        #time.sleep_ms( 100 )
        
        self.write_command( self.cmd.INVON if invert else self.cmd.INVOFF )  
        
        m = 0x00
        if xy_swap:
            m |= 0x20
        if x_reverse:
            m |= 0x40
        if y_reverse:
            m |= 0x80
        self.write_command( self.cmd.MADCTL, [ m ] )          

        self.write_command( self.cmd.NORON )
        #time.sleep_ms( 10 )

        self.write_command( self.cmd.DISPON )
        #time.sleep_ms( 100 )
                  
    # =======================================================================
      
    @report  
    def _flush_implementation( self ):
        
        x_end = self.size.x - 1 + self._offset.x
        self.write_command( self.cmd.CASET, [
            0x00, self._offset.x, 
            x_end // 256, x_end % 256
        ])
        
        y_end = self.size.y - 1 + self._offset.y
        self.write_command( self.cmd.RASET, [ 
            0x00, self._offset.y,
            y_end // 256, y_end % 256
        ])
        
        self.write_command( self.cmd.RAMWR )
        for y in range( self.size.y ):
            for x in range( self.size.x ):
                c = 0xFF if self._framebuffer.pixel( x, y ) else 0x00
                self._line_buffer[ 2 * x ] = c                  
                self._line_buffer[ 2 * x + 1 ] = c                  
            self.write_command( None, buffer = self._line_buffer )            
        
    # =======================================================================
        
    def _clear_implementation( 
        self,
        ink: bool
    ):
        self._framebuffer.fill( ink )
        
    # =======================================================================
        
    def _write_pixel_implementation( 
        self, 
        location: ( int, xy ), 
        ink: bool
    ):
        self._framebuffer.pixel(
            location.x,
            location.y,
            ink
        )
        
    # =======================================================================

# ===========================================================================

    

 