# ===========================================================================
#
# file     : gf_touch.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the ft6236 touch screen interface driver class.
#
# ===========================================================================

from micropython import const 

from godafoss.gf_time import *
from godafoss.gf_xy import *
from godafoss.gf_pins import *
from godafoss.gf_make_pins import *


# ===========================================================================

class touch:
    """
    lcd touch sensor interface
    """
        
    # =======================================================================    

    def __init__(
        self,
        span: int,
        size: xy
    ):
        self._span = span
        self._size = size
        
    # =======================================================================        

    def touch_adcs( self ):
        """
        read and return the raw x and y touch ADC values.
        
        :result: int, int
            tuple of the 12-bit x and y ADC values of the touch point
            None, None when no touch
        """

        raise NotImplementedError  
            
    # =======================================================================        

    def touch_fractions( self ):
        """
        read and return the x and y touch values as fractions
        
        :result: :class:`~godafoss.fraction`, :class:`~godafoss.fraction`
            tuple of the 12-bit x and y ADC values, or None
            
        This function reads the two ADC touch channels.
        When no touch is detected, None is rerurned
        When a touch is detected, a list of the x and y touch
        locations is returned as a :class:`~godafoss.fraction` pair.
        """
        a, b = self.touch_adcs()
        
        if a == None:
            return None
            
        return fraction( a, self._span ), fraction( b, self._span )
            
    # =======================================================================        

    def touch_xy( 
        self, 
        size: xy 
    ):
        """
        read and return the touch location as xy pixel cooordinates
        
        :result: None, :class:`~godafoss.xy`
            the touch location, or None if no touch
        """
        t = self.touch_fractions()
        if t == None:
            return None
        x, y == t    
            
        return xy( 
            x.scaled( 0, size.x -1 ), 
            y.scaled( 0, size.y -1 )
        )
            
    # =======================================================================              

    def demo( self ):
        """
        demo: print touch adc values
        """
        
        print( "touch demo" )
        while True:
            a, b = self.touch_adcs()        
            if a is not None:
                print( "(%d,%d)" % ( a, b ) )
                sleep_us( 200_000 )
    
# ===========================================================================
