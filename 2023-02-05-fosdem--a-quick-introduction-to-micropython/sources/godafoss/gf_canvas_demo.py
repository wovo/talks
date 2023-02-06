# ===========================================================================
#
# file     : gf_canvas_demo.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the canvas_demo function.
#
# ===========================================================================

import time

from godafoss.gf_tools import *
from godafoss.gf_xy import *
from godafoss.gf_color import *
from godafoss.gf_canvas import *
from godafoss.gf_drawable import *
from godafoss.gf_line import *
from godafoss.gf_rectangle import *
from godafoss.gf_circle import *
from godafoss.gf_text import *


def canvas_demo( c: canvas ):
        from random import randint
        print( "canvas demo", c.size )
        while True:

            c.clear()
            c.draw( xy( 0, 0 ), rectangle( c.size ) )
            c.flush()
            time.sleep_ms( 500 )
            c.draw( xy( 1, 1 ), text( "Hello world" ) )
            c.flush()
            time.sleep_ms( 500 )            
            c.draw( xy( 1, 9 ), text( "Micropython" ) )
            c.flush()
            time.sleep_ms( 500 )            
            c.draw( xy( 1, 17 ), text(  "+ Godafoss" ) )
            c.flush()
            time.sleep_ms( 2_000 )

            c.clear()
            c.draw( xy( 0, 0 ), rectangle( c.size ) )
            c.flush()
            for dummy in range( 0, 20 ):
                start = xy(
                    randint( 0, c.size.x - 1 ),
                    randint( 0, c.size.y - 1 ) )
                end = xy(
                    randint( 0, c.size.x - 1 ),
                    randint( 0, c.size.y - 1 ) )
                c.draw( start, line( end - start ) )
                c.flush()
            time.sleep_ms( 2_000 )

            c.clear()
            c.draw( xy( 0, 0 ), rectangle( c.size ) )
            c.flush()
            for dummy in range( 0, 10 ):
                start = xy(
                    randint( 0, c.size.x - 1 ),
                    randint( 0, c.size.y - 1 )
                )
                end = xy(
                    randint( 0, c.size.x - 1 ),
                    randint( 0, c.size.y - 1 )
                )
                c.draw( start, rectangle( end - start ))
                c.flush()
            time.sleep_ms( 2_000 )

            c.clear()
            c.draw( xy( 0, 0 ), rectangle( c.size ) )
            c.flush()
            for dummy in range( 0, 20 ):
                start = xy(
                    randint( 0, c.size.x - 1 ),
                    randint( 0, c.size.y - 1 )
                )
                radius = randint( 0, min( c.size.x, c.size.y ) // 2 )
                end = xy(
                    randint( 0, c.size.x - 1 ),
                    randint( 0, c.size.y - 1 )
                )
                c.draw( start, circle( radius ) )
                c.flush()
            time.sleep_ms( 2_000 )


