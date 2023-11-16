# ===========================================================================
#
# file     : gf_shape.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the (abstract) shape class.
#
# ===========================================================================

from godafoss.gf_xy import *


# ===========================================================================

class shape:
    """
    something that can be drawn on a canvas
    
    A shape is something that can be drawn on a :class:`~godafoss.canvas`.
    Examples are a 
    :class:`~godafoss.line`, 
    :class:`~godafoss.rectangle`, 
    :class:`~godafoss.circle`, and 
    :class:`~godafoss.glyph` (character).
    
    Shapes can be grouped together by adding them together
    (+ operator).
    The result is a :class:`~godafoss.shape` that, when written, 
    writes all its constituent shapes.
    
    A shape can be pre-multiplied by an xy value, which adds
    an offset to where the shape is written.
    
    $macro_start shape
    This class implements the :class:`~shape` interface:
    it can be written to a :class:`~godafoss.sheet`, added to another 
    :class:`~godafoss.shape`
    to form a compound shape, or post-mathmultiplied
    (@ operator) with an :class:`~godafoss.xy` value to include an offset.
    $macro_end
    """

    # =======================================================================

    def __init__( 
        self
    ):     
        pass
        
    # =======================================================================

    def write( 
        self, 
        sheet: "sheet", 
        offset: xy = xy( 0, 0 ),
        ink: bool | color = True
    ) -> None:
        """
        write the shape to a sheet
        
        :param sheet: (:class:`~godafoss.sheet`)
            the :class:`~godafoss.sheet` on which the shape must be written
                  
        :param offset: (:class:`~godafoss.xy`, default (0,0) )
            the offset at which the shape must be written      

        Writing a :class:`~godafoss.shape` is additive 
        in the sense that pixels that are True
        are written in the sheets foreground 'color', while pixels that
        are False are not written.

        $macro_start shape_write      
        :param sheet: (:class:`~godafoss.sheet`)
            the :class:`~godafoss.sheet` on which the shape must be written
                  
        :param offset: (:class:`~godafoss.xy`, default (0,0) )
            the offset at which the shape must be written 
            
        Writing a :class:`~godafoss.shape` is additive in the sense 
        that pixels that are True are written in the sheets 
        foreground 'color', while pixels that are False are not written.            
        $macro_end
        """
        
        raise NotImplementedError        

    # =======================================================================

    def __add__( 
        self, 
        other: "shape"
    ) -> "shape":
        return _shape_add( self, other )
        
    # =======================================================================

    def __rmul__( 
        self, 
        modifier: xy
    ) -> "shape":
    
        if isinstance( modifier, xy ):
            return _shape_offset( self, modifier )
            
        # color -> image
        # sequence of modifiers -> apply all (mustb be a type??)
            
        return NotImplemented   
        
        
    # =======================================================================

    def __matmul__( 
        self, 
        modifier: xy
    ) -> "shape":
    
        if isinstance( modifier, xy ):
            return _shape_offset( self, modifier )
            
        # color -> image
        # sequence of modifiers -> apply all (mustb be a type??)
            
        return NotImplemented   
        
        
# ===========================================================================

class _shape_offset( shape ):

    def __init__( self, subject, offset ):
        self._subject = subject
        self._offset = offset
        shape.__init__( self )
        
    def write( 
        self, 
        sheet: "sheet", 
        offset: xy = xy( 0, 0 ),
        ink: bool | color = True
    ) -> None:
        self._subject.write( sheet, self._offset + offset, ink ) 
        
        
# ===========================================================================

class _shape_add( shape ):

    def __init__( self, a, b ):
        self._a = a
        self._b = b
        shape.__init__( self )
        
    def write( 
        self, 
        sheet: "sheet", 
        offset: xy = xy( 0, 0 ),
        ink: bool | color = True
    ) -> None:
        self._a.write( sheet, offset, ink ) 
        self._b.write( sheet, offset, ink ) 
        
        
# ===========================================================================
        