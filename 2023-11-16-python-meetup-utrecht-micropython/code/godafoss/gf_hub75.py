# ===========================================================================
#
# file     : gf_hub75.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the RP2040 HUB75 LED panel driver
#
# ===========================================================================

import micropython
import framebuf
import machine
import uctypes

import rp2

from godafoss.gf_time import *
from godafoss.gf_report import *
from godafoss.gf_xy import *
from godafoss.gf_color import *
from godafoss.gf_canvas import *

# ===========================================================================

class hub75( canvas ):
    """
    RP2040 HUB75 display driver

    HUB75 is an interface and protocol for driving RGB LED panels.
    This driver uses RP2040 specific hardware (DMA and PIO),
    so it cabn be used only with that chip.
    
    :param size: xy
        size of the display in x and y direction
        
    :param r1_b2: int
        pin number of the r1 pin of the interface
        
        The pins for r1, g1, b1, r2, g2, b2 are consecutive.
    
    :param a_e: int
        pin numbber of the a pin of the interface
        
        The pins for a, b, c, d, e are cosecutive.
    
    :param clk_lat_int: int
        pin number of the clk pin of the interface
        
        The clk, lat, int pins are consecutive.
    
    :param frequency: int
        interface frequency (default: 10_000_000)
        
        The clock frequency (clk pin) used in the interface.
        The maximum seems to be 20 MHz.
    
    :param background: color
        background color (default: colors.black)
        
        The (default) background color of the display.

    A HUB75 panel has a two groups of three shift registers.
    Each group of three shift registers drives one row of RGB LEDs, 
    one shift register per colour per LED color..
    One group of shift registers drives LED rows in the 
    upper half of the panel, the other group drives the lower half.
    Within each half of the panel, up to five selector input pins 
    (A..E) determine which of the up to 32 LED rows is enabled.
    The shift registers each have a separate data input 
    (R1, G1, B1, R2, G2, B2),
    and common clock (CLK), latch (LAT) and output-enable (OE) inputs.
    
    A panel that uses all five selector pins is referred to 
    as 1:32 multiplexed, because at
    each moment only one of the 32 row pairs (one in the upper part, 
    one in the lower part) is enabled.
    The more common 1:16 multiplexed panels use four 
    selector inputs (E is connected to ground).
    
    A typical N x 16 panel omits the lower half of the panel,
    so the R2, G2, and B2 pins are not used.
    Such panels are still 1:16 multiplexed.
    
    To maintain a steady image, the row pairs must be driven at a
    high enough rate to avoid flicker.
    This requires the controller to output data at a rate that is
    challenging for microcontrollers.
    For larger displays, panels are put in series, 
    so the combined shift registers are concatenated.
    This drives the required data rate up even more, 
    to a point where dedicated hardware or FPGAs must be used.
    
    This driver uses the DMA (Direct Memory Access) and
    PIO (Programmable Input Output) peripherals of the RP2040
    chip to driver a HUB75 display at a high enough data rate.
    (In fact, at the highest rate it can handle.)
    
    The HUB75 interface uses 5V signal levels, but driving it
    with 3.3V RP2040 pins seems to be fine.
    
    A typical monochrome panel uses a HUB12 connector,
    which is not compatible with HUB75.
    
    A HUB75 panel (even a single one) can draw a lot of current:
    even a small 16x16 panel with all LEDs on theoretically draws 16A.
    Those displays have separate power connectors, and should
    be used with a suitable power supply.
    
    A quirck of this driver is that it often doesn't work
    when it is running, stopped, and - without a reset or Thonny STOP -
    is started again.
    It does however work each tine it is started after a reset
    or Thonny STOP. 

    I haven't found an official description of the HUB75 interface
    and protocol.
    This [sparkfun article](https://www.sparkfun.com/news/2650)
    gives a good overview.
    This page describes the
    [binary code modulation](http://www.batsocks.co.uk/readme/art_bcm_1.htm)
    used by the driver to dim the LEDs.
    """

    # =======================================================================
    
    def __init__(
        self,
        size: xy,
        r1_b2: int,
        a_e: int,
        clk_lat_oe: int,
        frequency: int = 10_000_000,
        background: color = colors.black
    ):
        canvas.__init__(
            self,
            size = size,
            is_color = True,
            background = background
        )
            
        self._frequency = frequency       
        self._r1_n = r1_b2
        self._a_n = a_e
        self._clk_n = clk_lat_oe
        
        self._framebuffer_buffer = bytearray( 
            2 * self.size.y * self.size.x )
        self._framebuffer = framebuf.FrameBuffer(
            self._framebuffer_buffer, 
            self.size.x, 
            self.size.y, 
            framebuf.RGB565 
        )

        # any ongoing DMA must be killed before the pio sm is installed
        machine.mem32[ 0x50000000 + 0x444 ] = 0x03
        while machine.mem32[ 0x50000000 + 0x444 ] != 0:
            pass
        
        # the fixed values in the pio buffer must be
        # allocated and initialized before the pio sm is started
        # flush_prepare takes care of this
        self._flush_prepare()

        # the state machine that outputs the word stream to the HUB75 display
        @rp2.asm_pio(
            autopull = True,
            sideset_init = ( [ rp2.PIO.OUT_HIGH ] * 3 ),    
            out_init = ( [ rp2.PIO.OUT_LOW ] * 6 ),
            set_init = ( [ rp2.PIO.OUT_HIGH ] * 4 ),    
            out_shiftdir = rp2.PIO.SHIFT_RIGHT
        ) 
        def spi_cpha0():
            # I don't understadn why the two pull()
            # instructions are needed
            
            # pull count from the data stream and put it on the a-e pins
            pull()
            mov( x, osr )
            
            # shift out count 6-bit values to the color pins
            label( "bitloop" )
            out( pins, 8 ).side( 0 + 0 + 0 )
            jmp( x_dec, "bitloop" ).side( 0 + 0 + 1 )
            
            # display off, latch new data
            nop().side( 4 + 2 + 0 ) # oe = 1, lat = 0
            
            # exec the instruction that 
            # outputs the row multiplex value to the a-e pins
            pull()
            out( exec, 32 )
                 
            # the first out in the bit loop will disable
            # the latch and enable the display
            # display will be on for the duration of the shifting

        # install and start the state machine
        sm_id = 0         
        self._sm = rp2.StateMachine(
            sm_id,
            spi_cpha0,
            2 * self._frequency,
            set_base=machine.Pin( self._a_n ),
            out_base=machine.Pin( self._r1_n ),
            sideset_base=machine.Pin( self._clk_n ),
        )
        self._sm.active(1)
        
        def dma_poke(
            channel: int,
            offset: int,
            value: int
        ):
            machine.mem32[ 0x50000000 + channel * 0x40 + offset ] = value
           
        # 1st DMA channel that transfers the _pio_buffer
        # to the pio state machine
        dma_poke( 1, 0x00, uctypes.addressof( self._pio_buffer ) )
        dma_poke( 1, 0x04, 0x50200010 )
        dma_poke( 1, 0x08, len( self._pio_buffer ) // 4 )
        dma_poke( 1, 0x10,
            ( 0x0 << 15 ) | ( 0 << 11 ) | ( 1 << 4 ) | ( 2 << 2 ) | 1  )
        
        # variable that holds the start address of the _pio_buffer
        self._pio_buffer_start_var = bytearray( 4 )
        machine.mem32[
            uctypes.addressof( self._pio_buffer_start_var )
        ] = uctypes.addressof( self._pio_buffer )

        # 2nd DMA that transfers the start of the _pio_buffer to the
        # start-and-trigger address of the 1st DMA channel
        dma_poke( 0, 0x00, uctypes.addressof( self._pio_buffer_start_var ) )
        dma_poke( 0, 0x04, 0x50000000 + 1 * 0x40 + 0x3C )
        dma_poke( 0, 0x08, 1 )
        dma_poke( 0, 0x0C,
            ( 0x3F << 15 ) | ( 0 << 11 ) | ( 0 << 4 ) | ( 2 << 2 ) | 1 )
        
    # =======================================================================    

    def _encode( self, ink ):
        a, b, c = ink.rgb()
        return (( a >> 4 ) << 8 ) | (( b >> 4 ) << 4 ) | ( c >> 4 )        
    
    # =======================================================================

    def _clear_implementation( 
        self,
        ink: color
    ):
        self._framebuffer.fill( self._encode( ink ) )
        
    # =======================================================================
        
    def _write_pixel_implementation( 
        self, 
        location: ( int, xy ), 
        ink: color
    ):
        self._framebuffer.pixel(
            location.x,
            location.y,
            self._encode( ink )
        )
        
    # =======================================================================    

    def _flush_prepare( self ) -> None:

        self._pio_buffer = \
            bytearray(  ( self.size.y // 2 ) * ( self.size.x + 8 ) )
        self.clear()
        
        buffer_pointer = uctypes.addressof( self._pio_buffer )
        for y in range( self.size.y // 2 ):
            
            machine.mem32[ buffer_pointer ] = self.size.x
            buffer_pointer += 4
            
            for x in range( self.size.x ):
                machine.mem8[ buffer_pointer ] = 0
                buffer_pointer += 1
                
            machine.mem32[ buffer_pointer ] = \
                rp2.asm_pio_encode( "set(pins,%d)" % y, 0 )
            buffer_pointer += 4

    # =======================================================================
    
    @micropython.native
    def _flush_direct_decode_viper( self ) -> None:
        pixel = self._framebuffer.pixel
        mem8 = machine.mem8
        size_x = self.size.x
        size_y = self.size.y
        
        @micropython.viper
        def encode( a: uint, b: uint ) -> uint:
            d = uint( 0 )
            if ( a & uint( 0x0F00 ) ): d += uint( 1 )
            if ( a & uint( 0x00F0 ) ): d += uint( 2 )
            if ( a & uint( 0x000F ) ): d += uint( 4 )
                
            if ( b & uint( 0x0F00 ) ): d += uint( 8 )
            if ( b & uint( 0x00F0 ) ): d += uint( 16 )
            if ( b & uint( 0x000F ) ): d += uint( 32 )
            return d
        
        buffer_pointer = uctypes.addressof( self._pio_buffer )
        for y in range( size_y // 2 ):

            # value never changes
            buffer_pointer += 4
            
            for x in range( self.size.x ):                   
                a = pixel( x, y )    
                b = pixel( x, y + size_y // 2 )
                
                mem8[ buffer_pointer ] = encode( a, b )
                buffer_pointer += 1
                
            # value never changes    
            buffer_pointer += 4    

    # =======================================================================    

    @report
    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self._flush_direct_decode_viper()

    # =======================================================================    

# ===========================================================================