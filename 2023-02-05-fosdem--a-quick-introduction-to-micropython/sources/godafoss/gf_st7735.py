# ===========================================================================
#
# file     : gf_st7735.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the st7735 LCD driver class.
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
from godafoss.gf_lcd_spi import *
from godafoss.gf_lcd_reset_backlight_power import *


# ===========================================================================

class st7735( canvas, lcd_spi, lcd_reset_backlight_power ):
    """
    st7735 SPI color lcd controller driver
    
    :param size: (:class:`~godafoss.xy`)
        horizontal and vertical size, in pixels
        
    :param spi: (machine.SPI)
        spi bus that connects to the chip (miso not used) max 16 MHz
        
    :param dc: ($macro_insert make_pin_out_types )
        data/command pin
        
    :param cs: ($macro_insert make_pin_out_types )
        chip select pin (active low)
        
    :param reset: (None, $macro_insert make_pin_out_types )
        reset pin; active low;
        optional, the pin can be connected to Vcc (3.3V).
        
    :param power: (None, $macro_insert make_pin_out_types )
        optional
        
    :param background: (bool)
        background 'color', default (False) is off (white-ish)
    
    :param offset: (:class:`~godafoss.xy`)
        the location of the first to-be-displayed (topleft) pixel
        optional, default is (0,0)
        
    This chip is often used in cheap color displays.
    
    This driver uses a RAM canvas of 2 bytes per pixel.
    On smaller targets this can be cause memory allocation failure.
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
        RAMRD   = const( 0x2E )
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
            reset_duration = 10,
            reset_wait = 120_000
        )         
        lcd_spi.__init__(
            self,
            spi = spi,
            data_command = data_command,
            chip_select = chip_select,
        )
        
        order = order.upper()
        if order == "RGB":
            self._encode = self._encode_rgb
        elif order == "RBG":
            self._encode = self._encode_rbg        
        elif order == "GRB":
            self._encode = self._encode_grb
        elif order == "GBR":
            self._encode = self._encode_gbr        
        elif order == "BRG":
            self._encode = self._encode_brg        
        elif order == "BGR":
            self._encode = self._encode_bgr
        else:
            raise ValueError( "unsupported color order '%s'" % order )
        
        self._buffer = bytearray( 2 * self.size.y * ( self.size.x + x_deadband ) )
        self._framebuffer = framebuf.FrameBuffer(
            self._buffer, ( self.size.x + x_deadband ), self.size.y, framebuf.RGB565 )
        
        self.write_command( self.cmd.SLPOUT )
        sleep_us(120_000)
         
        self.write_command( self.cmd.INVCTR, [ 0x03 ] )

        # self.write_command( 0x62, [ 0x02, 0x04 ] )

        self.write_command( self.cmd.PWCTR1 )
        self.write_command( self.cmd.PWCTR2, [ 0xC0 ] )
        self.write_command( self.cmd.PWCTR3, [ 0x0D, 0x00 ] )
        self.write_command( self.cmd.PWCTR4, [ 0x8D, 0x6A ] )
        self.write_command( self.cmd.PWCTR5, [ 0x8D, 0xEE ] )

        self.write_command( self.cmd.VMCTR1, [ 0x0E ] )

        self.write_command( self.cmd.GMCTRP1,
            [ 0x10, 0x0E, 0x02, 0x03, 0x0E, 0x07, 0x02, 0x07,
              0x0A, 0x12, 0x27, 0x37, 0x00, 0x0D, 0x0E, 0x10 ] )
        self.write_command( self.cmd.GMCTRN1,
            [ 0x10, 0x0E, 0x03, 0x03, 0x0F, 0x06, 0x02, 0x08,
              0x0A, 0x13, 0x26, 0x36, 0x00, 0x0D, 0x0E, 0x10 ] )
        
        if 0: self.write_command( self.cmd.FRMCTR1,
            [ 0x05, 0x3A, 0x3A ] )
        if 0: self.write_command( self.cmd.FRMCTR2,
            [ 0x05, 0x3A, 0x3A ] )
        if 0: self.write_command( self.cmd.FRMCTR3,
            [ 0x05, 0x3A, 0x3A, 0x05, 0x3A, 0x3A ] )
        
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
        
        self.write_command( self.cmd.DISPON )
        sleep_us(100 )
        
    # =======================================================================

    def _flush_implementation( self ):
        self.write_command( self.cmd.CASET, [
            0x00, self._offset.x, 
            0x00, self.size.x - 1 + self._offset.x 
        ])
        self.write_command( self.cmd.RASET, [ 
            0x00, self._offset.y,
            0x00, self.size.y - 1 + self._offset.y
        ])
        self.write_command( self.cmd.RAMWR, buffer = self._buffer )
        
    # =======================================================================
     
    def _encode_rgb( self, c ):
        return (
            (( c.red & 0xF8 ) << 8 )
            | (( c.green & 0xFC ) << 3 )
            | ( c.blue >> 3 )
        )        
        
    # =======================================================================
    
    def _encode_rbg( self, c ):
        return (((c.green&0b00011100)<<3) +((c.red&0b11111000)>>3)<<8) + (c.blue&0b11111000)+((c.green&0b11100000)>>5)
        return 0x_00_00_00_80
        return (
            ( c.red << 16 )
            | ( c.blue << 8 )
            | ( c.green << 0 )
        )        
        
    # =======================================================================

    def _encode_brg( self, c ):
        return (
            (( c.blue & 0xF8 ) << 8 )
            | (( c.red & 0xFC ) << 3 )
            | ( c.green >> 3 )
        )        
        
    # =======================================================================

    def _encode_bgr( self, c ):
        return (
            (( c.blue & 0xF8 ) << 8 )
            | (( c.green & 0xFC ) << 3 )
            | ( c.red >> 3 )
        )        
        
    # =======================================================================

    def _encode_gbr( self, c ):
        return (
            (( c.green & 0xF8 ) << 8 )
            | (( c.blue & 0xFC ) << 3 )
            | ( c.red >> 3 )
        )        
        
    # =======================================================================

    def _encode_grb( self, c ):
        return (
            (( c.green & 0xF8 ) << 8 )
            | (( c.red & 0xFC ) << 3 )
            | ( c.blue >> 3 )
        )        
        
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

        
        