# ===========================================================================
#
# file     : gf_tools.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains some basic tooling that is not
# MicroPytyhon specific and has no external dependencies.
#
# ===========================================================================

import machine


# ===========================================================================

def sign( x ):
   return 1 if x > 0 else -1 if x < 0 else 0

# ===========================================================================

def less( x, n = 1 ):
   return x - sign( x ) * n

# ===========================================================================

def unity(
    x: any
) -> any:
    """
    returns its argument unmodified

    :param x: any
        the object to be returned

    :result: any
        the parameter

    This function returns its argument unmodified.
    This is used as a do-nothing default for a parameter.

    example::
    $insert_example( "test_tools.py", "unity example", 1 )
    """
    return x


# ===========================================================================

def within(
    a: any,
    low: any,
    high: any
) -> bool:
    """
    test whether a value is between two bounds

    :param a: any
        the value to be checked

    :param low: any
        the lower bound to check the value against

    :param high: any
        the higher bound to check the value against

    :result: any
        whether a is in the trange [low..high]

    This function returns whether a is between low and high.
    The low and high values are included in the allowed range.

    Low and high must be in order: low =< high.
    If they are not the function will return False.

    examples::
    $insert_example( "test_tools.py", "within example", 1 )
    """
    return ( a >= low ) and ( a <= high )


# ===========================================================================

def clamp(
    x: any,
    low: any,
    high: any
) -> any:
    """
    x, clamped to the nearest value in the range [low..high]

    :param x: any
        the value to clamp within the range [low..high]

    :param low: any
        the lower bound of the clamp interval

    :param high: any
        the higher bound of the clamp interval

    :result: any
        either x, or the nearest value in the range [low..high]

    This function returns max( low, min( x, high ) ).

    examples::
    $insert_example( "test_tools.py", "clamp example", 1 )
    """

    return max( low, min( x, high ) )


# ===========================================================================

def invert_bits(
    value: int,
    n_bits: int
) -> int:
    """
    the value, with its lowqer n_bits bits inverted

    :param value: int
        the value to invert

    :param n_bits: int
        the number of valid bits in the value

    :result: int
        the value, with its lower n_bits bits inverted

    This function returns the value, of which n_bits are relevant,
    with those bits inverted.
    The higher bits in the returned value are 0 (clear).

    examples::
    $insert_example( "test_tools.py", "invert_bits example", 1 )
    """

    return ( ~ value ) & ( ( 0b1 << n_bits ) - 1 )


# ===========================================================================

def mirror_bits(
    value: int,
    n_bits: int
) -> int:
    """
    the value, with its lower n_bit bits mirrored

    :param value: int
        the value to mirror

    :param n_bits: int
        the number of valid bits in the value

    :result: int
        the value, with its lower n_bits bits mirrored

    This function returns the value, of which n_bits are relevant,
    with the bits mirrored (most significant bit becomse the least
    signififacnt bit and vice verse, etc.)
    The higher bits in the returned value are 0 (clear).

    examples::
    $insert_example( "test_tools.py", "mirror_bits example", 1 )
    """

    result = 0
    for _ in range( n_bits ):
        result = ( result << 1 ) | ( value & 0b01 )
        value = value >> 1
    return result


# ===========================================================================

def bar_bits(
    n_bits: int
) -> int:
    """
    unsigned int value with (only) the lower n_ones bits 1

    :param n_bits: int
        the number of 1-value bits in the result

    :result: int
        unsigned int value, with (only) the lower n_bits bits 1

    This function returns the integer value,
    of which the lowest n_ones bits
    are 1 (set), the other (higher) bits are 0 (clear).

    examples::
    $insert_example( "test_tools.py", "bar_bits example", 1 )
    """

    result = 0
    for _ in range( n_bits ):
        result = ( result << 1 ) | 0b1
    return result


# ===========================================================================

def is_iterable(
    x: any
) -> bool:
    """
    test for iterability

    :param x: any
        the object to be tested for iterability

    :result: bool
        whether x is iterable

    The standard way to test for iterability is to use
    from collections.abc import Iterable,
    but this is not (yet?) available in MicroPython.
    Hence this workaround.
    """
    try:
        for _ in x:
            return True
        return True
    except TypeError:
        return False


# ===========================================================================

def first_not_none(
    *args: any
) -> any:
    """
    return the first not None argument

    :param args: any
        the arguments that are considered

    :result: any
        the first of the \*args that is not None

    This function returns the first argument that is not None.
    It is usefull to replace a default of None with
    a default value that can't be specified as a default.

    When there is only one argument and it is iterable,
    it is used as the list of alternatives.

    If all arguments are None, None is returned.

    examples::
    $insert_example( "test_tools.py", "first_not_none example", 1 )
    """

    if ( len( args ) == 1 ) and is_iterable( args[ 0 ] ):
        args = args[ 0 ]

    for x in args:
        if x is not None:
            return x

    return None


# ===========================================================================

def make_tuple(
    *args: any
) -> any:
    """
    make a tuple from a tuple or list, or from a number of arguments

    :param \*args: any
        the arguments are to be turned into a tuple

    :result: any
        a tuple constructed from the \*args

    When called with one argument, which is a list or a tuple,
    this function returns it as a tuple.
    Otherwise, it returns a tuple of its argument(s).

    examples::
    $insert_example( "test_tools.py", "make_tuple example", 1 )
    """

    if len( args ) == 1 and isinstance( args[ 0 ], ( list, tuple ) ):
        return tuple( args[ 0 ] )
    else:
        return tuple( args )


# ===========================================================================

def make_list(
    *args: any
) -> any:
    """
    make a list from a tuple or list, or from a number of arguments

    :param args: any
        the arguments are to be turned into a list

    :result: any
        a list constructed from the \*args

    When called with one argument, which is a list or a tuple,
    this function returns it as a list.
    Otherwise, it returns a list of its argument(s).

    examples::
    $insert_example( "test_tools.py", "make_list example", 1 )
     """

    if len( args ) == 1 and isinstance( args[ 0 ], ( list, tuple ) ):
        return list( args[ 0 ] )
    else:
        return list( args )


# ===========================================================================

def nth_from(
    n: int | bool,
    *args: any
) -> any:
    """
    the n-th argument

    :param n: int | bool
        the index into the arguments

    :param \*args: any
        the arguments from which the n-th is to be selected

    :result: any
        the n-th of the \*args

    This function returns the n-th of the \*args.
    If the number of \*args is 1 and it is a list or tuple,
    the function returns the n-th element from it
    (the first element is the 0th).

    If the n argument is a boolean, it will be interpreted
    as 0 and 1, and the number of things to choose from must
    be 2.
    Note that in that case the false-option comes first,
    which is unlike a Python conditional expression
    or a c \/ c++ ?-expression.

    examples::
    $insert_example( "test_tools.py", "nth_from example", 1 )
    """

    options = make_tuple( *args )

    if isinstance( n, bool ):
        n = int( n )
        if len( options ) != 2:
            raise IndexError

    return options[ n ]


# ===========================================================================

def bytes_from_int(
    value: int,
    n_bytes: int
) -> bytes:
    """bytes lsb-first representation of an int

    :param value: int
        the value to be converted to bytes

    :param n_bytes: int
        the desired number of bytes

    :result: bytes
        the bytes representation of the value

    This function returns the int value as n_byte bytes,
    least significant byte first (little endian).

    examples::
    $insert_example( "test_tools.py", "bytes_from_int example", 1 )
    """

    array = bytearray( n_bytes )
    for i in range( 0, n_bytes ):
        array[ i ] = value & 0xFF
        value = value >> 8
    return bytes( array )


# ===========================================================================

def int_from_bytes(
    array: bytes | bytearray,
    signed: bool = False
) -> int:
    """int value from a lowest-byte-first sequence of bytes

    :param array: bytes | bytearray
        the array of bytes that is to be converted to an integer
        
    :param signed: bool
        treat the resulting bit pattern as unsigned (False, default)
        or signed (True)

    :result: int
        the array interpreted as integer value

    This function returns the bytes as an unsigned integer value,
    the first byte as least significant byte of the int value.
    
    Python has the int.from_bytes function, but it is currently
    not implemented fully and correctly in MicroPython.
    Hence this alternative.

    examples::
    $insert_example( "test_tools.py", "int_from_bytes example", 1 )
    """

    result = 0
    for i in range( len( array ) - 1, -1, -1 ):
        result = ( result << 8 ) | ( array[ i ] & 0xFF )     
        
    if signed and ( ( array[ -1 ] & 0x80 ) != 0 ):
        result = - ( ( result - 1 ) ^ bar_bits( 8 * len( array ) ) )
        
    return result 

    
# ===========================================================================

def elapsed_us( f ):
    """
    execute function and return the elapsed time in microseconds
    """
    
    from godafoss.gf_time import ticks_us
    
    before = ticks_us()
    f()
    after = ticks_us()
    return after - before    


# ===========================================================================

class immutable:
    """
    make an object immutable

    Python names are references, and class objects are mutable,
    so a class member variable can inadvertently be modified.
    The xy class is immutable, but if it were not, this would
    be possible::

        origin = xy( 0, 0 )
        a = origin
        a.x = 10 # this modifies the object that origin references!
        print( origin.x ) # prints 10

    To prevent such modifications, a value class inherits from freeze,
    and calls immutable._init__( self ) when all its members
    have been initialized.

    $macro_start immutable
    Values (objects) of this class are immutable.
    $macro_end

    usage example::
    $insert_example( "test_tools.py", "immutable example", 1 )
    """

    _frozen = False

    # =======================================================================

    def __init__( self ) -> None:
        """
        after the initialization, the object members can't be modified
        """
        self._frozen = True

    # =======================================================================

    def __delattr__( self, *args, **kwargs ):
        if self._frozen:
            raise TypeError( "immutable object" )
        object.__delattr__( self, *args, **kwargs )

    # =======================================================================

    def __setattr__( self, *args, **kwargs ):
        if self._frozen:
            raise TypeError( "immutable object" )
        object.__setattr__( self, *args, **kwargs )

    # =======================================================================


# ===========================================================================

class repeater:
    """
    iterate the indicated number of iterations, or forever when None

    :param iterations: int | None
        the number of iterations, or None for infinite iterationfs

    This iterator is usefull for iterative demos that by default
    must run forever, but might be used to run a fixed numer of times.

    examples::

        for _ in repeater( 10 ): ...  # ... is repeated 10 times
        for _ in repeater( None ): ...  # ... is repeated forever
    """

    # =======================================================================

    def __init__(
        self,
        iterations: int | None
    ) -> None:
        self.iterations = iterations
        self.n = None

    # =======================================================================

    def __iter__( self ):
        self.n = 0
        return self

    # =======================================================================

    def __next__( self ):
        if self.iterations is not None:
            self.n += 1
            if self.n > self.iterations:
                raise StopIteration
        return self.n

    # =======================================================================
    
# ===========================================================================

class remember:
    """
    """
        
    def __init__( self, addresses ):
        self._addresses = [ address for address in addresses ]
        self._data = [ machine.mem32[ address ] for address in addresses ]
        
    def restore( self ):
        for address, data in zip( self._addresses, self._data ):
            machine.mem32[ address ] = data
    

# ===========================================================================
