# ===========================================================================
#
# file     : gf_sr04.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the xxxx
#
# ===========================================================================

import micropython
import gc
import os
    

# ===========================================================================

def print_info():
    """
    print the target name and some memory information

    This function is meant to give a quick impression of your target system.
    """
    
    # this line is not needed in this function within godafoss,
    # but with it you can cut-n-paste, this function to use it outside
    # godafoss, for instance to explore a new target
    import gc, os, micropython

    gc.collect()
    print( "Name           %8s"  % ( "'" + os.uname()[ 0 ] ) + "'" )
    print( "RAM allocated %8d B" % gc.mem_alloc() )
    print( "RAM free      %8d B" % gc.mem_free() )
    
    try:
        s = os.statvfs( "//" )
        print( "FLASH free    %8d B" % ( s[ 0 ] * s[ 3 ] ) )
    except: 
        print( "target has no os.statvfs()" )    

    print( "mem info:" )
    micropython.mem_info()