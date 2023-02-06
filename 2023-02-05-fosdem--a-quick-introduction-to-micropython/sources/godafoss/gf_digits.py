# ===========================================================================
#
# file     : gf_digits.py
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
from godafoss.gf_pins import *


# ===========================================================================

class digits:
    """
    seven-segments display

    :param n: int
        the number of digits

    :param digit_order: Iterable[ int ] | None
        the number of digits

    This class abstracts a seven-segment display.

    When the digit_order is not specified, it is range( n ).

    When the digit_order is specified, it is the order in which the
    numerical digits are placed.
    When this digit_order skips some digits, those are not
    considered numeric digits, and they are not included in the
    p count, and are not used by the write() method.
    Such 'digits' can still be written by the write_digit_segments()
    method.

    The n attribute is the number of digits.
    The p ttribute is the number of numeric digits.
    The segments attribute provides the translation from value
    to active segments.
    The LSB is segment a, the MSB - 1 is segment g.
    """

    segments = {
        '0': 0b_0011_1111,
        '1': 0b_0000_0110,
        '2': 0b_0101_1011,
        '3': 0b_0100_1111,
        '4': 0b_0110_0110,
        '5': 0b_0110_1101,
        '6': 0b_0111_1101,
        '7': 0b_0000_0111,
        '8': 0b_0111_1111,
        '9': 0b_0110_1111,
        ' ': 0b_0000_0000,
        '-': 0b_0100_0000,
        '_': 0b_0000_1000,
        'h': 0b_0111_0100,
        'H': 0b_0111_0110,
        'o': 0b_0101_1100,
        'C': 0b_0110_0001,
        'c': 0b_0101_1000,
    }
    

    # =======================================================================

    def __init__(
        self,
        n: int,
        digit_order: Iterable[ int ] = None
    ):
        self.n = n
        self._digit_order = \
            digit_order if digit_order is not None else list( range( n ) )
        self.p = len( self._digit_order )
        self._dirty = True

    # =======================================================================

    def write_digit_segments(
        self,
        n: int,
        v: int
    ):
        """
        write the segments of a single digit

        :param n: int
            the digit that is written

        :param v: int
            the seven-segment value

        This method writes the 8-bit value v to the segments of digit n.
        The digit order (optional constructor parameter) is NOT
        taken into account by this method.
        The LSB is written to segment a, the MSB to the decimal point.

        When n is outside the number of valid digits,
        the write_digit_segments() call has no effect.

        A segments display can be buffered, so a flush() call might be
        required to effectuate what was written by write_digit_segments()
        calls.
        """

        raise NotImplementedError
        
    # =======================================================================

    def write_digits(
        self,
        values: Iterable[ int ]
    ):
        """
        write the 8-bit values to the segments of the digits
        
        :param values: Iterable[ int ]
            the values to write to the numeric digits        

        This method writes the 8-bit values to the digits 
        of the display, starting at the leftmost one.
        The digit order (optional constructor parameter) is NOT
        taken into account by this method.        
        Excess values (beyond the number of numerical digits in the display)
        are ignored.
        """

        for i, s in enumerated( values ):
            write_digit_segments( i, s )        

    # =======================================================================

    def flush(
        self,
        forced: bool = False
    ) -> None:
        """
        effectuate what was written to the display

        :param forced: bool
            True forces a flush, even when no changes were made

        Writes to the 7 segment display can be buffered.
        If so, a flush() method call is required to effectuate
        what was written.

        A flush() call might be a no-op when nothing was written since
        the previous flush() call, unless the forced parameter is True.
        """

        if self._dirty or forced:
            self._dirty = False
            self._flush_implementation()

    # =======================================================================

    def _flush_implementation( self ) -> None:
        """
        flush the content (concrete implementation)

        This method must be implemented by a concrete class.
        """

        raise NotImplementedError

    # =======================================================================

    def write(
        self,
        s: str,
        points: Iterable[ bool ] = (),
        align = True,
        ink: bool = True,
        flush: bool = True
    ):
        """
        write a string to the display

        This method writes the string s to the display.
        Valid characters that are the digits 0-9, the characters
        hHoCc-_ and the space.
        A point or comma enables the decimal point of the previous digit.
        Other characters are ignored.

        The valid characters and their representation in segments
        are stored in the segments attribute.
        Characters can be added or changed if desired.

        By default, the result will be written right-aligned: spaces
        (digits with no segments enabled) will be prepended to
        fill the number of digits in the display.
        When the align parameter is False, result will be
        written left-aligned (spaces will be appended instead of prepended).

        The decimal points can also be enabled by the elements
        of the points parameter.
        Each element enables the decimal point of
        one digit in the result (after alignment).

        By default, enabled segments will light up.
        When the ink parameter is False, this will  be reversed:
        non-enabled segments will light up.

        By default, the display will be updated (flush() call).
        When the flush parameter is False no flush() will be called,
        hence a flush() call might be needed to effectuate the write.
        
        This method takes the digit_order (optional constructor parameter) 
        into account. Digits that are not present in the digit_order
        are skipped.
        """

        result = []
        for c in s:

            if c in [ ",", "." ]:
                if len( result ) > 0:
                    result[ -1 ] = result[ -1 ] | 0x80

            elif c in self.segments:
                result.append( self.segments[ c ] )

            else:
                # ignore other characters
                pass

        while len( result ) < self.p:
            if align:
                result.insert( 0, 0 )
            else:
                result.append( 0 )

        for i, point in enumerate( points ):
            if ( i < self.p ) and point:
                result[ i ] = result[ i ] | 0x80

        for i, v in enumerate( result ):
            if not ink:
                v = 0xFF ^ v
            if i < self.p:
                self.write_digit_segments( self._digit_order[ i ], v )

        if flush:
            self.flush()

    # =======================================================================

    def demo(
        self,
        iterations = None
    ):
        """
        seven-segment display demo
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
