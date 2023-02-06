# ===========================================================================
#
# file     : gf_canvas.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the canvas class.
#
# ===========================================================================

from godafoss.gf_tools import *
from godafoss.gf_xy import *
from godafoss.gf_invertible import *
from godafoss.gf_color import *
from godafoss.gf_shape import *


# ===========================================================================

class canvas( invertible ):
    """
    graphic drawing area, either monochrome or color 
    
    :param location: (:class:`~godafoss.xy`)
        the size of the canvas in pixels in x and y direction
    
    :param is_color: (bool)
        False for a monochrome canvas, True for a color canvas
    
    $insert_image( "canvas-coordinates", 1, 500 )    

    A canvas is a rectanglular area of either monochrome or color pixels.
    A canvas has a size attribute, which is the number of pixels in
    the x and y directions.
    The top-left pixel is at xy( 0, 0 ), the bottom-right pixel is
    at xy(canvas.size.x - i, canvas.size.y - 1).
    
    The is_color attribute is False for a monochrome
    canvas, or True for a color canvas.
    
    The write_pixel method writes a single pixel.
    
    The write method writes a :class:`~godafoss.shape`.
    
    Canvases can be added, which creates a canvas that writes
    to both constituent canvases.
    
    $macro_start canvas_monochrome
    This class implements the monochrome 
    :class:`~godafoss.canvas` interface, 
    which provides functionality to write shapes 
    (:class:`~godafoss.line`, :class:`~godafoss.circle`, 
    :class:`~godafoss.rectangle`, :class:`~godafoss.text`),
    to derive modified canvases 
    (inverted, mirrored, rotated, parts, combinations, etc.),
    and a comprehensive demo.
    $macro_end
    
    $macro_start canvas_color
    This class implements the color :class:`~godafoss.canvas` interface, 
    which provides functionality to write shapes 
    (:class:`~godafoss.line`, :class:`~godafoss.circle`, 
    :class:`~godafoss.rectangle`, :class:`~godafoss.text`),
    to derive modified canvases 
    (inverted, mirrored, rotated, parts, combinations, etc.),
    and a comprehensive demo.
    $macro_end
    """

    # =======================================================================

    def __init__(
        self,
        size: xy,
        is_color: bool,
        background: bool | color
    ):
        self.size = size
        self.is_color = is_color
        self.background = background
        self.foreground = - background if self.is_color else not background
        self._dirty = True
        invertible.__init__( self )

    # =======================================================================
    
    def within( 
        self, 
        location: xy 
    ):
        """
        check if the location is within the canvas
        
        :param location: (:class:`~godafoss.xy`)
            the location coordinates to be checked     
        
        This method returns True iff the location
        is within the canvas.
        """
        
        return (
            within( location.x, 0, self.size.x - 1 )
            and within( location.y, 0, self.size.y - 1 ) )    

    # =======================================================================
    
    def _cure_ink( 
        self, 
        ink: color | bool | None
    ) -> color | bool | None:
        """
        return specific ink
        
        This method returns a concrete ink:
        
        - None when no pixel write must be done
        - else, for a monochrome canvas: True
        - else (for a color canvas) a color
        """
        if ink is not None:
            if self.is_color:
                if isinstance( ink, bool ):
                    if ink:
                        ink = self.foreground
                    else:
                        ink = self.background
            else:
                if not isinstance( ink, bool ):
                   raise valueError( 
                       "monochrome canvas method called with color ink"   
                   )                   
        return ink                   
    
    
    # =======================================================================
    
    def write_pixel(
        self,
        location: xy,
        ink: color | bool | None = True
    ) -> None:
        """
        write a pixel
        
        :param location: (:class:`~godafoss.xy`)
            the location of the pixel that is to be written 
        
        :param ink: (:class:`~godafoss.color`, bool, None, defauklt: True)
            the value to be written to the pixel      

        This method writes a single pixel.
        When the location is within the canvas, 
        and the ink parameter is not None, 
        the ink is written to the pixel.
        
        If the ink argument is None, the pixel is not is written.
        
        For a monochrome canvas, the ink must (if not None)
        be a bool. When True, the foreground 'color'
        is written. When False, the pixel is not written.
        
        For a monochrome canvas, when the ink is a color,
        that color is written to the pixel.
        When the ink is a bool, the canvas foreground
        color is written. When False, the pixel is not written.
        
        A canvas is be buffered: the writing of pixels is
        be effectuated only when the flush() method is called.
        """
        
        if ( ink is not None ) and self.within( location ):
            ink = self._cure_ink( ink )
            self._dirty = True
            self._write_pixel_implementation( 
                location,
                ink
            )
    
    # =======================================================================

    def flush( 
        self, 
        forced: bool = False 
    ) -> None:
        """
        effectuate what was written to the canvas
        
        :param forced: (bool)
            True forces a flush, even when no pixels were written

        Writes to the canvas can be buffered.
        If so, a flush() method call is required to effectuate
        the write_pixel() calls.
        
        A flush() call might be a no-op when no pixels were changed since
        the previous flush() call, unless the forced parameter is True.
        
        $macro_start canvas_flush
        effectuate what was written
        
        :param forced: (bool)
            True forces a flush, even when no pixels were written        

        Writes to the display are buffered:
        a flush() method call is required to effectuate what was written.
        
        A flush() call is a no-op when no pixels were changed since
        the previous flush() call, unless the forced parameter is True.        
        $macro_end        
        """ 
        
        if self._dirty or forced:
            self._dirty = False
            self._flush_implementation()            

    # =======================================================================

    def write( 
        self, 
        thing: shape,
        location: xy = xy( 0, 0 )        
    ) -> None:
        """
        write a :class:`~godafoss.shape`
        
        The write() method calls the write() method of the 
        :class:`~godafoss.shape` to write itself to the canvas.
        """
        
        thing.write( self, location )
        
    # =======================================================================

    def clear( 
        self, 
        ink: bool | color = False 
    ) -> None:
        """
        clear the display
        
        :param ink: (bool)
            the 'color' to write to all pixels
        
        This method clears the display.
        The default implementation writes False to all individual pixels.
        A concrete canvas might implement a faster method.

        A display might be buffered: a clear() call might
        be effectuated only when the flush() method is called.
        
        $macro_start canvas_clear
        clear the display
        
        :param ink: (bool)
            the 'color' to write to all pixels
        
        This method clears the display.
        By default the background 'color' is written to all pixels.
        When ink is true, the inverse of the background is written.

        Writes are buffered: a flush call is required
        to write changed pixels to the screen.
        $macro_end        
        """      
        
        ink = self._cure_ink( ink )
        self._dirty = True
                
        for x in range( 0, self.size.x ):
            for y in range( 0, self.size.y ):
                self._write_pixel_implementation( xy( x, y ), ink )
            
    # =======================================================================
    
    def _write_pixel_implementation(
        self,
        location: xy,
        ink: color | bool
    ) -> None:  
        """
        write a pixel (concrete implementation)
        
        :param location: (:class:`~godafoss.xy`)
            the location of the pixel that is to be written 
        
        :param ink: (:class:`~godafoss.color`, bool )
            the value to be written to the pixel        
        
        This method must be implemented by a concrete class that
        inherits from canvas. When this method is called:
        - the location is within the canvas.
        - for a monochrome canvas, the ink is True.
        - for a color canvas, the ink is a color.
        """
        
        raise NotImplementedError    

    # =======================================================================
    
    def _flush_implementation( self ) -> None:  
        """
        flush the canvas content (concrete implementation)
        
        This method must be implemented by a concrete class that
        inherits from canvas.
        """

        raise NotImplementedError   
    
    # =======================================================================
    
    def _clear_implementation( 
        self, 
        ink: bool | color
    ) -> None:
        """
        clear the display (concrete implementation)
        
        :param ink: (bool)
            the 'color' to write to all pixels
            
        This method can be implemented by a concrete class that
        inherits from canvas. 
        The default implementation writes False to all individual pixels.
        A concrete canvas might implement a faster method.
        
        When this method is called:    
        - for a monochrome canvas, the ink is a bool.
        - for a color canvas, the ink is a color.             
        """      
                
        for x in range( 0, self.size.x ):
            for y in range( 0, self.size.y ):
                self._write_pixel_implementation( xy( x, y ), ink )    
    
    # =======================================================================
    
    def demo(
        self,
        iterations = None
    ):
        from godafoss.gf_canvas_demos import canvas_demo
        canvas_demo( self, iterations )
    
    # =======================================================================

    def demo_ggf_photos(
        self,
        location: str,        
        iterations = None
    ):
        from godafoss.gf_canvas_demos import canvas_demo_ggf_photos
        canvas_demo_ggf_photos( self, location, iterations )
    
    # =======================================================================
    
    def __add__( 
        self, 
        other: "canvas" 
    ) -> "canvas":
        return _canvas_add( self, other )  
        
    # =======================================================================

    def inverted( self ) -> "canvas":
        """
        inverse of the display

        This method returns a display that inverts the effect 
        of write_pixel() calls.
        """
        
        return _canvas_inverted( self )        
        
    # =======================================================================

    def folded( self, n: int, zigzag: bool = False ) -> "canvas":
        """
        folded version of the display

        This method returns a display corresponds to te original one,
        folded by n.
        """
        
        return _canvas_folded( self, n, zigzag )        
        
    # =======================================================================

    def part( 
        self, 
        start: xy, 
        size: xy 
    ) -> "canvas":
        """
        part of the canvas

        This method returns a new canvas that is 
        part of the original canvas, as specified by the
        start and size parameters.
        
        The clear() method of a canvas part can be significantly slower
        than the clear() of the original canvas, because it can't use
        the clear() of the driver (which often has a fast way to clear 
        the whole canvas).
        """
        
        return _canvas_part( self, start, size )         
        
    # =======================================================================
    
    def xy_swapped( self ):
        return _canvas_transformed( 
            self, 
            xy( self.size.y, self.size.x ),
            lambda c: xy( c.y, c.x )
        )
        

    # =======================================================================

    def rotated( 
        self, 
        rotation: int 
    ) -> "canvas":
        """
        rotated version of the canvas

        This method returns a canvas that is 
        a rotated version of the original canvas.
        Allowed rotation values are 0, 90, 180 and 270.
        """
        
        if rotation == 0:
            return _canvas_transformed( 
                self, 
                self.size, 
                lambda c: xy( c.x, c.y )
            )
            
        elif rotation == 90:
            return _canvas_transformed( 
                self, 
                xy( self.size.y, self.size.x ),
                lambda c: xy( self.size.x - 1 - c.y, c.x )
            )
            
        elif rotation == 180:
            return _canvas_transformed( 
                self, 
                self.size, 
                lambda c: xy( self.size.x - 1 - c.x, self.size.y - 1 - c.y )
            )
            
        elif rotation == 270:
            return _canvas_transformed( 
                self, 
                xy( self.size.y, self.size.x ), 
                lambda c: xy( c.y, self.size.y - 1 - c.x ) 
            )    
            
        else:
            raise ValueError( "rotation must be 0, 90, 180 or 270" )       
        
    # =======================================================================

    def extended( 
        self, 
        other: "canvas", 
        direction: str = "EN"
    ) -> "canvas":
        """
        extension of the canvas

        This method returns a canvass that extends the canvas.
        
        The direction determines where the other canvas is placed
        relative to the original canvas (north, east, south or west),
        and which side of the canvases is aligned 
        (again: north, east, south or west).
        Valid values for the direction are
        "ES", "EN", "WS", "WN", "NW", "NE", "SW", "SE".
        """
        
        if len( direction ) != 2:
            raise ValueError( "direction must be 2 characters" )
            
        direction, alignment = direction            
            
        # which canvas comes first    
        if direction in "SE":
            a, b = self, other
        elif direction in "NW":
            a, b = other, self
        else:
           raise ValueError( "direction[ 0 ] is invalid" ) 
           
        # size depends on extension direction: x or y
        # shift depends on both extension direction and alignment
        if direction in "EW":
            size = xy( 
                self.size.x + other.size.x,
                max( self.size.y, other.size.y ) )

            if alignment == "S":
                a_shift = xy( 0,        size.y - a.size.y )
                b_shift = xy( a.size.x, size.y - b.size.y )
                
            elif alignment == "N":
                a_shift = xy( 0,        0 )
                b_shift = xy( a.size.x, 0 )
                
            else:
                raise ValueError( "direction[ 1 ] is invalid" )
                
        elif direction in "NS":
            size = xy( 
                max( self.size.x, other.size.x ),
                self.size.y + other.size.y )

            if alignment == "E":
                a_shift = xy( b.size.x - a.size.x, 0 )
                #b_shift = xy( a.size.x, 0 )
                
            elif alignment == "W":
                a_shift = xy( 0, 0 )
                b_shift = xy( 0, a.size.y )
                
            else:
                raise ValueError( "direction[ 1 ] is invalid" )           
        
        return _canvas_extend( a, b, size, - a_shift, - b_shift )          

    # =======================================================================


# ===========================================================================  
#
# helper classes
# 
# ===========================================================================

class _canvas_add( canvas ):
    """
    helper class that adds two canvass
    """
    def __init__( 
        self, 
        a: canvas, 
        b: canvas 
    ):
        self._a = a
        self._b = b
        canvas.__init__(
            self,
            xy( 
                max( self._a.size.x, self._b.size.x ),
                max( self._a.size.y, self._b.size.y ) 
            )
        )
        
    def write_pixel(
        self,
        location: xy,
        ink: bool | None = True     
    ) -> None:
        self._a.write_pixel( location, ink )
        self._b.write_pixel( location, ink )
        
    def flush( self, forced: bool = False ) -> None:
        self._a.flush( forced )       
        self._b.flush( forced )
        
    def clear( self, ink: bool = False ) -> None:
        self._a.clear( ink )
        self._b.clear( ink )
        
        
# ===========================================================================   

class _canvas_inverted( canvas ):
    """
    helper class that inverts a canvas    
    """
    
    def __init__( self, subject: canvas ):
        self._subject = subject
        canvas.__init__( self, subject.size )
        
    def write_pixel(
        self,
        location: xy,
        ink: bool | None = True       
    ) -> None:
        self._subject.write_pixel( 
            location, 
            None if ink is None else not ink 
        )  
        
    def flush( self, forced: bool = False ) -> None:
        self._subject.flush( forced )
        
    def clear( self, ink: bool = False ) -> None:
        self._subject.clear( not ink )       


# ===========================================================================   

class _canvas_folded( canvas ):
    """
    helper class that folds a canvas    
    """
    
    def __init__( self, subject: canvas, n: int, zigzag: bool ):
        self._subject = subject
        self._n = n
        self._zigzag = zigzag
        canvas.__init__(
            self,
            xy( subject.size.x // n, subject.size.y * n ),
            is_color = subject.is_color,
            background = subject.background
        )
        
    def _write_pixel_implementation(
        self,
        location: xy,
        ink: bool | color        
    ) -> None:
        x, y = location.x, location.y
        if self._zigzag and ( ( y % 2 ) == 1 ):
            x = self.size.x - ( x + 1 )
        x = x + self.size.x * ( y // self._subject.size.y )
        y = y % self._subject.size.y
        self._subject._write_pixel_implementation( xy( x, y ), ink )  
        
    def _flush_implementation( self ) -> None:
        self._subject._flush_implementation()
        
    def _clear_implementation(
        self,
        ink: bool | color
    ) -> None:
        self._subject._clear_implementation( ink )       


# ===========================================================================   

class _canvas_part( canvas ):
    """
    helper class that is part of a canvas
    """
    
    def __init__( self, subject, start, size ):
        self._subject = subject
        self._start = start
        canvas.__init__( self, size )

    def write_pixel(
        self,
        location: xy,
        ink: bool | None = True       
    ) -> None:
        if self.within( location ):
            self._subject.write_pixel( self._start + location, ink )      
       
    def flush( self, forced: bool = False ) -> None:
        self._subject.flush( forced )
        
    # can't use the subject clear() method, because that
    # would clear all of the subject, and with our background
        
        
# ===========================================================================   

class _canvas_transformed( canvas ):
    """
    helper class that is a transformed version of the canvas
    """
    
    def __init__( self, subject, size, transform_location ):
        self._subject = subject
        self._transform_location = transform_location
        canvas.__init__(
            self,
            size = size,
            is_color = subject.is_color,
            background = subject.background
        )

    def write_pixel(
        self,
        location: xy,
        ink: bool | None = True        
    ) -> None:
        p = self._transform_location( location )
        if self._subject.within( p ):        
            self._subject.write_pixel( p, ink )      
       
    def flush( self, forced: bool = False ) -> None:
        self._subject.flush( forced )
        
    def clear( self, ink: bool = False ) -> None:
        self._subject.clear( ink )    
        
        
# ===========================================================================

class _canvas_extend( canvas ):
    """
    helper class that extends a canvas to te right
    """
    
    def __init__( 
        self, 
        a: canvas, 
        b: canvas, 
        size: xy,
        a_delta: xy, 
        b_delta: xy 
    ):
        self._a = a
        self._b = b
        self._a_delta = a_delta
        self._b_delta = b_delta
        canvas.__init__( self, size )

    def write_pixel(
        self,
        location: xy,
        ink: bool | None = True        
    ) -> None:
        p = location + self._a_delta
        if self._a.within( p ):
            self._a.write_pixel( p, ink )
  
        p = location + self._b_delta
        if self._b.within( p ):
            self._b.write_pixel( p, ink )
       
    def flush( self, forced: bool = False ) -> None:
        self._a.flush( forced )       
        self._b.flush( forced )
        
    def clear( self, ink: bool = False ) -> None:
        self._a.clear( ink )       
        self._b.clear( ink )       
        
# ===========================================================================
