# ===========================================================================
#
# file     : gf_terminal.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the (abstract) character terminal class.
#
# ===========================================================================

from godafoss.gf_xy import *


# ===========================================================================

class terminal:
    """
    character terminal

    :param size: (:class:`~godafoss.xy`)
        horizontal and vertical size, in characters

    A character terminal is a fixed size rectangular area of
    (ASCII) characters.
    The x and y coordinates are 0-origin and count to the right and down.
    In other words, the top-left character position is (0,0),
    and the bottom right character position is size - (1,1).

    $insert_image( "terminal-coordinates", 1, 500 )

    A terminal has a cursor, which is the location (x y coordinates) where
    the write() function will put the next character (and advance x by 1).

    A terminal doesn't scroll:
    when the cursor is outside the visible character area
    (beyond the end of the line, or beyond the number of lines)
    any characters written will be ignored.

    The following characters are treated special:
       - \\\\n puts the cursor at the first position of the next line
       - \\\\r puts the cursor at the start of the current line
       - \\\\f puts the cursor at the top-left position and clears
         the terminal
       - \\\\txxyy puts the cursor at the position (xx,yy).
         The xx and yy must be ascii numeric characters. For instance
         \\\\t0501 puts the cursor at the 6th character of the second line.
    """

    # =======================================================================

    def __init__(
        self,
        size: xy
    ) -> None:
        self.size = size
        self.cursor = xy( 0, 0 )
        self._goto_state = 0

    # =======================================================================

    def _cursor_set_implementation( self ) -> None:
        """
        called after a change of the write location

        This function is called when the write location has
        been changed *except* when this was to the next x
        position due to a call to write_implementation.

        The default implementation does nothing.
        """

        return

    # =======================================================================

    def cursor_set(
        self,
        new_cursor: xy
    ) -> None:
        """
        put the cursor (write location) at xy

        :param new_cursor: (:class:`~godafoss.xy`)
            horizontal and vertical size, in characters
        """

        self.cursor = new_cursor
        self._cursor_set_implementation()

    # =======================================================================

    def _write_implementation(
        self,
        c: chr
    ) -> None:
        """
        the actual writing of a character

        :param c: (chr)
            the character to be written

        When this function is called, the the current cursor is
        guaranteed to be within the terminal, and the character is
        not one of the special characters (\\n, \\r, \\c)
        """

        raise NotImplementedError

    # =======================================================================

    def write_char(
        self,
        c: chr
    ) -> None:
        """
        write a single character

        :param c: (chr)
            the character to be written
        """

        # handle the cursor setting after a s'\t'

        v = ord( c ) - ord( '0' )
        if self._goto_state == 1:
            self._x = 10 * v
            self._goto_state += 1

        elif self._goto_state == 2:
            self._x += v
            self._goto_state += 1

        elif self._goto_state == 3:
            self._y = 10 * v
            self._goto_state += 1

        elif self._goto_state == 4:
            self._y += v
            self._goto_state = 0
            self.cursor_set( xy( self._x, self._y ) )

        # handle special characters

        elif c == '\t':
            self._goto_state = 1

        elif c == '\n':
            self.cursor_set( xy( 0, self.cursor.y + 1 ) )

        elif c == '\r':
            self.cursor_set( xy( 0, self.cursor.y ) )

        elif c == '\v':
            self.cursor_set( xy( 0, 0 ) )

        elif c == '\f':
            self.clear()

        # handle a normal char

        elif (
            ( self.cursor.x >= 0 )
            and ( self.cursor.x < self.size.x )
            and ( self.cursor.y >= 0 )
            and ( self.cursor.y < self.size.y )
        ):
            self._write_implementation( c )
            self.cursor = self.cursor + xy( 1, 0 )

    # =======================================================================

    def write(
        self,
        s: str
    ) -> None:
        """
        write a string

        :param s: (str)
            the string to be written
        """
        for c in s:
            self.write_char( c )

    # =======================================================================

    def clear( self ) -> None:
        """
        clear the terminal

        This function clears the terminal (writes a space to all positions)
        and puts the cursor at xy(0,0).
        The default implementation does this by writing spaces to all
        locations. A concrete implementation might provide
        a better (faster) way.
        """

        for y in range( 0, self.size.y ):
            self.cursor_set( xy( 0, y ) )
            for x in range( 0, self.size.x ):
                self.write( ' ' )
        self.cursor_set( xy( 0, 0 ) )

    # =======================================================================

# ===========================================================================
