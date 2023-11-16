# ===========================================================================
#
# file     : gf_board_lilygo_ttgo_t_dongle_s3.py
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

class board_lilygo_ttgo_t_dongle_s3:

    """
    `lilygo_ttgo_t_dongle_s3`_ board
    
    .. _lilygo_ttgo_t_dongle_s3: \\
        https://github.com/Xinyuan-LilyGO/T-Dongle-S3
    
    $insert_image( "lilygo_ttgo_t_dongle_s3", 1, 300 )
    
    +-----------+--------------------------------------------------------+
    | uC        | ESP32                                                  |
    +-----------+--------------------------------------------------------+
    | OLED      | ST7735 80 x 160 color                                  |
    +-----------+--------------------------------------------------------+
    | USB       | A                                                      |
    +-----------+--------------------------------------------------------+

    This is an ESP32-S3 (dual RISC V) dongle with a 80 x 160 SPI color LCD, 
    a reset button, a neopixel and an SD card slot
    (hidden inside the USB A connector).
    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |  35 | button1_pin                                                    |
    +-----+----------------------------------------------------------------+
    |   0 | button2_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  18 | spi_sclk                                                       |
    +-----+----------------------------------------------------------------+
    |  19 | spi_mosi                                                       |
    +-----+----------------------------------------------------------------+
    |   5 | tft_cs                                                         |
    +-----+----------------------------------------------------------------+
    |  16 | tft_dc                                                         |
    +-----+----------------------------------------------------------------+
    |  23 | tft_rst                                                        |
    +-----+----------------------------------------------------------------+
    |   4 | tft_bl                                                         |
    +-----+----------------------------------------------------------------+
    
    $macro_insert board lilygo_ttgo_t_display
    """

    # =======================================================================

    def __init__( self ):
        self.button1_pin = 35
        self.button1_pin = 0
        self.spi_sclk = 18
        self.spi_mosi = 19
        self.tft_cs = 5
        self.tft_dc = 16
        self.tft_rst = 23
        self.tft_bl = 4
          
    # =======================================================================
       
    def spi( 
        self, 
        baudrate = 1_000_000,
        polarity = 1,
        phase = 1       
    ):
        """
        the (hard) SPI bus
        """
        
        return machine.SPI(
            1,
            baudrate = baudrate,
            polarity = polarity,
            phase = phase,
            sck = machine.Pin( self.spi_sclk ),
            mosi = machine.Pin( self.spi_mosi ),

            # dummy, the default MISO pin is used for the tft_rst
            miso = machine.Pin( 23 )
        )
        
    # =======================================================================

    def display_monochrome( self ):
        """
        the LCD (monochrome driver)
        """        
        return gf.lcd(
            chip = "st7789",
            size = gf.xy( 135, 240 ), 
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            reset = self.tft_rst,
            backlight = self.tft_bl,
            margin = gf.xy( 51, 40 ),
            x_deadband = 0,
            color_order = None,
            # lookup_table = False
        )
        
    # =======================================================================

    def display( self ):
        """
        the LCD (color driver)
        """        
        return gf.lcd(
            chip = "st7789",
            size = gf.xy( 135, 240 ), 
            spi = self.spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            reset = self.tft_rst,
            backlight = self.tft_bl,
            margin = gf.xy( 52, 40 )
        )
        
    # =======================================================================
        
# ===========================================================================
