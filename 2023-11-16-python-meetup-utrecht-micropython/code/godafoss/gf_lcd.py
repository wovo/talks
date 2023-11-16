# ===========================================================================
#
# file     : gf_lcd.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the generic color LCD driver.
#
# ===========================================================================

from micropython import const
import framebuf
import machine

from godafoss.gf_time import *
from godafoss.gf_report import *
from godafoss.gf_xy import *
from godafoss.gf_color import *
from godafoss.gf_pins import *
from godafoss.gf_canvas import *
from godafoss.gf_lcd_spi import *
from godafoss.gf_lcd_reset_backlight_power import *

@micropython.viper
def dma_setup(
    channel: uint,
    start : uint,
    end: uint,
    buf_len: uint,
    control: uint
):
    base = uint( 0x50000000 ) + channel * uint( 0x40 )
    ptr32( base + 0x00 )[ 0 ] = start
    ptr32( base + 0x04 )[ 0 ] = end
    ptr32( base + 0x08 )[ 0 ] = buf_len
    ptr32( base + 0x0C )[ 0 ] = control

# ===========================================================================
     
def _encode_565( a, b, c ):
    v = ( ( a >> 3 ) << 11 ) | ( ( b >> 2 ) << 5 ) | ( c >> 3 )
    return ( ( v & 0xFF ) << 8  ) | ( ( v >> 8 ) & 0xFF )


# ===========================================================================

class lcd( canvas, lcd_spi, lcd_reset_backlight_power ):
    """
    generic SPI color lcd driver
    
    :param chip: str
        driver chip name
        
        Supported driver chips are st7567, st7735, st7789 and ili9341.
           
    :param size: :class:`~godafoss.xy`
        size in pixels in x and y direction

    :param spi: machine.SPI
        SPI channel that connects to the driver chip

    :param data_command
        data / command pin to the driver chip

    :param chip_select
        SPI chip select pin to the driver chip (active low)

    :param reset
        reset pin to the driver chip (optional, active low)
        
        The constructor resets the driver chip.
        The lcd_reset_backlight_power:reset method can be used
        to reset the chip.        

    :param backlight
        backlight pin to the driver chip (optional, active high)
        
        The constructor enables the backlight.
        The lcd_reset_backlight_power:backlight method can be used
        to switch the power.        

    :param power
        power enable pin to the driver chip (optional, active high)
        
        The constructor enables power to the driver chip.
        The lcd_reset_backlight_power:power method can be used
        to switch the power.

    :param background: :class:`~godafoss.color`
        default background color (default: colors.black)
        
        This is the default for the clear() method.
        The inverse of the background is the default for writing
        a monochrome shape.

    :param invert: bool
        invert the luminosity of colors (default: False)

    :param mirror_x: bool
        mirror (reverse) x adressing (default: False)

    :param mirror_y: bool
        mirror (reverse) y adressing (default: False)

    :param swap_xy: bool
        swap the x and y addressing (default: False)

    :param color_order: str | None
        color order
    
        This parameter specifies order in which the colors must be stored
        in the chip to be displayed correctly on the LCD.
        The default is RGB, which is correct for most chips.
        For instancem, for a chip that swap the red and blue channels
        specify "BGR".

        In color mode, this driver uses a RAM canvas of 2 bytes per pixel, 
        which can be more than your target has available.
        In monochrome mode (color_order = None) it uses a RAM canvas 
        of 8 pixels per byte, but a downside is that flushing takes
        longer because data for the SPI transactions must
        be constructed on the fly.
        
    :param mechanisms: int
        the mechanism used for monochrome data transport
        
        This parameter selects the mechanism used by the flush
        method to transport data to the LCD when the LCD is
        use in monochrome mode.
        
        The default value of 0 uses a 4k lookup table.
        When this memory use is a problem, 1 can be specified.
        This setting uses a line buffer of 2 bytes per pixel in the x
        direction (256 bytes for 128 x 128 display) and calculates
        the data on the fly, which is much slower.
        
        For a RP2040 chip setting 2 uses a PIO engine to
        generate the data.
        This is fast and requires no buffer, but uses a PIO engine,
        and can only display the colors black and white.
        
        +------------------------------------------------------+
        | Raspberry Pi Pico RP2040 ST7735 color LCD 128 x 128  |
        +-----------------+--------------+---------------------+
        | use             | method       | flush takes         |
        +-----------------+--------------+---------------------+
        | color           | n.a.         | 80 ms               |
        +-----------------+--------------+---------------------+
        | monochrome      | 0            | 114 ms              |
        +-----------------+--------------+---------------------+
        | monochrome      | 1            | 374 ms              |
        +-----------------+--------------+---------------------+
        | monochrome      | 2            | 114 ms              |
        +-----------------+--------------+---------------------+

    :param offset: :class:`~godafoss.xy`
        offset of the displayed area
    
        LCD modules can have an margin of hidden pixels 
        to the left and top of the displayed area.
        This parameter is the offset of the first displayed pixel
        (default: xy(0,0)).          
    
    This class is a front-end for the drivers for various SPI color LCDs.
    """

    # =======================================================================

    def __init__( 
        self, 
        chip: str,
        size: xy, 
        spi: machine.SPI, 
        data_command: [ int, pin_out, pin_in_out, pin_oc ],
        chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
        reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
        backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
        power: [ int, pin_out, pin_in_out, pin_oc ] = None,
        background: color = colors.black, 
        color_order: str | None = "RGB",
        mechanism: int = 0,
        invert: bool = False,
        mirror_x: bool = False,
        mirror_y: bool = False,
        swap_xy: bool = False,
        offset = xy( 0, 0 ),
        x_deadband = 0    
    ):
        self._color_order = color_order
        self._invert = invert
        self._mirror_x = mirror_x
        self._mirror_y = mirror_y
        self._swap_xy = swap_xy
        self._offset = offset
        
        canvas.__init__(
            self,
            size = size,
            is_color = self._color_order is not None,
            background = background
        )

        lcd_reset_backlight_power.__init__( 
            self, 
            reset = - make_pin_out( reset ), 
            backlight = backlight, 
            power = power,
            
            # longest required reset:
            #     10 us low,
            #     120 ms wait for reset to effectuate
            # (ST7735 datasheet 9.16)
            reset_duration = 10,
            reset_wait = 120_000
        )
        
        lcd_spi.__init__(
            self,
            spi = spi,
            data_command = data_command,
            chip_select = chip_select,
        )
               
        if self.is_color:
        
            color_order = color_order.upper()
            if color_order == "RGB":
                self._encode = lambda c: _encode_565( c.red, c.green, c.blue )
                
            elif color_order == "RBG":
                self._encode = lambda c: _encode_565( c.red, c.blue, c.green )
                
            elif color_order == "GRB":
                self._encode = lambda c: _encode_565( c.green, c.red, c.blue )
                
            elif color_order == "GBR":
                self._encode = lambda c: _encode_565(  c.green, c.blue, c.red )
                 
            elif color_order == "BRG":
                self._encode = lambda c: _encode_565( c.blue, c.red, c.green )
                
            elif color_order == "BGR":
                self._encode = lambda c: _encode_565( c.blue, c.green, c.red )
                
            else:
                raise ValueError( "unsupported color order '%s'" % color_order )   
        
            self._buffer = bytearray( 
                2 * self.size.y * ( self.size.x + x_deadband ) )
            self._framebuffer = framebuf.FrameBuffer(
                self._buffer, 
                self.size.x + x_deadband, 
                self.size.y, 
                framebuf.RGB565 
            )
            
            self._flush_data_transport = \
               self._flush_data_transport_color                        
            
        else:    
            self._encode = lambda x: x
        
            self._buffer_size = \
                ( ( self.size.x + x_deadband ) * ( self.size.y ) + 7 ) // 8
            self._buffer = bytearray( self._buffer_size )
            self._framebuffer = framebuf.FrameBuffer(
                self._buffer, 
                self.size.x + x_deadband, 
                self.size.y, 
                framebuf.MONO_HLSB 
            )
            
            if mechanism == 0:
                
               # create fast-lookup for 8 pixels at a time
               # (uses 4k RAM)
               self._pixels = [ bytearray( 16 ) for _ in range( 256 ) ]
               for v in range( 256 ):
                    i = 0
                    m = 0x80
                    for _ in range( 8 ):
                        c = 0xFF if v & m != 0 else 0x00
                        self._pixels[ v ][ i ] = c                  
                        self._pixels[ v ][ i + 1 ] = c
                        m = m >> 1
                        i += 2
                        
               self._flush_data_transport = \
                   self._flush_data_transport_monochrome_lookup                        
                
            elif mechanism == 1:
                
               self._line_buffer = bytearray( 2 * self.size.x )
               self._flush_data_transport = \
                  self._flush_data_transport_monochrome_line_buffer                        
                
            elif mechanism == 2:
                
                # each GPIO pin has 2 registers, starting at 0x40014000
                # a register is 4 bytes, control is the 2nd register                
                io_addresses = (
                    0x40014000 + self._spi.sck * 8 + 4,
                    0x40014000 + self._spi.mosi * 8 + 4
                )
                self.spi_gpio = remember( io_addresses )
                self.make_fsm()                  
                self.spi_pio = remember( io_addresses )
                self.spi_gpio.restore()
        
                self._flush_data_transport = \
                    self._flush_data_transport_monochrome_rp2_pio
        
            else:
                raise ValueError( "undefined mechanism '%d'" % mechanism )                
            
        # get the chip-specific driver    
        name = "lcd_driver_%s" % chip
        try:
            exec( "from godafoss.gf_%s import %s" % ( name, name ) )
        except ImportError:
            raise ValueError( "unknown lcd chip '%s'" % chip )
        driver = eval( name )
        self._driver = driver( self )
        
    # =======================================================================
    
    def make_fsm( self ):
        import rp2
        
        @rp2.asm_pio(
            autopull=True,
            pull_thresh=32,
            sideset_init=rp2.PIO.OUT_HIGH,
            out_init=rp2.PIO.OUT_LOW,
            out_shiftdir = rp2.PIO.SHIFT_LEFT
        )
        
        def spi_cpha0():           
            out( pins, 1 )
            set( x, 15 )
            label( "bitloop" )
            nop().side( 0x0 )
            jmp( x_dec, "bitloop" ).side( 0x1 )
            
        sm_id = 0
        freq = 30_000_000
        self._sm = rp2.StateMachine(
            sm_id,
            spi_cpha0,
            2 * freq,
            sideset_base=machine.Pin( 18 ),
            out_base=machine.Pin( 19 ),
        )
        print( self._sm )
        self._sm.active(1)           
                
    # =======================================================================
    
    def _flush_data_transport_color( self ):
        self.write_command( self._driver.cmd.RAMWR, buffer = self._buffer )
      
    # =======================================================================
    
    @micropython.native      
    def _flush_data_transport_monochrome_lookup( self ):       
        self.write_command( self._driver.cmd.RAMWR )
        self._data_command.write( 1 )
        self._chip_select.write( 0 )
        
        _n = const( 8 )
        _m = const( _n * 16 )
        p = bytearray( _m )
        i = 0
        
        # optimization by avoiding lookup, ~ 10% faster
        pp = self._pixels
        ww = self._spi.write
        
        for b in self._buffer: 
            p[ i : i + 16 ] = pp[ b ]
            i += 16
            if i >= _m:
                ww( p )
                i = 0
                
        self._chip_select.write( 1 )        
      
    # =======================================================================
    
    #@micropython.native      
    def _flush_data_transport_monochrome_line_buffer( self ):       
        self.write_command( self._driver.cmd.RAMWR )
        self._data_command.write( 1 )
        self._chip_select.write( 0 )
        for y in range( self.size.y ):
            for x in range( self.size.x ):
                c = 0xFF if self._framebuffer.pixel( x, y ) else 0x00
                self._line_buffer[ 2 * x ] = c                  
                self._line_buffer[ 2 * x + 1 ] = c                  
            self._spi.write( self._line_buffer )         
        self._chip_select.write( 0 )
     
    # =======================================================================
    
    @micropython.viper
    def pio_put( self, d: uint ):
        ptr1 = ptr32( 0x50200004 )
        while ( ptr1[ 0 ] & ( 0x0F << 16 ) ) != 0:
            pass
        ptr = ptr32( 0x50200010 )
        ptr[ 0 ] = d   
    
    def _flush_data_transport_monochrome_rp2_pio_old( self ):       
        self.write_command( self._driver.cmd.RAMWR )

        self._data_command.write( 1 )
        self._chip_select.write( 0 )
                
        self.spi_pio.restore()
        
        n = 0
        d = 0
        put = self._sm.put
        for b in self._buffer:
            d = d << 8 | b
            n += 1
            if n == 4:
                # put( d )
                self.pio_put( d )
                # sleep_us( 100 )
                # self._sm.put( d )
                d = 0
                n = 0
            #self._sm.put( b << 24 )
                    
        while self._sm.tx_fifo() != 0:
            pass   
        sleep_us( 1_000 )    
            
        self.spi_gpio.restore()       

        self._chip_select.write( 1 )     
      
    # =======================================================================
    
    def _flush_data_transport_monochrome_rp2_pio( self ):
        import ctypes, uctypes
        
        self.write_command( self._driver.cmd.RAMWR )

        self._data_command.write( 1 )
        self._chip_select.write( 0 )
                
        self.spi_pio.restore()

        dma_setup(
            0,
            uctypes.addressof( self._buffer ),
            0x50200010 ,
            self._buffer_size // 4,
            ( 1 << 22 ) | (0x0 << 15 ) | ( 1 << 4 ) | ( 2 << 2 ) | 1
        )                
                    
        while self._sm.tx_fifo() != 0:
            pass
          

        self.spi_gpio.restore()       

        self._chip_select.write( 1 )     
      
    # =======================================================================
      
    @report  
    def _flush_implementation(
        self,
        forced: bool
    ) -> None:     
        
        x_end = self.size.x - 1 + self._offset.x
        self.write_command( self._driver.cmd.CASET, [
            0x00, self._offset.x, 
            x_end // 256, x_end % 256
        ])
        
        y_end = self.size.y - 1 + self._offset.y
        self.write_command( self._driver.cmd.RASET, [ 
            0x00, self._offset.y,
            y_end // 256, y_end % 256
        ])
        
        self._flush_data_transport()     
        
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
