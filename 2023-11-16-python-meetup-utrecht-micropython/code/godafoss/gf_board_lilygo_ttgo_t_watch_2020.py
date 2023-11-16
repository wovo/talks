# ===========================================================================
#
# file     : gf_board_lilygo_ttgo_t_watch_2020.py
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

class board_lilygo_ttgo_t_watch_2020:

    """
    `lilygo_ttgo_t_watch_2020`_ watch
    
    .. _lilygo_ttgo_t_watch_2020: \\
        https://t-watch-document-en.readthedocs.io\\
        /en/latest/introduction/product/2020.html
    
    $insert_image( "lilygo_ttgo_t_watch_2020", 1, 300 )
    
    +-----------------+-----------------------------------------------------+
    | uC              | ESP32 with PSRAM                                    |
    +-----------------+-----------------------------------------------------+
    | LCD             | ST7789 240 x 240 color                              |
    +-----------------+-----------------------------------------------------+
    | Touch           | FT6236                                              |
    +-----------------+-----------------------------------------------------+
    | Power           | AXP202                                              |
    +-----------------+-----------------------------------------------------+
    | Audio           | MAX98357A                                           |
    +-----------------+-----------------------------------------------------+
    | Accelerometer   | BMA423                                              |
    +-----------------+-----------------------------------------------------+
    | Real Time Clock | PCF8563                                             |
    +-----------------+-----------------------------------------------------+
    | USB             | micro, CH9102, boot / reset circuit                 |
    +-----------------+-----------------------------------------------------+

    This is an wrist watch with an ESP32 with PSRAM, a small LiPo accu,
    a touch LCD, a vibration/buzzer motor, an accelerometer, 
    i2s audio with a small speaker, and an RTC.
    
    Pressing the button on the side for 5 seconds powers the watch down.
    When powered down, pressing it for 2 seconds restarts it.
    If this button can be read by the ESP32 I have not found out how.
    
    The names in the table below are available as attributes.    

    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |  18 | i2c_sda (power and accelerometer)                              |
    +-----+----------------------------------------------------------------+
    |  19 | i2c_scl (power and accelerometer)                              |
    +-----+----------------------------------------------------------------+
    |  35 | power_int_pin                                                  |
    +-----+----------------------------------------------------------------+
    |  39 | accelerometer_int_pin                                          |
    +-----+----------------------------------------------------------------+
    |  18 | tft_sclk                                                       |
    +-----+----------------------------------------------------------------+
    |  19 | tft_mosi                                                       |
    +-----+----------------------------------------------------------------+
    |   5 | tft_cs                                                         |
    +-----+----------------------------------------------------------------+
    |  27 | tft_dc                                                         |
    +-----+----------------------------------------------------------------+
    |  12 | tft_bl                                                         |
    +-----+----------------------------------------------------------------+
    |  23 | touch_i2c_sda                                                  |
    +-----+----------------------------------------------------------------+
    |  32 | touch_i2c_scl                                                  |
    +-----+----------------------------------------------------------------+
    |  38 | touch_int                                                      |
    +-----+----------------------------------------------------------------+
    |  25 | audio_i2s_ws                                                   |
    +-----+----------------------------------------------------------------+
    |  26 | audio_i2s_bck                                                  |
    +-----+----------------------------------------------------------------+
    |  33 | audio_i2s_dout                                                 |
    +-----+----------------------------------------------------------------+
    |   4 | buzzer_pin                                                     |
    +-----+----------------------------------------------------------------+
    |  13 | ir_pin                                                         |
    +-----+----------------------------------------------------------------+
    |  37 | rtc_pin                                                        |
    +-----+----------------------------------------------------------------+
    
    $macro_insert board lilygo_ttgo_t_watch_2020
    """

    # =======================================================================

    def __init__( self ):
    
        self.i2c_sda = 21
        self.i2c_scl = 22
        self.power_int_pin = 35
        self.accelerometer_int_pin = 39
        
        self.tft_sclk = 18
        self.tft_mosi = 19
        self.tft_cs = 5
        self.tft_dc = 27
        self.tft_bl = 12
        
        self.touch_i2c_sda = 23
        self.touch_i2c_scl = 32
        self.touch_int = 38
        
        self.audio_i2s_ws = 25
        self.audio_i2s_bck = 26
        self.audio_is2_dout = 33
        
        self.buzzer_pin = 4
        self.ir_pin = 13        
        self.rtc_pin = 37
        
        self.power_i2c_address = 0x35
        self.accelerometer_i2c_address = 0x18
        
        self._i2c = None
       
          
    # =======================================================================
       
    def display_spi( 
        self, 
        id: int = 1,
        baudrate = 30_000_000,
        polarity = 1,
        phase = 1       
    ) -> machine.SPI:
        """
        default (hard) SPI bus for the LCD
        """
        
        return machine.SPI(
            id,
            baudrate = baudrate,
            polarity = polarity,
            phase = phase,
            sck = machine.Pin( self.tft_sclk ),
            mosi = machine.Pin( self.tft_mosi ),
            miso = machine.Pin( 23 ) # dummy
        )
        
    # =======================================================================

    def display( 
        self,
        spi: machine.SPI = None
    ) -> canvas:
        """
        ST7789 240 x 240 color LCD
        
        After a restart the LCD is disabled and the backlight is off.
        The display constructor enables the LCD 
        and switches the backlight on.        
        """          
        self.display_enable()
        return gf.st7789( 
            size = gf.xy( 240, 240 ), 
            spi = spi if spi is not None else self.display_spi(),
            data_command = self.tft_dc,
            chip_select = self.tft_cs,
            backlight = self.tft_bl,
            invert = True,
        )
        
    # =======================================================================
    
    def i2c( self ) -> machine.I2C:
        """
        i2c bus for the power and accelerometer
        
        This function returns the i2c bus for the AXP202 power
        management chip and the BMA423 accelerometer.
        """        
        
        if self._i2c is None:
            self._i2c = machine.SoftI2C(
                scl = machine.Pin( self.i2c_scl ),
                sda  = machine.Pin( self.i2c_sda ),
                freq = 100_000
            )    
        return self._i2c

    # =======================================================================
    
    def display_enable( self ) -> None:
        """
        enable power to the LCD
        """
        
        i2c = self.i2c()  
        power_output_control = i2c.readfrom_mem( 
            self.power_i2c_address, 
            0x12, 
            1 
        )[ 0 ]
        power_output_control |= 4 # LDO2 enable
        i2c.writeto_mem( 
            self.power_i2c_address, 
            0x12, 
            bytes( [ power_output_control ] ) 
        )        
    
    # =======================================================================
    
    def touch_i2c( 
        self, 
        freq: int = 100_000 
    ) -> machine.I2C:
        """
        touch chip i2c bus
        """
        
        return machine.SoftI2C(
            scl = machine.Pin( self.touch_i2c_scl ),
            sda = machine.Pin( self.touch_i2c_sda ),
            freq = freq
        ) 
        
    # =======================================================================
    
    def touch( 
        self,
        i2c: machine.I2C = None
    ):
        """
        ft6236 touch chip
        """

        return gf.ft6236( i2c if i2c is not None else self.touch_i2c() )
    
    # =======================================================================
    
    def buzzer( self ) -> pin_out:
        """
        buzzer pin
        """

        return gf.make_pin_out( self.buzzer_pin )
        
    # =======================================================================

# ===========================================================================
