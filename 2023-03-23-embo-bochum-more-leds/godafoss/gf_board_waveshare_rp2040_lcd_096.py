# ===========================================================================
#
# file     : gf_board_waveshare_rp2040_lcd_096.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains board-specific things.
#
# ===========================================================================

import godafoss as gf
import machine


# ===========================================================================

class board_ttgo_txx_display:

    """
    https://www.waveshare.com/rp2040-lcd-0.96.htm
    
    should use hard spi
    """

    def __init__( self ):
   
        self.i2c_scl = 21
        self.i2c_sda = 22
        
        self.spi_miso = 2 # dummy
        self.spi_mosi = 19
        self.spi_sclk = 18
        
        self.tft_cs = 5
        self.tft_dc = 16
        self.tft_rst = 23
        self.tft_bl = 4
        
        self.button1 = 35
        self.button2 = 0
        
    def i2c( self ):
        return machine.SoftI2C(
            scl = machine.Pin( self.i2c_scl, machine.Pin.OUT ),
            sda = machine.Pin( self.i2c_sda, machine.Pin.OUT )
        ) 
        
    def spi( 
        self, 
        baudrate = 10_000_000,
        polarity = 1,
        phase = 1       
    ):
        return machine.SoftSPI( 
            baudrate = baudrate,
            polarity = polarity,
            phase = phase,
            sck = machine.Pin( self.spi_sclk, machine.Pin.OUT ),
            mosi = machine.Pin( self.spi_mosi, machine.Pin.OUT ),
            miso = machine.Pin( self.spi_miso, machine.Pin.IN )
        )
        
    def display( self ):
        return gf.st7789_monochrome( 
            size = gf.xy( 135, 240 ), 
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            reset = self.tft_rst,
            backlight = self.tft_bl,
            offset = gf.xy( 52, 40 )
        )
        
# ===========================================================================
