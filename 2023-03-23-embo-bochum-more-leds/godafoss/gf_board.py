# ===========================================================================
#
# file     : gf_board.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the trampoline to the board modules.
#
# ===========================================================================

def board( 
    name: str, 
    *args, **kwargs 
):   
    """
    get a board object
    
    :param name: str
        the name of the board
        
    :param args,kwargs:
        further parameters (if any) are passsed to the board constructor        

    :result: 
        board object
        
    This function returns a board object.
    A board object provides easy access to the peripherals on the board.
    
    $macro_start board
    To obtain an instance of this class, 
    use the :func:`~board` function with "$1" as argument.
    $macro_end
    """

    exec( "from godafoss.gf_board_%s import board_%s" % ( name, name ) )
    return eval( "board_%s" % name )( *args, **kwargs )
    

# ===========================================================================
