# ===========================================================================
#
# file     : gf_sheet.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the (abstract) canvas class.
#
# ===========================================================================

from godafoss.gf_tools import *
from godafoss.gf_xy import *
from godafoss.gf_invertible import *
from godafoss.gf_shape import *


# ===========================================================================

class sheet( invertible ):
    """
    monochrome graphic drawing area (abstract class)
    
    $insert_image( "canvas-coordinates", 1, 500 )    

    A sheet is a rectanglular area of monochrome pixels.
    A sheet has a size, which is the number of pixels in
    the x and y directions.
    The top-left pixel is at xy( 0, 0 ), the bottom-right pixel is
    at xy(sheet.size.x - i, sheet.size.y - 1).
    
    The write_pixel method writes a single pixel.
    The write method writes a :class:`~godafoss.shape`.
    
    Sheets can be added, which creates a sheet that writes
    to both constituent sheets.
    
    $macro_start sheet
    This class implements the :class:`~godafoss.sheet` interface, 
    which provides functionality to write shapes 
    (:class:`~godafoss.line`, :class:`~godafoss.circle`, 
    :class:`~godafoss.rectangle`, :class:`~godafoss.text`),
    to derive modified sheets 
    (inverted, mirrored, rotated, parts, combinations, etc.),
    and a comprehensive demo.
    $macro_end
    """

    # =======================================================================

    def __init__(
        self,
        size: xy
    ):
        self.size = size
        invertible.__init__( self )

    # =======================================================================

    def write_pixel(
        self,
        location: xy,
        ink: bool | None = True
    ) -> None:
        """
        write a pixel
        
        :param location: (:class:`~godafoss.xy`)
            the location of the pixel that is to be written 
        
        :param ink: (None, bool)
            the value to be written to the pixel        

        This method writes a single pixel.

        A sheet might be buffered: the writing of pixels might
        be effectuated only when the flush() method is called.
        
        $macro_start sheet_write_pixel
        write a pixel
        
        :param location: (:class:`~godafoss.xy`)
            the location of the pixel that is to be written 
        
        :param ink: (None, bool)
            the value to be written to the pixel
            
        When the location is within the sheet, 
        and the ink parameter is not None, 
        the ink is written to the pixel.
        The default value of ink (True) writes the sheet
        foreground, False writes the sheets background.
        
        Writes are buffered: a flush call is required
        to write changed pixels to the screen.
        $macro_end
        """
        
        raise NotImplementedError
        
    # =======================================================================

    def flush( 
        self, 
        forced: bool = False 
    ) -> None:
        """
        effectuate what was written to the sheet
        
        :param forced: (bool)
            True forces a flush, even when no pixels were written

        Writes to the sheet can be buffered.
        If so, a flush() method call is required to effectuate
        the write_pixel() calls.
        
        A flush() call might be a no-op when no pixels were changed since
        the previous flush() call, unless the forced parameter is True.
        
        $macro_start sheet_flush
        effectuate what was written
        
        :param forced: (bool)
            True forces a flush, even when no pixels were written        

        Writes to the display are buffered:
        a flush() method call is required to effectuate what was written.
        
        A flush() call is a no-op when no pixels were changed since
        the previous flush() call, unless the forced parameter is True.        
        $macro_end        
        """ 
        
        raise NotImplementedError        

    # =======================================================================
    
    def within( 
        self, 
        location: xy 
    ):
        """
        check if the location is within the sheet
        
        :param location: (:class:`~godafoss.xy`)
            the location coordinates to be checked     
        
        This method returns True iff the location
        is within the sheet.
        """
        
        return (
            within( location.x, 0, self.size.x - 1 )
            and within( location.y, 0, self.size.y - 1 ) )

    # =======================================================================
    
    def write( 
        self, 
        thing: shape,
        location: xy = xy( 0, 0 )        
    ) -> None:
        """
        write a :class:`~godafoss.shape`
        
        The write() method calls the write() method of the 
        :class:`~godafoss.shape` to write itself to the sheet.
        """
        
        thing.write( self, location )
        
    # =======================================================================

    def clear( 
        self, 
        ink: bool = False 
    ) -> None:
        """
        clear the display
        
        :param ink: (bool)
            the 'color' to write to all pixels
        
        This method clears the display.
        The default implementation writes False to all individual pixels.
        A concrete sheet might implement a faster method.

        A display might be buffered: a clear() call might
        be effectuated only when the flush() method is called.
        
        $macro_start sheet_clear
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
                
        for x in range( 0, self.size.x ):
            for y in range( 0, self.size.y ):
                self.write_pixel( xy( x, y ), ink )
            
    # =======================================================================
    
    def demo(
        self,
        iterations = None
    ):
        from godafoss.gf_sheet_demos import sheet_demo
        sheet_demo( self, iterations )
    
    # =======================================================================
    
    def __add__( 
        self, 
        other: "sheet" 
    ) -> "sheet":
        return _sheet_add( self, other )  
        
    # =======================================================================

    def inverted( self ) -> "sheet":
        """
        inverse of the display

        This method returns a display that inverts the effect 
        of write_pixel() calls.
        """
        
        return _sheet_inverted( self )        
        
    # =======================================================================

    def folded( self, n: int ) -> "sheet":
        """
        folded version of the display

        This method returns a display corresponds to te original one,
        folded by n.
        """
        
        return _sheet_folded( self, n )        
        
    # =======================================================================

    def part( 
        self, 
        start: xy, 
        size: xy 
    ) -> "sheet":
        """
        part of the sheet

        This method returns a new sheet that is 
        part of the original sheet, as specified by the
        start and size parameters.
        
        The clear() method of a sheet part can be significantly slower
        than the clear() of the original sheet, because it can't use
        the clear() of the driver (which often has a fast way to clear 
        the whole sheet).
        """
        
        return _sheet_part( self, start, size )         
        
    # =======================================================================

    def rotated( 
        self, 
        rotation: int 
    ) -> "sheet":
        """
        rotated version of the sheet

        This method returns a sheet that is 
        a rotated version of the original sheet.
        Allowed rotation values are 0, 90, 180 and 270.
        """
        
        if rotation == 0:
            return _sheet_transformed( 
                self, 
                self.size, 
                lambda c: xy( c.x, c.y )
            )
            
        elif rotation == 90:
            return _sheet_transformed( 
                self, 
                xy( self.size.y, self.size.x ),
                lambda c: xy( self.size.x - 1 - c.y, c.x )
            )
            
        elif rotation == 180:
            return _sheet_transformed( 
                self, 
                self.size, 
                lambda c: xy( self.size.x - 1 - c.x, self.size.y - 1 - c.y )
            )
            
        elif rotation == 270:
            return _sheet_transformed( 
                self, 
                xy( self.size.y, self.size.x ), 
                lambda c: xy( c.y, self.size.y - 1 - c.x ) 
            )    
            
        else:
            raise ValueError( "rotation must be 0, 90, 180 or 270" )       
        
    # =======================================================================

    def extended( 
        self, 
        other: "sheet", 
        direction: str = "EN"
    ) -> "sheet":
        """
        extension of the sheet

        This method returns a sheets that extends the sheet.
        
        The direction determines where the other sheet is placed
        relative to the original sheet (north, east, south or west),
        and which part of the sheets is aligned 
        (again: north, east, south or west).
        Valid values for the direction are
        "ES", "EN", "WS", "WN", "NW", "NE", "SW", "SE".
        """
        
        if len( direction ) != 2:
            raise ValueError( "direction must be 2 characters" )
            
        direction, alignment = direction            
            
        # which sheet comes first    
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
        
        return _sheet_extend( a, b, size, - a_shift, - b_shift )          

    # =======================================================================


# ===========================================================================  
#
# helper classes
# 
# ===========================================================================

class _sheet_add( sheet ):
    """
    helper class that adds two sheets
    """
    def __init__( 
        self, 
        a: sheet, 
        b: sheet 
    ):
        self._a = a
        self._b = b
        sheet.__init__(
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

class _sheet_inverted( sheet ):
    """
    helper class that inverts a sheet    
    """
    
    def __init__( self, subject: sheet ):
        self._subject = subject
        sheet.__init__( self, subject.size )
        
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

class _sheet_folded( sheet ):
    """
    helper class that folds a sheet    
    """
    
    def __init__( self, subject: sheet, n: int ):
        self._subject = subject
        self._n = n
        sheet.__init__( self, xy( subject.size.x // n, subject.size.y * n ) )
        
    def write_pixel(
        self,
        location: xy,
        ink: bool | None = True       
    ) -> None:
        if self.within( location ):
            self._subject.write_pixel( 
                xy(
                    location.x + self.size.x * ( location.y // self._subject.size.y ),
                    location.y % self._subject.size.y
                ),
                ink 
            )  
        
    def flush(
        self,
        forced: bool = False
    ) -> None:
        self._subject.flush( forced )
        
    def clear(
        self,
        ink: bool = False
    ) -> None:
        self._subject.clear( ink )       


# ===========================================================================   

class _sheet_part( sheet ):
    """
    helper class that is part of a sheet
    """
    
    def __init__( self, subject, start, size ):
        self._subject = subject
        self._start = start
        sheet.__init__( self, size )

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

class _sheet_transformed( sheet ):
    """
    helper class that is a transformed version of the sheet
    """
    
    def __init__( self, subject, size, transform_location ):
        self._subject = subject
        self._transform_location = transform_location
        sheet.__init__( self, size )

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

class _sheet_extend( sheet ):
    """
    helper class that extends a sheet to te right
    """
    
    def __init__( 
        self, 
        a: sheet, 
        b: sheet, 
        size: xy,
        a_delta: xy, 
        b_delta: xy 
    ):
        self._a = a
        self._b = b
        self._a_delta = a_delta
        self._b_delta = b_delta
        sheet.__init__( self, size )

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
