import godafoss as gf

display = gf.hub75(
    size = gf.xy( 64, 32 ),
    r1_b2 = 2,
    a_e = 10,
    clk_lat_oe = 26,
    frequency = 1_000_000
)#.folded( 2 )

if 0:
 d = display
 d.clear()
 d.write( gf.rectangle( gf.xy( -10, -10 ) ), gf.xy( 20, 20 ) )
 d.write( gf.rectangle( gf.xy( 10, 10 ) ), gf.xy( 30, 30 ) )
 d.flush()

if 1:
 display.demo()

if 0:
 for c in [ gf.colors.red, gf.colors.green, gf.colors.blue ]:
    print( c )
    display.clear( c ) 
    if 0:
     display.write(
        gf.rectangle( display.size - gf.xy( 10, 10 ), fill = True ),
        gf.xy( 5, 5 ),
        gf.colors.black
    )
    display.flush()
    gf.sleep_us( 1_000_000 )