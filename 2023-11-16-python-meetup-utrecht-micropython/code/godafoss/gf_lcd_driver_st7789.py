# ===========================================================================
#
# file     : gf_lcd_driver_st7789.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the st7789 LCD driver chip specific parts
# for use by gf_lcd.
#
# ===========================================================================

from micropython import const

from godafoss.gf_time import *
from godafoss.gf_lcd import *


# ===========================================================================

class lcd_driver_st7789:
    
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

        #master.write_command( self.cmd.SWRESET )
        master.write_command( self.cmd.SLPOUT )
        sleep_us(120_000)        
           
        master.write_command( self.cmd.COLMOD, [ 0x05 ] ) # was 66
        sleep_us(120_000)  
      
        master.write_command( self.cmd.MADCTL, [ 0x10 ] );  # was 10                    
        master.write_command( self.cmd.CASET, [
            0, 0, master.size.x >> 8, master.size.x & 0xFF ])
        master.write_command( self.cmd.RASET, [
            0, 0, master.size.y >> 8, master.size.y & 0xFF ])
      
        master.write_command( self.cmd.INVON )
        #time.sleep_ms( 10 )
        master.write_command( self.cmd.NORON )
        #time.sleep_ms( 100 )
        master.write_command( self.cmd.DISPON )
        #time.sleep_ms( 100 )
        
        master.write_command(
            self.cmd.INVON if master._invert else self.cmd.INVOFF )  
        
        m = 0x00
        if master._swap_xy:
            m |= 0x20
        if master._mirror_x:
            m |= 0x40
        if master._mirror_y:
            m |= 0x80
        master.write_command( self.cmd.MADCTL, [ m ] )          

        master.write_command( self.cmd.NORON )
        #time.sleep_ms( 10 )

        master.write_command( self.cmd.DISPON )
        #time.sleep_ms( 100 )
                   
    # =======================================================================

# ===========================================================================