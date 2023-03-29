# ===========================================================================
#
# file     : gf_board_sunton_esp32_2432s028.py
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

class board_sunton_esp32_2432s028:

    """
    sunton_sp32_2432s028 board
    
    
    $insert_image( "sunton_esp32_2432s028_front", 1, 200, width = 45 )
    $insert_image( "sunton_esp32_2432s028_back", 1, 200, width = 45 )
    
    +-----------+--------------------------------------------------------+
    | uC        | ESP32                                                  |
    +-----------+--------------------------------------------------------+
    | LCD       | ILI9341 240 * 430 color                                |
    +-----------+--------------------------------------------------------+
    | touch     | XPT2046 (resistive)                                    |
    +-----------+--------------------------------------------------------+
    | USB       | micro, CH340, boot & reset circuit,                    |
    |           | linear regulator                                       |
    +-----------+--------------------------------------------------------+
    | LED       | RGB leds                                               |
    +-----------+--------------------------------------------------------+
    | Sound     | filter, SC8002B 3W aplifier, 2 pin connector           |
    +-----------+--------------------------------------------------------+
    | LDR       | analog input                                           |
    +-----------+--------------------------------------------------------+
    | buttons   | boot, reset                                            |
    +-----------+--------------------------------------------------------+
    | misc.     | boot & reset buttons, SD card,                         |
    |           | connector, single-wire connector                       |
    +-----------+--------------------------------------------------------+

    This is an ESP32 board with a color LCD with touch, RGB leds,
    buttons for bootmode and reset, a LiPo connector and
    simple charge circuit (with linear regulators), a speaker interface,
    
    PSRAM??
    
    The names in the table below are available as attributes.
    Note that the touch chip, the LCD and the SD card use separate
    SPI busses.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |   4 | red_led_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  16 | green_led_pin                                                  |
    +-----+----------------------------------------------------------------+
    |  17 | blue_led_pin                                                   |
    +-----+----------------------------------------------------------------+
    |  26 | speaker_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  34 | ldr_pin                                                        |
    +-----+----------------------------------------------------------------+
    |  14 | tft_sclk_pin                                                   |
    +-----+----------------------------------------------------------------+
    |  13 | tft_mosi_pin                                                   |
    +-----+----------------------------------------------------------------+
    |  12 | tft_miso_pin                                                   |
    +-----+----------------------------------------------------------------+
    |   2 | tft_rs_pin                                                     |
    +-----+----------------------------------------------------------------+
    |  15 | tft_cs_pin                                                     |
    +-----+----------------------------------------------------------------+
    |  33 | xpt2046_cs_pin                                                 |
    +-----+----------------------------------------------------------------+
    |  33 | xpt2046_cs_pin                                                 |
    +-----+----------------------------------------------------------------+
    |  33 | xpt2046_cs_pin                                                 |
    +-----+----------------------------------------------------------------+
    |  33 | xpt2046_cs_pin                                                 |
    +-----+----------------------------------------------------------------+
    |  33 | xpt2046_cs_pin                                                 |
    +-----+----------------------------------------------------------------+
    |     | i2c_scl_pin                                                    |
    +-----+----------------------------------------------------------------+
    |     | i2c_sda_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  21 | bootmode_pin                                                   |
    +-----+----------------------------------------------------------------+
    
    $macro_insert board sunton_esp32_2432s028
    
    http://www.jczn1688.com/zlxz
    """


    def __init__( self ):
        
        self.red_led_pin = 4
        self.green_led_pin = 16
        self.blue_led_pin = 17
        
        self.speaker_pin = 26
        self.ldr_pin = 34
        self.boot_pin = 0        
   
        self.touch_sclk = 25
        self.touch_mosi = 32
        self.touch_miso = 39
        self.touch_cs = 33
        self.touch_irq = 36
        
        self.tft_sclk = 14
        self.tft_mosi = 13
        self.tft_miso = 12
        self.tft_rs = 2
        self.tft_cs = 15
        self.tft_bl = 21
                 
        self.sd_sclk = 18
        self.sd_mosi = 23
        self.sd_miso = 19
        self.sd_cs = 5
        
    def touch( self ):
        spi = machine.SoftSPI( 
            baudrate = 10_000,
            sck = machine.Pin( self.touch_sclk ),
            mosi = machine.Pin( self.touch_mosi ),
            miso = machine.Pin( self.touch_miso )
        )
        return gf.xpt2046(
            spi = spi,
            cs = self.touch_cs
        )        
        
    def display_monochrome( self ):
        spi = machine.SPI(
            1,
            baudrate = 30_000,
            sck = machine.Pin( self.tft_sclk ),
            mosi = machine.Pin( self.tft_mosi ),
            miso = machine.Pin( self.tft_miso )
        )        
        return gf.lcd(
            chip = "ili9341",
            size = gf.xy( 240, 320 ), 
            spi = spi,
            data_command = self.tft_rs,
            chip_select = self.tft_cs,
            backlight = self.tft_bl,
            color_order = None,
            mechanism = 0
        )
        
# ===========================================================================
