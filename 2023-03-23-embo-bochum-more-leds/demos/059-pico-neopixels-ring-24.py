import godafoss as gf
edge = gf.edge()

# number of pixels:
# rings 8, 16, 24
# strip 56
# matrix 64

p = gf.ws281x( edge.p5, 24 )
                                
p.demo_color_wheel( dim = 24 )  