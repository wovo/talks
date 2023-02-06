# ===========================================================================
#
# file     : gf_text.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the text class
#
# ===========================================================================

from godafoss.gf_xy import *
from godafoss.gf_shape import *
from godafoss.gf_font import *

             
# ===========================================================================
    
class text( shape ):    

    def __init__( 
        self, 
        text: str,  
        font: font = default_font()
    ):
        self._text = text
        self._font = font
        self.size = xy(
            sum( [ self._font.read( c ).size.x for c in text ] ),
            self._font.read( text[ 0 ] ).size.y
        )    
        shape.__init__( self )   
                    
    def write( 
        self, 
        sheet: "sheet",
        offset: xy = xy( 0, 0 ),
        ink: bool | color = True
    ):  
        x_offset_in_text = 0
        y_offset = 0
        for c in self._text:
        
            if c == '\n':
                x_offset_in_text = 0
                y_offset += self._font.size.y
                
                # quit when below the sheet
                if y_offset >= sheet.size.y:
                    return
                    
                continue
        
            glyph = self._font.read( c )
            x_offset_in_sheet = offset.x + x_offset_in_text
            
            # skip when beyond the right side of the sheet
            if (
                # skip when before the left side of the sheet
                ( x_offset_in_sheet + glyph.size.x >= 0 )
                
                # skip when beyond the right side of the sheet
                and ( x_offset_in_sheet < sheet.size.x )
            ):    
                glyph.write( 
                    sheet, 
                    offset + xy( x_offset_in_text, y_offset ),
                    ink
                )
                
            x_offset_in_text += glyph.size.x
            
            
# ===========================================================================
            