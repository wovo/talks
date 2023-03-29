import godafoss as gf
edge = gf.edge()

p = gf.ws281x( edge.p5, 64 ).folded( 8, zigzag = True ).xy_swapped()
          
while True:          
    for c in "emBO++":
        p.clear()                               
        p.write( gf.text( c ) )
        p.flush()
        gf.sleep_us( 500_000 )