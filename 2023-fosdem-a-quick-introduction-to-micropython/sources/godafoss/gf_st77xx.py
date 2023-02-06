# ===========================================================================
#
# file     : gf_st77xx.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains common functionality for st77xx LCD driver chips.
#
# ===========================================================================

from micropython import const
import framebuf
import machine

from godafoss.gf_time import *
from godafoss.gf_xy import *
from godafoss.gf_color import *
from godafoss.gf_pins import *
from godafoss.gf_canvas import *
from godafoss.gf_encode_565 import *
from godafoss.gf_lcd_spi import *
from godafoss.gf_lcd_reset_backlight_power import *


# ===========================================================================

class st77xx( encode_565 ):
    """
    st77xx SPI color lcd driver chips common parts
    """
    
    class cmd:
        NOP     = const( 0x00 ) 
        SWRESET = const( 0x01 )
        RDDID   = const( 0x04 )
        RDDST   = const( 0x09 )
        
        SLPIN   = const( 0x10 )
        SLPOUT  = const( 0x11 )
        NORON   = const( 0x13 )
        INVOFF  = const( 0x20 )
        INVON   = const( 0x21 )
        DISPOFF = const( 0x28 )
        DISPON  = const( 0x29 )
        
        CASET   = const( 0x2A )
        RASET   = const( 0x2B )
        RAMWR   = const( 0x2C )

        PTLAR   = const( 0x30 )
        COLMOD  = const( 0x3A )
        MADCTL  = const( 0x36 )
        
        RDID1   = const( 0xDA )
        RDID2   = const( 0xDB )
        RDID3   = const( 0xDC ) 
        RDID4   = const( 0xDD ) 
        FRMCTR1 = const( 0xB1 ) 
        FRMCTR2 = const( 0xB2 )
        FRMCTR3 = const( 0xB3 )
        INVCTR  = const( 0xB4 )
        PWCTR1  = const( 0xC0 )
        PWCTR2  = const( 0xC1 )
        PWCTR3  = const( 0xC2 )
        PWCTR4  = const( 0xC3 )
        PWCTR5  = const( 0xC4 )
        VMCTR1  = const( 0xC5 )
        GMCTRP1 = const( 0xE0 )
        GMCTRN1 = const( 0xE1 )

    def __init__( 
        self, 
        size, 
        spi: machine.SPI, 
        data_command: [ int, pin_out, pin_in_out, pin_oc ],
        chip_select: [ int, pin_out, pin_in_out, pin_oc ], 
        reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
        backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
        power: None | int | pin_out | pin_in_out | pin_oc = None,
        background = colors.black,
        invert = False,
        x_reverse = False,
        y_reverse = False,
        xy_swap = False,
        order: str = "RGB",
        offset = xy( 0, 0 ),
        x_deadband = 0,
    ):
        self._offset = offset
        canvas.__init__(
            self,
            size = size,
            is_color = True,
            background = background
        )
        lcd_reset_backlight_power.__init__( 
            self, 
            reset = - make_pin_out( reset ), 
            backlight = backlight, 
            power = power,
            
            # 10 us low, 120 ms wait for reset to effectuate
            # ST7735 datasheet 9.16      
            # ST7789 datasheet 7.4.5            
            reset_duration = 10,
            reset_wait = 120_000
        )         
        lcd_spi.__init__(
            self,
            spi = spi,
            data_command = data_command,
            chip_select = chip_select,
        )
        encode_565.__init__(
            self,
            order
        )    
        
        self._buffer = bytearray( 2 * self.size.y * ( self.size.x + x_deadband ) )
        self._framebuffer = framebuf.FrameBuffer(
            self._buffer, ( self.size.x + x_deadband ), self.size.y, framebuf.RGB565 )
        
        self.write_command( self.cmd.SLPOUT )
        sleep_us(120_000)
         
        self.write_command( self.cmd.INVCTR, [ 0x03 ] )


        #self.write_command( self.cmd.PWCTR1 )
        #self.write_command( self.cmd.PWCTR2, [ 0xC0 ] )
        #self.write_command( self.cmd.PWCTR3, [ 0x0D, 0x00 ] )
        #self.write_command( self.cmd.PWCTR4, [ 0x8D, 0x6A ] )
        #self.write_command( self.cmd.PWCTR5, [ 0x8D, 0xEE ] )

        #self.write_command( self.cmd.VMCTR1, [ 0x0E ] )

        #self.write_command( self.cmd.GMCTRP1,
        #    [ 0x10, 0x0E, 0x02, 0x03, 0x0E, 0x07, 0x02, 0x07,
        #      0x0A, 0x12, 0x27, 0x37, 0x00, 0x0D, 0x0E, 0x10 ] )
        #self.write_command( self.cmd.GMCTRN1,
        #    [ 0x10, 0x0E, 0x03, 0x03, 0x0F, 0x06, 0x02, 0x08,
        #      0x0A, 0x13, 0x26, 0x36, 0x00, 0x0D, 0x0E, 0x10 ] )
        
        self.write_command( self.cmd.INVON if invert else self.cmd.INVOFF )      

        self.write_command( self.cmd.COLMOD, [ 0x55 ] ) # 16-bit RGB 565
        
        m = 0x00
        if xy_swap:
            m |= 0x20
        if x_reverse:
            m |= 0x40
        if y_reverse:
            m |= 0x80
        self.write_command( self.cmd.MADCTL, [ m ] )       
        
        self.write_command( self.cmd.NORON )
        self.write_command( self.cmd.DISPON )

        
    # =======================================================================

    def _flush_implementation( self ):
        
        x_end = self.size.x - 1 + self._offset.x
        self.write_command( self.cmd.CASET, [
            self._offset.x // 256, self._offset.x % 256, 
            x_end // 256, x_end % 256
        ])
        
        y_end = self.size.y - 1 + self._offset.y
        self.write_command( self.cmd.RASET, [ 
            self._offset.y // 256, self._offset.y % 256,
            y_end // 256, y_end % 256
        ])
        
        self.write_command( self.cmd.RAMWR, buffer = self._buffer ) 
        
    # =======================================================================
        
    def _clear_implementation( 
        self,
        ink: color
    ):
        self._framebuffer.fill( self._encode( ink ) )
        
    # =======================================================================
        
    def _write_pixel_implementation( 
        self, 
        location: ( int, xy ), 
        ink: color
    ):
        self._framebuffer.pixel(
            location.x,
            location.y,
            self._encode( ink )
        )
        
    # =======================================================================

# ===========================================================================

        
        