# ===========================================================================
#
# file     : gf_ssd1309.py
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
import machine
import framebuf

from godafoss.gf_xy import *
from godafoss.gf_make_pins import *
from godafoss.gf_canvas import *
from godafoss.gf_lcd_reset_backlight_power import *
from godafoss.gf_lcd_spi import *


# ===========================================================================

class _ssd1309_base( canvas ):
    """
    ssd1309 spi/i2c b/w oled display driver
    """

    # Command constants from display datasheet
    CONTRAST_CONTROL = const(0x81)
    ENTIRE_DISPLAY_ON = const(0xA4)
    ALL_PIXELS_ON = const(0XA5)
    INVERSION_OFF = const(0xA6)
    INVERSION_ON = const(0XA7)
    DISPLAY_OFF = const(0xAE)
    DISPLAY_ON = const(0XAF)
    NOP = const(0xE3)
    COMMAND_LOCK = const(0xFD)
    CHARGE_PUMP = const(0x8D)

    # Scrolling commands
    CH_SCROLL_SETUP_RIGHT = const(0x26)
    CH_SCROLL_SETUP_LEFT = const(0x27)
    CV_SCROLL_SETUP_RIGHT = const(0x29)
    CV_SCROLL_SETUP_LEFT = const(0x2A)
    DEACTIVATE_SCROLL = const(0x2E)
    ACTIVATE_SCROLL = const(0x2F)
    VSCROLL_AREA = const(0xA3)
    SCROLL_SETUP_LEFT = const(0x2C)
    SCROLL_SETUP_RIGHT = const(0x2D)

    # Addressing commands
    LOW_CSA_IN_PAM = const(0x00)
    HIGH_CSA_IN_PAM = const(0x10)
    MEMORY_ADDRESSING_MODE = const(0x20)
    COLUMN_ADDRESS = const(0x21)
    PAGE_ADDRESS  = const(0x22)
    PSA_IN_PAM = const(0xB0)
    DISPLAY_START_LINE = const(0x40)
    SEGMENT_MAP_REMAP  = const(0xA0)
    SEGMENT_MAP_FLIPPED = const(0xA1)
    MUX_RATIO = const(0xA8)
    COM_OUTPUT_NORMAL = const(0xC0)
    COM_OUTPUT_FLIPPED = const(0xC8)
    DISPLAY_OFFSET = const(0xD3)
    COM_PINS_HW_CFG = const(0xDA)
    GPIO = const(0xDC)

    # Timing and driving scheme commands
    DISPLAY_CLOCK_DIV = const(0xd5)
    PRECHARGE_PERIOD = const(0xd9)
    VCOM_DESELECT_LEVEL = const(0xdb)
    
    class commands:
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

    def __init__(
        self,
        size: xy,
        background: bool
    ) ->  None:

        canvas.__init__( 
            self, 
            size = size,
            is_color = False,
            background = background
        )
        self._buffer = bytearray((( self.size.y + 7 ) // 8 ) * self.size.x )
        self._framebuf = framebuf.FrameBuffer(
            self._buffer, self.size.x, self.size.y, framebuf.MONO_VLSB )
                    
        for cmd in (
            self.DISPLAY_OFF, 
            self.DISPLAY_CLOCK_DIV, 0x80,
            self.MUX_RATIO, self.size.y - 1,
            self.DISPLAY_OFFSET, 0x00,
            self.DISPLAY_START_LINE,
            self.CHARGE_PUMP, 0x14,
            self.MEMORY_ADDRESSING_MODE, 0x00, 
            self.SEGMENT_MAP_FLIPPED,
            self.COM_OUTPUT_FLIPPED,
            self.COM_PINS_HW_CFG, 0x02 if (self.size.y == 32 or self.size.y == 16) and (self.size.x != 64)
                else 0x12,
            self.CONTRAST_CONTROL, 0xFF,
            self.PRECHARGE_PERIOD, 0xF1,
            self. VCOM_DESELECT_LEVEL, 0x40,            
            self.ENTIRE_DISPLAY_ON, # output follows RAM contents
            self.INVERSION_OFF, # not inverted
            self.DISPLAY_ON
        ):
            self.write_command(cmd) 
           
        self.clear()
        self.flush()
        
    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: xy,
        ink: bool
    ) -> None:
        self._framebuf.pixel(
            location.x,
            location.y,
            ink
        )           

    # =======================================================================
    
    def _clear_implementation(
        self,
        ink
    ) -> None:
        self._framebuf.fill( 0xFF if ink else 0x00 )

    # =======================================================================

    def write_command(
        self,
        cmd: int
    ) -> None:
        """
        write a command byte to the chip
        """
        raise NotImplementedError
               
    # =======================================================================

    def _flush_implementation( self ) -> None:
        
        # the active area is x-centered
        x0 = ( 128 - self.size.x ) // 2 
        x1 = x0 + self.size.x - 1
            
        self.write_command( self.commands.set_col_addr )
        self.write_command( x0 )
        self.write_command( x1 )
        self.write_command( self.commands.set_page_addr )
        self.write_command( 0 )
        self.write_command( ( self.size.y // 8 ) - 1 )
        self._write_framebuf()

    # =======================================================================

# ===========================================================================


class ssd1309_i2c( _ssd1309_base ):
    """
    ssd1306 i2c monochrome oled display driver
    
    :param size: (:class:`~godafoss.xy`)
        horizontal and vertical size, in pixels
        
    :param i2c: (machine.I2C)
        i2c bus that connects to the chip
    
    :param background: (bool)
        background 'color', default (False) is off
    
    :param address: (int)
        7-bit i2c slave address, default is 0x3C

    This is an i2c driver for the i2c ssd1306 monochrome oled controller.
    This chip is used in various cheap oled displays and modules.
    
    #$insert_image( "ssd1306-i2c", 1, 200 )
    
    $macro_insert canvas_monochrome    
    """

    # =======================================================================

    def __init__( 
        self, 
        size: xy, 
        i2c: machine.I2C, 
        background = False, 
        address = 0x3C
    ) -> None:
        self._i2c = i2c
        self._address = address
        self._cmd = bytearray( 2 )
        _ssd1309_base.__init__(
            self,
            size = size,
            background = background
        )

    # =======================================================================

    def write_command( 
        self, 
        cmd: int 
    ) -> None:
        """
        write a command byte to the chip
        
        :param command: (int)
            the command byte to be send to the chip
        
        This method writes a single command byte to the chip.
        """
        
        self._cmd[ 0 ] = 0x80  # Co=1, D/C#=0
        self._cmd[ 1 ] = cmd
        self._i2c.writeto( self._address, self._cmd )

    # =======================================================================

    def _write_framebuf( self ) -> None:
        self._i2c.start()
        self._cmd[ 0 ] = ( self._address << 1 ) | 0x00
        self._cmd[ 1 ] = 0x40 # set_disp_start_line?
        self._i2c.write( self._cmd )
        self._i2c.write( self._buffer )
        self._i2c.stop()
        
    # =======================================================================        


#============================================================================

class ssd1309_spi(
    lcd_reset_backlight_power, 
    lcd_spi,
    _ssd1309_base
):
    """
    ssd1309 spi monochrome oled display driver
    
    :param size: (:class:`~godafoss.xy`)
        horizontal and vertical size, in pixels
        
    :param spi: (machine.SPI)
        spi bus that connects to the chip (miso not used)
    
    :param data_command: ($macro_insert make_pin_out_types )
        dc (data/command) pin of the chip 
        
    :param chip_select: ($macro_insert make_pin_out_types )
        cs (chip select) pin of the chip   

    :param reset: (None, $macro_insert make_pin_out_types )
        reset pin of the chip, active low;
        optional, the pin can be connected to Vcc (3.3V).
    
    :param background: (bool)
        background 'color', default (False) is off
    
    This is a spi driver for the ssd1306 monochrome oled controller.
    This chip is used in various cheap oled displays and modules.
    
    #$insert_image( "ssd1306-spi", 1, 200 )
    
    $macro_insert canvas_monochrome      
    """
    
    # =======================================================================

    def __init__( 
        self, 
        size: xy, 
        spi: machine.SPI, 
        data_command: [ int, pin_out, pin_in_out, pin_oc ], 
        chip_select: [ int, pin_out, pin_in_out, pin_oc ], 
        reset: [ int, pin_out, pin_in_out, pin_oc ] = None, 
        background = False 
    ) -> None:
        lcd_reset_backlight_power.__init__(
            self,
            reset = - make_pin_out( reset ),
            backlight = None,
            power = None
        ) 
        lcd_spi.__init__(
            self,
            spi = spi,
            data_command = data_command,
            chip_select = chip_select
        )         
        _ssd1309_base.__init__(
            self, size = size,
            background = background
        )

    # =======================================================================
    
    def _write_framebuf( self ) -> None:
        self.write_command( None, buffer = self._buffer )

    # =======================================================================
    
# ===========================================================================