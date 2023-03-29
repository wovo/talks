# ===========================================================================
#
# file     : gf_st7567.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the st7567 LCD driver class.
#
# ===========================================================================

from micropython import const
import framebuf
import machine

from godafoss.gf_time import *
from godafoss.gf_xy import *
from godafoss.gf_pins import *
from godafoss.gf_canvas import *
from godafoss.gf_lcd_spi import *
from godafoss.gf_lcd_reset_backlight_power import *

SET_BIAS  =const(0xA2)
POWER_CTRL=const(0x28)
SET_BOOST =const(0xF8)
SOFT_RST  =const(0xE2)
SEG_DIR   =const(0xA0)
COM_DIR   =const(0xC0)
REGU_RATIO=const(0x20)
EVSET_MODE=const(0x81)
DISP_ONOFF=const(0xAE)
INV_DISP  =const(0xA6)#0:normal display 1:inverse
ALL_PIX_ON=const(0xA4)
SRTLIN_SET=const(0x40)#40~7F
PAGEAD_SET=const(0xB0)#b0~b8
COLHAD_SET=const(0x10)#0x10~0x1F
COLLAD_SET=const(0x00)#0x00~0x0F


# ===========================================================================

class st7567(
    canvas,
    lcd_spi,
    lcd_reset_backlight_power
):
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
    
    """
    
    def __init__( 
        self, 
        size, 
        spi, 
        data_command: [ int, pin_out, pin_in_out, pin_oc ],
        chip_select: [ int, pin_out, pin_in_out, pin_oc ] = None, 
        reset: [ int, pin_out, pin_in_out, pin_oc ] = None,
        backlight: [ int, pin_out, pin_in_out, pin_oc ] = None,
        power: [ int, pin_out, pin_in_out, pin_oc ] = None,
        background = colors.black, 
        invert = False,
        x_reverse = False,
        y_reverse = False,
        xy_swap = False,
        x_deadband = 0,
        elecvolt=0x1F,regratio=0x03,invX=0x00,invY=0x00,invdisp=0x00        
    ):
        canvas.__init__(
            self,
            size = size,
            is_color = False,
            background = background
        )

        lcd_spi.__init__(
            self,
            spi = spi,
            data_command = data_command,
            chip_select = chip_select,
        )
                    
        lcd_reset_backlight_power.__init__( 
            self, 
            reset = - make_pin_out( reset ), 
            backlight = backlight, 
            power = power,          
            reset_duration = 10,
            reset_wait = 120_000
        )
        
        self._buffer = bytearray((( self.size.y + 7 ) // 8 ) * self.size.x )
        self._framebuf = framebuf.FrameBuffer(
            self._buffer, self.size.x, self.size.y, framebuf.MONO_VLSB )
        
        self.EV=elecvolt
        self.RR=regratio
        self.invX=0x00 if(invX==0) else 0x01#0x00:MX=0 normal dir, 0x01:MX=1 reverse dir
        self.invY=0x00 if(invY==0) else 0x08#0x00:MY=0 0x08:MY=1
        self.invdisp=0x00 if(invdisp==0) else 0x01
        
        self.write_command(SOFT_RST)#optional, I think it's useless
        self.write_cmd(SET_BOOST)#set booster mode
        self.write_cmd(0x00)#boost: 0x00:x4 0x01:x5
        self.write_cmd(SET_BIAS|0x01)# 0:1/9 1:1/7
        self.write_cmd(EVSET_MODE)#put device into EV setting mode
        self.write_cmd(self.EV)#0x00~0x3F set contrast to 0x1f with last command
        self.write_cmd(REGU_RATIO|self.RR)#0x00~0x07 3.0~6.5
        self.write_cmd(POWER_CTRL|0x07)#7:{booster on,regulator on,follower on}
        self.write_cmd(INV_DISP|self.invdisp)#normal display
        self.write_cmd(ALL_PIX_ON|0x00)#0x00:normal display 0x01:all pixel on
        self.write_cmd(SEG_DIR|self.invX)#0:MX=0 normal dir, 1:MX=1 reverse dir
        self.write_cmd(COM_DIR|self.invY)#0x00:MY=0 0x08:MY=1 (may change to reverse y)
        
        time.sleep_ms(50)
        self.fill(0)
        self.show()
        self.write_cmd(DISP_ONOFF|0x01)#1:display on normal display mode        
                  
    # =======================================================================
    
    def write_cmd(
        self,
        cmd: int
    ) -> None:
        self.write_command( cmd )
      
    # =======================================================================

    def _flush_implementation( self ):
        
        self.write_cmd(DISP_ONOFF|0x00)
        self.write_cmd(SRTLIN_SET|0x00)
        colcnt=0
        pagcnt=0
        while (pagcnt<9):
            self.write_cmd(PAGEAD_SET|pagcnt)
            self.write_cmd(COLHAD_SET|0x00)
            self.write_cmd(COLLAD_SET|0x00)
            if(pagcnt<8):
                self.write_data(self.buffer[(128*pagcnt):(128*pagcnt+128)])
            else:
                while (colcnt<128):
                    colcnt+=1
                    self.write_data(b"\x00")
            pagcnt+=1
            self.write_cmd(DISP_ONOFF|0x01)
            
        return    
        
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
        
        self.write_command( self.cmd.RAMWR, buffer = self._buffer )                  
        
    # =======================================================================
        
    def _clear_implementation( 
        self,
        ink: color
    ):
        self._framebuffer.fill( self._encode( ink ) )
        
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
    
# ===========================================================================
 