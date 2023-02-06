#============================================================================
#
# file     : gf_make_pins.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the functions that make pins.
#
# ===========================================================================

from godafoss.gf_pins import *
from godafoss.gf_gpio import *


# ===========================================================================

def make_pin_in( 
    p: None | int | pin_in | pin_in_out | pin_oc
) -> pin_in:
    """
    make a pin_in
    
    This function returns a pin_in if one can be made from its
    parameter, which can be a pin number, a pin_in, a pin_in_out,
    a pin_oc, or None.
    
    $macro_start make_pin_in_types
    int, 
    :class:`~godafoss.pin_in`, 
    :class:`~godafoss.pin_in_out`, 
    :class:`~godafoss.pin_oc`
    $macro_end      
    """
    
    if p is None:
        return pin_in_dummy
    
    if isinstance( p, int ):
        if p < 0:
            return pin_in_dummy
        else:
            return gpio_in( p )
        
    return p.as_pin_in()    
    

# ===========================================================================

def make_pin_out( 
    p: None | int | pin_out | pin_in_out | pin_oc 
) -> pin_out:
    """
    make a pin_out
    
    This function returns a pin_out if one can be made from its
    parameter, which can be a pin number, a pin_out, a pin_in_out,
    or a pin_oc.
    
    When the parameter is a pin_oc, the returned pin_out won't
    drive its physical pin high: a suitable pull-up must be provided
    to do that.
    
    $macro_start make_pin_out_types
    int, 
    :class:`~godafoss.pin_out`, 
    :class:`~godafoss.pin_in_out`, 
    :class:`~godafoss.pin_oc`
    $macro_end    
    """
    
    if p is None:
        return pin_out_dummy
    
    if isinstance( p, int ):
        if p < 0:
            return pin_out_dummy            
        else:            
            return gpio_out( p )
        
    return p.as_pin_out()        
    

# ===========================================================================

def make_pin_in_out( 
    p: None | int | pin_in_out | pin_oc 
) -> pin_in_out:
    """
    make a pin_in_out
    
    This function returns a pin_in_out if one can be made from its
    parameter, which can be a pin number, a pin_in_out,
    or a pin_oc.
    
    When the parameter is a pin_oc, the returned pin_in_out won't
    drive its physical pin high: a suitable pull-up must be provided
    to do that.
    
    $macro_start make_pin_in_out_types
    int, 
    :class:`~godafoss.pin_in_out`, 
    :class:`~godafoss.pin_oc`
    $macro_end      
    """
    
    if p is None:
        return pin_in_out_dummy    
    
    if isinstance( p, int ):
        if p < 0:
            return pin_in_out_dummy
        else:
            return gpio_in_out( p )
        
    return p.as_pin_in_out()     


# ===========================================================================

def make_pin_oc( 
    p: None | int | pin_in_out | pin_oc 
) -> pin_oc:
    """
    make a pin_oc
    
    This function returns a pin_out if one can be made from its
    parameter, which can be a pin number, a pin_in_out,
    or a pin_oc.
    
    $macro_start make_pin_oc_types
    int, 
    :class:`~godafoss.pin_in_out`, 
    :class:`~godafoss.pin_oc`
    $macro_end     
    """
    
    if p is None:
        return pin_oc_dummy    
    
    if isinstance( p, int ):
        if p < 0:
            return pin_oc_dummy              
        else:
            return gpio_oc( p )
        
    return p.as_pin_oc()    
  
  
# ===========================================================================
