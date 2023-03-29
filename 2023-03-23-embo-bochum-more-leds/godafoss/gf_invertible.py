# ===========================================================================
#
# file     : gf_invertible.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the invert modifier and the
# (abstract) invertible class.
#
# ===========================================================================


# ===========================================================================

class invertible:
    """
    object that can be inverted

    Invertible objects can be inverted by using either:

    - the - operator
    - the .inverted() method
    - the invert modifier (applied using the @ operator)

    A class is invertible when it inherits from invertible,
    and implements the inverted() method.

    As an optimization, inverting an object twice might
    return the original object.

    examples::
    $insert_example( "test_invertible.py", "invertible examples", 1 )

    $macro_start invertible
    An inverted version of an object of this class can be obtained
    by applying either the .inverted() method, the unary minus - operator,
    or the invert modifier (applied using the @ operator).
    $macro_end
    """

    def __init__( self ) -> None:
        pass

    def inverted( self ) -> "invertible":
        """must be implemented by a concrete subclass of invertible

        A class that wants to be invertible must inherit from
        invertible and implementd the inverted() function.
        Typically, this function returns a proxy object that implements
        the same interface as the inverted object, but with the
        'polarity' of its operations reversed.
        For instance, a normal GPIO pin reads True when the pin
        is high, when the inverted GPIO pin is read it will
        will read True when the pin is low.
        """
        raise NotImplementedError

    def __neg__( self ) -> "invertible":
        return self.inverted()


# ===========================================================================

class _invert_modifier( invertible ):

    def __init__( self ):
        invertible.__init__( self )

    def __matmul__( self, subject ) -> "invertible":
        return subject.inverted()

    def inverted( self ) -> "invertible":
        return _unity_modifier()


# ===========================================================================

class _unity_modifier( invertible ):

    def __init__( self ):
        invertible.__init__( self )

    def __matmul__( self, subject: "invertible" ) -> "invertible":
        return subject

    def inverted( self ) -> "invertible":
        return _invert_modifier()


# ===========================================================================

invert = _invert_modifier()


# ===========================================================================
