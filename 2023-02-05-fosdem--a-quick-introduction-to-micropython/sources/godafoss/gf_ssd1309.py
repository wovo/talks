# ===========================================================================
#
# file     : gf_ssd1306.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the ssd1306 OLED driver class.
#
# ===========================================================================

from micropython import const
import framebuf

from godafoss.gf_xy import *
from godafoss.gf_color import *
from godafoss.gf_canvas import *


# ===========================================================================

class _ssd1306_base( canvas ):
    """
    ssd1306 spi/i2c b/w oled display driver
    """

    class cmd:
        set_contrast        = const( 0x81 )
        set_entire_on       = const( 0xa4 )
        set_norm_inv        = const( 0xa6 )
        set_disp            = const( 0xae )
        set_mem_addr        = const( 0x20 )
        set_col_addr        = const( 0x21 )
        set_page_addr       = const( 0x22 )
        set_disp_start_line = const( 0x40 )
        set_seg_remap       = const( 0xa0 )
        set_mux_ratio       = const( 0xa8 )
        set_com_out_dir     = const( 0xc0 )
        set_disp_offset     = const( 0xd3 )
        set_com_pin_cfg     = const( 0xda )
        set_disp_clk_div    = const( 0xd5 )
        set_precharge       = const( 0xd9 )
        set_vcom_desel      = const( 0xdb )
        set_charge_pump     = const( 0x8d )

    def __init__( self, size, background ):

        canvas.__init__( self, size, background )
        
        self.buffer = bytearray(( self.size.y // 8 ) * self.size.x )
        self.framebuf = framebuf.FrameBuffer(
            self.buffer, self.size.x, self.size.y, framebuf.MONO_VLSB )
            
        for x in (
            self.cmd.set_disp | 0x00,  # off
            # address setting
            self.cmd.set_mem_addr, 0x00,  # horizontal
            # resolution and layout
            self.cmd.set_disp | 0x00,  # off
            self.cmd.set_disp_start_line | 0x00,
            self.cmd.set_seg_remap | 0x01,  # column addr 127 mapped to seg0
            self.cmd.set_mux_ratio, self.size.y - 1,
            self.cmd.set_com_out_dir | 0x08,  # scan from com[n] to com0
            self.cmd.set_disp_offset, 0x00,
            self.cmd.set_com_pin_cfg, 0x02 if self.size.y == 32 else 0x12,
            # timing and driving scheme
            self.cmd.set_disp_clk_div, 0x80,
            self.cmd.set_precharge, 0xf1,
            self.cmd.set_vcom_desel, 0x30,  # 0.83*vcc
            # display
            self.cmd.set_contrast, 0xff,  # maximum
            self.cmd.set_entire_on,  # output follows ram contents
            self.cmd.set_norm_inv,  # not inverted
            # charge pump
            self.cmd.set_charge_pump, 0x14,
            self.cmd.set_disp | 0x01,

        ):
            self.write_cmd( x )
        self.clear()
        self.flush()
        
    def draw_pixel_implementation( self, location: xy, ink ):        
        self.framebuf.pixel( location.x, location.y, ink != color.black )

    def write_cmd( self, cmd ):
        raise NotImplementedError
        
    def clear( self, ink = None ):
        ink = first_not_none( ink )        
        self.framebuf.fill( ink != color.black )
        
    def flush( self ):
        x0 = 0
        x1 = self.size.x - 1
        if self.size.x == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd( self.cmd.set_col_addr )
        self.write_cmd( x0 )
        self.write_cmd( x1 )
        self.write_cmd( self.cmd.set_page_addr )
        self.write_cmd( 0 )
        self.write_cmd( self.size.y // 8 - 1 )
        self.write_framebuf()


class ssd1306_i2c( _ssd1306_base ):
    "Hello"

    def __init__( self, size, i2c, background, addr = 0x3c ):
        self.i2c = i2c
        self.addr = addr
        self.xcmd = bytearray( 2 )
        _ssd1306_base.__init__( self, size, background )

    def write_cmd( self, cmd ):
        "Hello"
        self.xcmd[ 0 ] = 0x80  # Co=1, D/C#=0
        self.xcmd[ 1 ] = cmd
        self.i2c.writeto( self.addr, self.xcmd )

    def write_framebuf( self ):
        "Hello"
        self.i2c.start()
        self.xcmd[ 0 ] = ( self.addr << 1 ) | 0x00
        self.xcmd[ 1 ] = 0x40
        self.i2c.write( self.xcmd )
        self.i2c.write( self.buffer )
        self.i2c.stop()


class ssd1306_spi( _ssd1306_base ):
    "Hello"

    def __init__( self, size, spi, dc, res, cs, background ):
        self.spi = spi
        self.cmd = bytearray( 2 )
        self.rate = 10 * 1024 * 1024
        self.dc = dc
        self.res = res
        self.cs = cs

        _ssd1306_base.__init__( self, size, background )              

        self.dc.write( 0 )
        self.res.write( 0 )
        self.cs.write( 1 )
        self.res.write( 1 )
        
    def write_cmd( self, cmd ):
        "Hwewllo"
        self.spi.init( baudrate=self.rate, polarity=0, phase=0 )
        self.cs.write( 1 )
        self.dc.write( 0 )
        self.cs.write( 0 )
        self.spi.write( bytearray( [ cmd ] ) )
        self.cs.write( 1 )

    def write_framebuf( self ):
        "Hello"
        self.spi.init( baudrate=self.rate, polarity=0, phase=0 )
        self.cs.write( 1 )
        self.dc.write( 1 )
        self.cs.write( 0 )
        self.spi.write( self.buffer )
        self.cs.write( 1 )
