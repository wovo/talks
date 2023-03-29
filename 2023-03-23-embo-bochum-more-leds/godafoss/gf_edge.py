# ===========================================================================
#
# file     : gf_edge.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file provides the 'abstract' interfaces that my 'edge' lab 
# target boards provide: for each target, a 14-pin header provides
# ground, power, and 8 data pins (p0..p7).
# Some of these pins also function as soft and hards SPI and I2C 
# interfaces.
# Some pins have dedicated functions when interfacing to 
# typical peripherals using soft and hard SPI and I2C, and
# for peripheral pins like chipo_select, data_command, reset
# background, etc.
#
# ===========================================================================

import godafoss as gf
import machine, os
from machine import Pin


# ===========================================================================

class edge:
    
    soft = gf.spi.soft
    hard = gf.spi.hard

    # =======================================================================

    def __init__(
        self,
        silent = False
    ):
        uname = os.uname()
        self.system = "?"
        self.pins = None
        
        if uname.sysname == "rp2":
            self._rp2()
            
        elif uname[ 0 ] == "esp32":
        
            if uname[ 4 ] == "ESP32C3 module with ESP32C3":
                self._esp32c3()
            
            elif uname[ 4 ] == "LOLIN_C3_MINI with ESP32-C3FH4":
                self._esp32_lolin_c3_mini()
                
            else:
                self._esp32()
                
        elif uname[ 0 ] == "esp8266":      
            self._esp8266()                 
    
        elif uname[ 0 ] == "mimxrt":
            self._mimxrt()
            
        if not silent:
            print( "edge board is", self.system )
            print( "edge pins are", self.pins )
            
        self.p0, self.p1, self.p2, self.p3, self.p4, \
            self.p5, self.p6, self.p7 = self.pins
        
        # (soft) SPI        
        self.spi_sck = self.p0
        self.spi_mosi = self.p1
        self.spi_miso = self.p2

        # lcd
        self.chip_select = self.p3
        self.data_command = self.p4
        self.reset = self.p5
        self.backlight = self.p6

        # (soft) I2C
        self.i2c_scl = self.p6
        self.i2c_sda = self.p7

        # neopixels
        self.neopixel_data = self.p5
        
    # =======================================================================
    #
    # utilities
    #
    # =======================================================================

    def port( self ):
        return gf.port_out( self.pins )
        # p0, p1, p2, p3, p4, p5, p6, p7 )

    # =======================================================================

    def spi( 
        self,
        frequency = 10_000_000,
        polarity = 1,
        phase = 1,
        mechanism: int = 1,        
    ):
        return gf.spi( 
            frequency = frequency,
            polarity = polarity,
            phase = phase,
            sck = self.spi_sck,
            mosi = self.spi_mosi,
            miso = self.spi_miso,
            mechanism = mechanism
        )
    
    # =======================================================================

    def _soft_spi( 
        self,
        baudrate = 10_000_000,
        polarity = 1,
        phase = 1,        
    ):
        return machine.SoftSPI( 
            baudrate = baudrate,
            polarity = polarity,
            phase = phase,
            sck = machine.Pin( self.spi_sck ),
            mosi = machine.Pin( self.spi_mosi ),
            miso = machine.Pin( self.spi_miso )
        )
    
    # =======================================================================

    def _hard_spi(
        self,
        baudrate = 20_000_000,
        polarity = 1,
        phase = 1, 
    ):
        return machine.SPI( 
            baudrate = baudrate,
            polarity = 1,
            phase = 1,
            sck = machine.Pin( self.spi_sck ),
            mosi = machine.Pin( self.spi_mosi ),
            miso = machine.Pin( self.spi_miso )
        )

    # =======================================================================

    def _hard_spi(
        self,
        baudrate = 20_000_000,
        polarity = 1,
        phase = 1, 
    ):
        return gf.spi( 
            baudrate = baudrate,
            polarity = 1,
            phase = 1,
            sck = self.spi_sck,
            mosi = self.spi_mosi,
            miso = self.spi_miso
        )

    # =======================================================================

    def soft_i2c(
        self,
        frequency = 100_000
    ):
        return machine.SoftI2C(
            freq = frequency,
            scl = machine.Pin( self.i2c_scl ),
            sda = machine.Pin( self.i2c_sda )
        ) 
    
    # =======================================================================

    def hard_i2c(
        self,
        frequency = 100_000
    ):        
        return machine.SoftI2C(
            freq = frequency,            
            scl = machine.Pin( self.i2c_scl ),
            sda = machine.Pin( self.i2c_sda )
        )                            

    # =======================================================================
    #
    # specializers for the various targets
    #
    # =======================================================================

    def _rp2( self ):
    
        v = gf.gpio_adc( 28 ).read().scaled( 0, 65535 )
        print( v )
    
        # 10k, 10k
        if gf.within( v, 31000, 35000 ):

            self.system = "original RP2040 rp2 or rp2w"
            self.pins = ( 18, 19, 16, 17, 26, 27, 13 , 12 )

        
        # 10k, 15k        
        elif gf.within( v, 24000, 28000 ): 

            self.system = "01Space RP2040-0.42 OLED"
            self.pins = ( 20, 24, 25, 26, 5, 6, 4, 3 )

        else:
            print( "rp2 unrecognized adc( 28 ) = ", v )           
        

    # =======================================================================
    
    def _esp32( self ):
    
        # differentiate according to the resistor divide on analog input 0
        v = gf.gpio_adc( 0 ).read()
    
        # 1k / 10 k -> 1/11 or around 9 of 100
        if ( v > 5 ) and ( v < 15 ):
            self.system = "ESP32- TTGO T-DISPLAY with 240x135 color LCD"
            self.pins = ( 21, 22, 17, 2, 15, 13, 12, 17 )

        else:    
            self.system = "generic ESP32"
            self.pins = ( 14, 13, 12, 15, 33, 21, 18, 19 )   


    # =======================================================================
    
    def _esp32c3( self ):
    
        v = gf.gpio_adc( 0 ).read().scaled( 0, 65535 )
        print( v )
    
        # 10k, 15k
        # ADC doesn't seem to work??
        if True:
        # if gf.within( v, 26000, 26400 ):    
    
            self.system = "01Space ESP32-C3-0.42 OLED"
            self.pins = ( 3, 4, 5, 6, 7, 8, 6, 5 )
       
        else:
            print( "esp32c3 unrecognized adc( 0 ) = ", v )      


    # =======================================================================
    
    def _esp32c3_lolin_c3_mini( self ):
    
        v = gf.gpio_adc( 0 ).read().scaled( 0, 65535 )
        print( v )
       
        system = "?"


    # =======================================================================
    
    def _esp8266( self ):
    
        self.system = "generic ESP8266"
        self.pins = ( 3, 3, 3, 3, 3, 3, 1, 2 )          


    # =======================================================================
        
    def _mimxrt( self ):
        
        self.system = "Teensy 4.1"
        self.pins = ( 27, 26, 1, 17, 18, 19, 20, 21 )
            
    # =======================================================================
    
# ===========================================================================
            