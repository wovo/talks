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
# This file contains various canvas demos
#
# ===========================================================================

from random import randint

from godafoss.gf_time import *
from godafoss.gf_tools import *
from godafoss.gf_xy import *
from godafoss.gf_canvas import *
from godafoss.gf_canvas_demo_colors import *
from godafoss.gf_canvas_demo_color_gradients import *
from godafoss.gf_canvas_demo_lines import *
from godafoss.gf_canvas_demo_rectangles import *
from godafoss.gf_canvas_demo_circles import *
from godafoss.gf_canvas_demo_text import *


# ===========================================================================

def canvas_demo( 
    s: canvas,
    iterations = None
):
    print( "canvas demos", s.size )
    pixels = s.size.x * s.size.y

    for _ in repeater( iterations ):
        if s.is_color:
            canvas_demo_colors( s, iterations = 1 )
            if pixels > 256:
                canvas_demo_color_gradients( s, iterations = 1 )
        if pixels > 256:
            canvas_demo_lines( s, iterations = 1 )
            canvas_demo_rectangles( s, iterations = 1 )
            canvas_demo_circles( s, iterations = 1 )
            canvas_demo_text( s, iterations = 1 )
        if 0: canvas_demo_scrolling_text(
            s,
            "Hello fantastic brave new world!\nusing Godafoss",
            iterations = 1
        )
         
# ===========================================================================
