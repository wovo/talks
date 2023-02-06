# ===========================================================================
#
# file     : gf_pcd8544.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the pcd8544 LCD driver class.
#
# ===========================================================================

from micropython import const
import framebuf
import machine

from godafoss.gf_xy import *
from godafoss.gf_pins import *
from godafoss.gf_make_pins import *
from godafoss.gf_canvas import *
from godafoss.gf_lcd_reset_backlight_power import *
from godafoss.gf_lcd_spi import *


# ===========================================================================

class pcd8544( 
    canvas, 
    lcd_reset_backlight_power, 
    lcd_spi 
):
    """
    pcd8544 SPI b/w lcd controller driver
    
    $macro_insert lcd_reset_backlight_power_functionality    
    
    :param size: (:class:`~godafoss.xy`)
        horizontal and vertical size, in pixels
        
    :param spi: (machine.SPI)
        spi bus (miso not used)
        
    :param data_command: ($macro_insert make_pin_out_types)
        dc (data/command) pin of the chip
        
    :param cs: ($macro_insert make_pin_out_types)
        cs (chip select) pin of the chip
        
    $macro_insert lcd_reset_backlight_power_parameters
        
    :param background: (bool)
        background 'color', default (False) is off (white-ish)
    
    This is a driver for a pcd8544 black & white lcd controller.
    This chip was used with an 84 x 48 lcd in the once-popular 
    Nokia model 5110  telephone, 
    hence it is often called a (Nokia) 5110 lcd.
    This type of lcd is cheap and available from lots of sources,
    but the quality is often low (dead-on-arrival), 
    and the pinout varies.
    
    $insert_image( "pcf8544", 1, 200 )
    
    The pcb module shown has a backlight pin that must be connected
    to the (3.3V) power via a suitable resistor (330 Ohm is OK).
    
    $macro_insert lcd_reset_backlight_power_functionality
    
    $macro_insert canvas_monochrome
    """
    
    # =======================================================================    

    class _commands:   
        """chip commands"""
    
        # common
        FUNCTION_SET     = const( 0x20 ) # 0 basic, 1 extended
        
        # basic
        DISPLAY_CONTROL  = const( 0x08 )
        BANK_ADDR        = const( 0x40 ) # y pos, by 8 rows (0~5 )    
        COL_ADDR         = const( 0x80 ) # x pos (0~83 )
        
        # extended
        TEMP_CONTROL     = const( 0x04 )
        SET_BIAS         = const( 0x10 )
        SET_VOP          = const( 0x80 )
    
    # =======================================================================    

    def __init__( 
        self, 
        size: xy, 
        spi: machine.SPI, 
        data_command: [ int, pin_out, pin_in_out, pin_oc ],
        chip_select: [ int, pin_out, pin_in_out, pin_oc ],
        reset: [ None, int, pin_out, pin_in_out, pin_oc ] = None, 
        backlight: [ None, int, pin_out, pin_in_out, pin_oc ] = None, 
        power: [ None, int, pin_out, pin_in_out, pin_oc ] = None,
        background: bool = False
    ) -> None:
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
            power = power
        ) 
        lcd_spi.__init__( 
            self, 
            spi = spi, 
            data_command = data_command, 
            chip_select = chip_select
        ) 

        self._buffer = bytearray(( self.size.y // 8 ) * self.size.x )
        self._framebuf = framebuf.FrameBuffer(
            self._buffer, self.size.x, self.size.y, framebuf.MONO_VLSB 
        )    
        
        # inlitialize the chip
        
        # select exteded instruction set
        self.write_command( self._commands.FUNCTION_SET    | 0x01 )  
        
        # Vop = 110000
        self.write_command( self._commands.SET_VOP         | 0x48 ) 

        # TCx = 10
        self.write_command( self._commands.TEMP_CONTROL    | 0x02 )  
        
        # BSx = 011
        self.write_command( self._commands.SET_BIAS        | 0x03 )  
        
        # select basic instruction set
        self.write_command( self._commands.FUNCTION_SET    | 0x00 )  
        
        # normal mode = 100
        self.write_command( self._commands.DISPLAY_CONTROL | 0x04 )  
        
    # =======================================================================    

    def _write_pixel_implementation( 
        self, 
        location: xy, 
        ink: bool
    ) -> None:
        """
        write to a single pixel
        """
               
        self._framebuf.pixel( 
            location.x, 
            location.y, 
            ink
        )
        
    # =======================================================================    

    def _flush_implementation( self ) -> None:
        """
        flush the framebuffer to the display
        """
        
        # set write pointer(s); write pixel data
        self.write_command( self._commands.COL_ADDR  | 0 )
        self.write_command( self._commands.BANK_ADDR | 0, self._buffer )

    # =======================================================================    

    def _clear_implementation( 
        self, 
        ink: bool
    ) -> None:
        """
        clear the framebufer
        """

        self._framebuf.fill( 0xFF if ink else 0x00 )      
        
    # =======================================================================
         
# ===========================================================================
