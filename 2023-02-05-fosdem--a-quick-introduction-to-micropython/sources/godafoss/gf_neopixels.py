# ===========================================================================
#
# file     : gf_neopixels.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the neopixels classes.
#
# ===========================================================================

from godafoss.gf_time import *
from godafoss.gf_color import *
from godafoss.gf_canvas import *


# ===========================================================================

class neopixels( canvas ):
    """
    neopixels common driver
    
    $macro_start neopixels
    :param n: (int)
        the number of pixels in the chain
    
    :param background: (:class:`~godafoss.color`)
        the background color (default: black)
        
    :param order: (str)
        the color order (default: RGB)    
        
    $macro_end    
    $macro_insert neopixels
    
    Neopixels are seperately controllable RGB LEDs,
    either as separate chip and LED, or as chip combined with an RGB LED.
    Neopixels can be connected into a chain, where only the first
    pixel is connected to a microcontroller.
    Power and data (and for some types a clock) are fed
    from each neopixel to the next.
    Such chains are often used in strips, and sometimes as rectanges
    (where the chain is folded).
    
    The common chip are summarized in the table below.
    The apa102 and ws2801 chips have dedicated driver classes.
    The hd107 seems to use the same protocol as the apa102, so
    it should work with that driver.
    The ws2811, ws2812, ws2813 and ws2815 chips 
    can use the ws281x driver class.
    
    +----------+-------+--------------+--------+------------------+
    | chip     | form  | interface    | power  | protocol         |
    +----------+-------+--------------+--------+------------------+
    | apa102   | chip  | data, clock  | 5V     | start, data, end |
    +----------+-------+--------------+--------+------------------+
    | hd107    | led   | data, clock  | 5V     | start, data, end |
    +----------+-------+--------------+--------+------------------+
    | ws2801   | chip  | data, clock  | 5V     | data only        |
    +----------+-------+--------------+--------+------------------+
    | ws2811   | chip  | data         | 5V     | data only        |
    +----------+-------+--------------+--------+------------------+
    | ws2812   | led   | data         | 5V     | data only        |
    +----------+-------+--------------+--------+------------------+
    | ws2813   | led   | data         | 5V     | data only        |
    +----------+-------+--------------+--------+------------------+
    | ws2815   | led   | data         | 12V    | data only        |
    +----------+-------+--------------+--------+------------------+
    
    Be aware that a chain of neopixels can draw a significant amount of
    current: at for brightness 60mA per pixel.
    Hence for non-trivial amounts of neopixels a separate power supply 
    is required, and power + ground 'bypass' wiring might be needed.
    """

    # =======================================================================

    def __init__( 
        self,  
        n: int, 
        background, 
        order: str = "RGB"
    ):
        canvas.__init__(
            self,
            size = xy( n, 1 ),
            is_color = True,
            background = colors.black
        )
        
        order = order.upper()
        if order == "RGB":
            self._permutate = lambda ink: ( ink.red, ink.green, ink.blue )
        elif order == "RBG":
            self._permutate = lambda ink: ( ink.red, ink.blue, ink.green )
        elif order == "BGR":
            self._permutate = lambda ink: ( ink.blue, ink.green, ink.red )
        elif order == "BRG":
            self._permutate = lambda ink: ( ink.blue, ink.red, ink.green )
        elif order == "GRB":
            self._permutate = lambda ink: ( ink.green, ink.red, ink.blue )
        elif order == "GBR":
            self._permutate = lambda ink: ( ink.green, ink.blue, ink.red )
        else:
            raise ValueError( "color order '%s'", order )
        

    # =======================================================================
    
    def _write_pixel_implementation( 
        self, 
        location: ( int, xy ), 
        ink: color
    ):      
        self._pixels[ location.x ] = self._permutate( ink )

    # =======================================================================
    
    def demo_color_wheel(
        self,
        color_list = (
            colors.red,
            colors.green,
            colors.blue,
            colors.white
        ),
        delay: int = 10_000,
        iterations = None,
        dim: int = 30
    ):
        for _ in repeater( iterations ):
            for c in ( color_list ):
                self.clear()
                for n in range( self.size.x + 1 ):
                    self.flush()
                    sleep_us( delay )
                    self.write_pixel(
                        xy( n, 0 ),
                        c // dim
                    )  
                for n in range( self.size.x + 1 ):
                    self.flush()
                    sleep_us( delay )
                    self.write_pixel(
                        xy( n, 0 ),
                        colors.black
                    ) 
    
# ===========================================================================

   
class ws281x( neopixels ):
    """
    requires neopixel support in the target, Teensy 4.1 by default doesn't
    """

    def __init__( 
        self, 
        pin: int, 
        n: int, 
        background = colors.black, 
        order: str = "RGB"
    ):
        import neopixel, machine
        self._pixels = neopixel.NeoPixel(
            machine.Pin( pin, machine.Pin.OUT ), n )
        
        neopixels.__init__( self, n, background, order )

    # =======================================================================

    def _flush_implementation( self ):
        self._pixels.write()    

    # =======================================================================
    
# ===========================================================================
