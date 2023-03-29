# ===========================================================================
#
# file     : gf_target_rp2040.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains specific things for the rp2040 target.
#
# ===========================================================================


# ===========================================================================
#
# DMA
#
# ===========================================================================

_rp2040_number_of_dma_channels = 8
_dma_channel_free_list = [ 
    True for _ in range( _rp2040_number_of_dma_channels ) 
]

# ===========================================================================

def dma_channel_get() -> int:
    for channel in range( _rp2040_number_of_dma_channels ):
        if _dma_channel_free_list[ channel ]:
            _dma_channel_free_list[ channel ] = False
            return channel
    return None        
    

# ===========================================================================

def dma_channel_release( channel: int ):
    _dma_channel_free_list[ channel ] = True

# ===========================================================================

@micropython.viper
def dma_channel_setup(
    channel: uint,
    start : uint,
    end: uint,
    buf_len: uint,
    control: uint
):
    base = uint( 0x50000000 ) + channel * uint( 0x40 )
    ptr32( base + 0x00 )[ 0 ] = start
    ptr32( base + 0x04 )[ 0 ] = end
    ptr32( base + 0x08 )[ 0 ] = buf_len
    ptr32( base + 0x0C )[ 0 ] = control
    
# ===========================================================================
#
# PIO
#
# ===========================================================================


    