# ===========================================================================
#
# file     : gf_lcd_driver_st7735.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the st7735 LCD driver chip specific parts
# for use by gf_lcd.
#
# ===========================================================================

from micropython import const

from godafoss.gf_time import *
from godafoss.gf_lcd import *


# ===========================================================================

class lcd_driver_st7735:

    # =======================================================================

    class cmd:
        NOP     = const( 0x00 ) 
        SWRESET = const( 0x01 )
        RDDID   = const( 0x04 )
        RDDST   = const( 0x09 )
        
        SLPIN   = const( 0x10 )
        SLPOUT  = const( 0x11 )
        NORON   = const( 0x13 )        
        INVOFF  = const( 0x20 )
        INVON   = const( 0x21 )
        DISPOFF = const( 0x28 )
        DISPON  = const( 0x29 )
        
        CASET   = const( 0x2A )
        RASET   = const( 0x2B )
        RAMWR   = const( 0x2C )
        RAMRD   = const( 0x2E )
        PTLAR   = const( 0x30 )
        COLMOD  = const( 0x3A )
        MADCTL  = const( 0x36 )
        RDID1   = const( 0xDA )
        RDID2   = const( 0xDB )
        RDID3   = const( 0xDC ) 
        RDID4   = const( 0xDD ) 
        FRMCTR1 = const( 0xB1 ) 
        FRMCTR2 = const( 0xB2 )
        FRMCTR3 = const( 0xB3 )
        INVCTR  = const( 0xB4 )
        PWCTR1  = const( 0xC0 )
        PWCTR2  = const( 0xC1 )
        PWCTR3  = const( 0xC2 )
        PWCTR4  = const( 0xC3 )
        PWCTR5  = const( 0xC4 )
        VMCTR1  = const( 0xC5 )
        GMCTRP1 = const( 0xE0 )
        GMCTRN1 = const( 0xE1 )

    # =======================================================================

    def __init__( 
        self, 
        master: lcd
    ):        
        
        master.write_command( self.cmd.SLPOUT )
        sleep_us(120_000)
         
        master.write_command( self.cmd.INVCTR, [ 0x03 ] )

        # master.write_command( 0x62, [ 0x02, 0x04 ] )

        master.write_command( self.cmd.PWCTR1 )
        master.write_command( self.cmd.PWCTR2, [ 0xC0 ] )
        master.write_command( self.cmd.PWCTR3, [ 0x0D, 0x00 ] )
        master.write_command( self.cmd.PWCTR4, [ 0x8D, 0x6A ] )
        master.write_command( self.cmd.PWCTR5, [ 0x8D, 0xEE ] )

        master.write_command( self.cmd.VMCTR1, [ 0x0E ] )

        master.write_command( self.cmd.GMCTRP1,
            [ 0x10, 0x0E, 0x02, 0x03, 0x0E, 0x07, 0x02, 0x07,
              0x0A, 0x12, 0x27, 0x37, 0x00, 0x0D, 0x0E, 0x10 ] )
        master.write_command( self.cmd.GMCTRN1,
            [ 0x10, 0x0E, 0x03, 0x03, 0x0F, 0x06, 0x02, 0x08,
              0x0A, 0x13, 0x26, 0x36, 0x00, 0x0D, 0x0E, 0x10 ] )
        
        if 0: master.write_command( self.cmd.FRMCTR1,
            [ 0x05, 0x3A, 0x3A ] )
        if 0: master.write_command( self.cmd.FRMCTR2,
            [ 0x05, 0x3A, 0x3A ] )
        if 0: master.write_command( self.cmd.FRMCTR3,
            [ 0x05, 0x3A, 0x3A, 0x05, 0x3A, 0x3A ] )
        
        master.write_command(
            self.cmd.INVON if master._invert else self.cmd.INVOFF )      

        master.write_command( self.cmd.COLMOD, [ 0x55 ] ) # 16-bit RGB 565
        
        m = 0x00
        if master._swap_xy:
            m |= 0x20
        if master._mirror_x:
            m |= 0x40
        if master._mirror_y:
            m |= 0x80
        master.write_command( self.cmd.MADCTL, [ m ] )       
        
        master.write_command( self.cmd.DISPON )
        sleep_us(100 )
        
    # =======================================================================

# ===========================================================================
