# ===========================================================================
#
# file     : gf_ili9341_monochrome.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the ili9431 LCD driver chip specific parts
# for use by gf_lcd.
#
# ===========================================================================

from micropython import const

from godafoss.gf_time import *
from godafoss.gf_lcd import *


# ===========================================================================

_RDDSDR = const(0x0f) # Read Display Self-Diagnostic Result
_SLPOUT = const(0x11) # Sleep Out
_GAMSET = const(0x26) # Gamma Set
_DISPOFF = const(0x28) # Display Off
_DISPON = const(0x29) # Display On
_CASET = const(0x2a) # Column Address Set
_PASET = const(0x2b) # Page Address Set
_RAMWR = const(0x2c) # Memory Write
_RAMRD = const(0x2e) # Memory Read
_MADCTL = const(0x36) # Memory Access Control
_VSCRSADD = const(0x37) # Vertical Scrolling Start Address
_PIXSET = const(0x3a) # Pixel Format Set
_PWCTRLA = const(0xcb) # Power Control A
_PWCRTLB = const(0xcf) # Power Control B
_DTCTRLA = const(0xe8) # Driver Timing Control A
_DTCTRLB = const(0xea) # Driver Timing Control B
_PWRONCTRL = const(0xed) # Power on Sequence Control
_PRCTRL = const(0xf7) # Pump Ratio Control
_PWCTRL1 = const(0xc0) # Power Control 1
_PWCTRL2 = const(0xc1) # Power Control 2
_VMCTRL1 = const(0xc5) # VCOM Control 1
_VMCTRL2 = const(0xc7) # VCOM Control 2
_FRMCTR1 = const(0xb1) # Frame Rate Control 1
_DISCTRL = const(0xb6) # Display Function Control
_ENA3G = const(0xf2) # Enable 3G
_PGAMCTRL = const(0xe0) # Positive Gamma Control
_NGAMCTRL = const(0xe1) # Negative Gamma Control

_CHUNK = const(1024) #maximum number of pixels per spi write

class lcd_driver_ili9341:
    
    class cmd: # klopt van geen kanten
        NOP        = const( 0x00 )
        SWRESET    = const( 0x01 )
        RDDID      = const( 0x04 )
        RDDST      = const( 0x09 )
        
        RDDPM      = const( 0x0A )
        RDDMADCTL  = const( 0x0B )
        RDDIM      = const( 0x0D )
        RDDSEM     = const( 0x0E )
        RDDSDR     = const( 0x0F )
        SLPIN      = const( 0x10 )
        SLPOUT     = const( 0x11 )
        PTLON      = const( 0x12 )
        NORON      = const( 0x13 )
        INVOFF     = const( 0x20 )
        INVON      = const( 0x21 )
        GAMSET     = const( 0x26 )
        DISPOFF    = const( 0x28 )
        DISPON     = const( 0x29 )
        CASET      = const( 0x2A )
        RASET      = const( 0x2B )
        RAMWR      = const( 0x2C )
        RAMRD      = const( 0x2E )
        PTLAR      = const( 0x30 )
        VSCRDEF    = const( 0x33 )
        TEOFF      = const( 0x34 )
        TEON       = const( 0x35 )
        MADCTL     = const( 0x36 )
        COLMOD     = const( 0x3A )

    def __init__( 
        self, 
        master: lcd
    ):
        
        self._master = master

        for command, data in (
            (_RDDSDR, b"\x03\x80\x02"),
            (_PWCRTLB, b"\x00\xc1\x30"),
            (_PWRONCTRL, b"\x64\x03\x12\x81"),
            (_DTCTRLA, b"\x85\x00\x78"),
            (_PWCTRLA, b"\x39\x2c\x00\x34\x02"),
            (_PRCTRL, b"\x20"),
            (_DTCTRLB, b"\x00\x00"),
            (_PWCTRL1, b"\x23"),
            (_PWCTRL2, b"\x10"),
            (_VMCTRL1, b"\x3e\x28"),
            (_VMCTRL2, b"\x86")):
            self._write(command, data)
            
        self._write(_MADCTL, b"\x08")      

        for command, data in (
            (_PIXSET, b"\x55"),
            (_FRMCTR1, b"\x00\x18"),
            (_DISCTRL, b"\x08\x82\x27"),
            (_ENA3G, b"\x00"),
            (_GAMSET, b"\x01"),
            (_PGAMCTRL, b"\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00"),
            (_NGAMCTRL, b"\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f")):
            self._write(command, data)
            
        self._write(_SLPOUT)
        sleep_us( 120_000 )
        self._write(_DISPON)      
                  
    # =======================================================================
    
    def _write( self, a, b = None ):
        self._master.write_command( a, b )           
        
    # =======================================================================

# ===========================================================================

    

 