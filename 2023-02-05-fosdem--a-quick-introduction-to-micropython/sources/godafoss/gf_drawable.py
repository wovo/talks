# ===========================================================================
#
# file     : gf_drawable.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the (abstract) drawable class.
#
# ===========================================================================

from godafoss.gf_tools import *
from godafoss.gf_xy import *
from godafoss.gf_canvas import *


# ===========================================================================

class drawable:
    """
    something that can be drawn on a canvas
    
    A drawable is an object that can be drawn on a canvas.
    Examples are a 
    
    To be drawn, the user must somehow specify the canvas on which to draw,
    and optionally the location where to draw (as offset from the orgigin), 
    and the color in which to draw. 
    These details can be specified when the drawable object is created, 
    applied via a modifier, be specified in the draw call, or be implicit.
    
    The canvas must be specified somehow.
    It can be specified with the object creation.
    A canvas specified in the draw call overrides a canvas of the
    object.    
    A canvas specified in a modifier overrides the canvas of the 
    (possibly already modified) object.
    
    Like the canvas, the ink color can be specified with the object 
    creation, be overruled by modifiers, 
    and finally be overruled by the draw() call.
    When no ink is specified, the complement (opposite) of the
    canvas background is used (color - operator).

    The offset defaults to no offset, which draws the drawable at the
    canvas origin xy( 0, 0 ), which is te top-left pixel.
    When offsets are specified (when the object is created, via
    modifiers, or with the draw() call) these offsets are all added to
    get the final offset.
    
    The draw call can be either the draw method of the drawable object
    (passing the canvas as parameter), or the draw method of the canvas 
    (passing the object as parameter).
    
    Drawables can be grouped together by adding them together.
    The result is a drawable that draws all its constituent drawables.
    """
    
    def __init__( self, ink = None ):
        self._ink = ink
        self._bundle = [ self ]
        
    def draw_implementation( self, canvas, offset, ink ):
        raise NotImplementedError    
               
    def draw( 
        self, 
        canvas: canvas, 
        offset: xy, 
        ink: color = None 
    ):
        """
        draw the drawable
        
        This function draws the drawable, using the canvas, offset and ink.
        """
        for component in self._bundle:
            component.draw_implementation( 
                canvas,
                offset,
                first_not_none( ink, - canvas.background )
            )   
        
    def __add__( self, other ):
        result = drawable()
        result._bundle = self._bundle + other._bundle
        return result
        
    def __rmatmul__( self, mod ):
    
        if isinstance( mod, xy ):    
            return modified_drawable( self, 
                lambda subject, canvas, offset, ink:
                    subject.draw( canvas, offset + mod, ink )
            )
            
        if isinstance( mod, color ):    
            return modified_drawable( self, 
                lambda subject, canvas, offset, ink:
                    subject.draw( canvas, offset, mod )
            )
            
        if isinstance( mod, drawable_modifier ):    
            return modified_drawable( self, 
                lambda subject, canvas, offset, ink:
                    mod.draw( canvas, offset, color )
            )
            
        return NotImplemented    
            
      
# ===========================================================================

class modified_drawable( drawable ):
    """
    a modified drawable
    
    An modified_drawable holds a subject drawable, 
    and a function that implements the way this
    subject is to be drawn when the modified_drawable is drawn.
    """

    def __init__( self, subject, draw ):
        self._subject = subject
        self._draw = draw
        drawable__init__( self )
        
    def draw_implementation( self, canvas, offset, ink ):
        self._draw( self._subject, canvas, offset, ink )  


# ===========================================================================

class drawable_modifier:
    """
    modifies a drawable
    
    A drawable_modifier can be applied to a drawable to
    yield a drawable that is drawn differently.
    
    Besides the explicit drawable modifiers
    a color value can be used as a drawable modifier
    to change ink in which the drawable is drawn. 
    An xy value can be used as a drawable modifier to add an offset 
    to the location where the drawable is drawn.
    
    Drawable modifiers can be applied to each other using the @ operator
    to yield a combined modifier.
    
    """
    
    def __init__( self, draw ):
        self._draw = draw
        
    def __matmul__( self, subject ):
        if isinstance( subject, drawable_modifier ):    
            return 
            

"""
replicate( 
    red @ x( 0, 0 ),
    blue @ x( 10, 0 ),
    xy( 20, 0 ) @ green
) @ circle( ... )   
"""
