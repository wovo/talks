# ===========================================================================
#
# file     : gf_digits_demos.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the digits class.
#
# ===========================================================================

from godafoss.gf_typing import *
from godafoss.gf_time import *
from godafoss.gf_xy import *
from godafoss.gf_digits import *


# ===========================================================================

def digits_demo(
    self,
    iterations = None
):
    """
    seven-segment digits display demo
    """
        
    print( "seven segments demo" )
        
    for _ in repeater( iterations ):

        for i in range( self.n ):
            for n in range( 10 ):
                for d in range( self.n ):
                    self.write(
                        ( " " * i ) + "%d" % n,
                        align = False
                    )
                    sleep_us( 10_000 )

        for i in range( 0, 10 ** self.n ):
            x = ( i // 100 ) % self.n
            self.write(
                "%d" % i,
                points = [ n == x for n in range( self.n ) ]
            )


# ===========================================================================
