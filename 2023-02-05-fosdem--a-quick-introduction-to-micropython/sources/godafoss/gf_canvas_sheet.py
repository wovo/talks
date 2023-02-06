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
# This file contains the (abstract) canvas class.
#
# ===========================================================================

from godafoss.gf_native import *
from godafoss.gf_tools import *
from godafoss.gf_invertible import *
from godafoss.gf_xy import *
from godafoss.gf_color import *
from godafoss.gf_display import *

from godafoss.gf_pins import *


# ===========================================================================

class canvas_sheet( display, invertible ):
    """
    graphic drawing area (abstract class)

    A canvas is a rectanglular area of pixels.
    The draw method draws (paints) a single pixel.

    A canvas has a size and (default) background color
    and foreground colors.
    When no foreground is specified, it is the
    negative (complement) of the background.
    """

    def __init__(
        self,
        size: xy,
        background: color,
        foreground: color = None
    ):
        self.background = background
        self.foreground = first_not_none( foreground, - background )
        display.__init__( size )
        invertible.__init__( self )

    # =======================================================================

    def draw_pixel_implementation(
        self,
        location: xy,
        ink: color
    ) -> None:
        """
        implementation of setting the color of a single pixel

        A concrete canvas implementation must implement this method.

        This method should not be called directly,
        only via the write_pixel method (NVI pattern).
        When called by the write_pixel method,
        the location has been checked to be inside the canvas,
        and the color has been determined (won't be None).
        """
        raise NotImplementedError

    # =======================================================================

    def draw_pixel(
        self,
        location: xy,
        ink: color | None = None
    ) -> None:
        """
        sets the color a single pixel

        This method checks whether the location is inside the canvas.
        If so, the write_pixel_implementation method is called.
        When no ink is specified, the ink color will be the complement of
        the canvas background.

        A canvas might be buffered: the drawing of pixels might
        be effectuated only when the flush() method is called.
        """

        ink = first_not_none( ink, self.foreground )
        if (
            within( location.x, 0, self.size.x - 1 )
            and within( location.y, 0, self.size.y - 1 )
        ):
            self.draw_pixel_implementation( location, ink )

    # =======================================================================

    def flush( self ) -> None:
        """
        effectuate the changes made to the canvas

        A concrete canvas implementation must implement this method.

        Call this method to effectuate changes made to the canvas.
        """
        raise NotImplementedError

    # =======================================================================

    def clear_implementation( self, ink: color ) -> None:
        """
        implementation of clearing the canvas

        A concrete canvas implementation can implement this method if
        a better (faster) way is available than looping over all pixels.
        """
        for x in range( 0, self.size.x ):
            for y in range( 0, self.size.y ):
                self.draw_pixel( xy( x, y ), ink )

    # =======================================================================

    def clear( self, ink: color | None = None ) -> None:
        """
        clear the canvas

        This method writes the indicated color to all pixels of
        the canvas.
        When no color is specified, the background of the canvas is used.
        """
        self.clear_implementation( first_not_none( ink, self.background ))

    # =======================================================================
    
    def draw( self, location:xy, thing ):
        thing.draw( self, location )

    # =======================================================================

    def folded( self, n: int ):
        return _folded_canvas( self, n )

    # =======================================================================

    def part( self, start: xy, size: xy ):
        return _canvas_part( self, start, size )

    # =======================================================================

    def color_transformed( self, color_transform ):
        return _canvas_transformed(
            self,
            color_transform = color_transform
        )

    # =======================================================================

    def inverted( self ) -> "canvas":
        """

        """
        return _canvas_transformed(
            self,
            color_transform =
                lambda ink: not ink
        )

    # =======================================================================

    def location_transformed( self, location_transform ):
        return _canvas_transformed(
            self,
            location_transform = location_transform
        )

    # =======================================================================

    def x_mirrored( self ):
        return _canvas_transformed(
            self,
            location_transform =
                lambda location: xy(
                    ( self.size.x - 1 ) - location.x,
                    location.y
                )
        )

    # =======================================================================

    def y_mirrored( self ):
        return _canvas_transformed(
            self,
            location_transform =
                lambda location: xy(
                    location.x,
                    ( self.size.y - 1 ) - location.y,
                )
        )

    # =======================================================================

    def xy_mirrored( self ):
        return _canvas_transformed(
            self,
            location_transform =
                lambda location: xy(
                    location.y,
                    location.x
                )
        )

    # =======================================================================

    def as_pin(
        self,
        location = None,
        on_color: color = colors.white,
        off_color: color = colors.black
    ):
        return self._as_pin( self, location, on_color, off_color )

    class _as_pin( pin_out ):

        def __init__( self, slave, location, on_color, off_color ):
            self._slave = slave
            self._location = location
            self._on_color = on_color
            self._off_color = off_color

        def write( self, value ):
            c = self._on_color if value else self._off_color
            if self._location is None:
                self._slave.draw_pixel( self._location, c )
            else:
                self._slave.clear( c )
            # self._slave.flush()

    # =======================================================================

    def as_x_port(
        self,
        y = 0,
        on_color: color = colors.white,
        off_color: color = colors.black
    ):
        return port_out( [
            self.as_pin( xy( x, y ), on_color, off_color )
            for x in range( 0, self.size.x )
        ] )

    # =======================================================================

    def demo_line( self ):
        "demo shows kitt display"
        print( "neopixels demo: red kitt on blue background" )
        kitt( self.as_port( colors.red, colors.blue / 50 ) )

    # =======================================================================

    def demo( self ):
        import godafoss.gf_canvas_demo
        godafoss.gf_canvas_demo.canvas_demo( self )


class _folded_canvas( canvas ):

    def __init__( self, main, n ):
        self.main = main
        self.n = n
        x = main.size.x // n
        y = n * main.size.y
        canvas.__init__( self, xy( x, y ), main.background )

    def draw_pixel_implementation( self, location: xy, ink ):
        x = location.x + ( location.y // self.main.size.y ) * self.size.x
        y = location.y % self.main.size.y
        self.main.draw_pixel( xy( x, y ), ink )

    def flush( self ):
        self.main.flush()


class _canvas_part( canvas ):

    def __init__( self, main, start, size ):
        self.main = main
        self.start = start
        canvas.__init__( self, size, main.background )

    def draw_pixel_implementation( self, location: xy, ink ):
        self.main.draw_pixel( self.start + location, ink )

    def flush( self ):
        self.main.flush()

    def clear( self, ink = None ):
        self.main.clear( ink )


class _canvas_transformed( canvas ):

    def __init__(
        self,
        main,
        size_transform = unity,
        location_transform = unity,
        color_transform = unity
    ):
        self.main = main
        self.size_transform = size_transform
        self.location_transform = location_transform
        self.color_transform = color_transform
        canvas.__init__(
            size_transform( self ),
            self.location_transform( self.main.size ),
            self.color_transform( self.main.background )
        )

    def draw_pixel_implementation( self, location: xy, ink ):
        self.main.draw_pixel(
            self.location_transform( location ),
            self.color_transform( ink )
        )

    def flush( self ):
        self.main.flush()
