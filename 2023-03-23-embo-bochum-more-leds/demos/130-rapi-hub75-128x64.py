import godafoss as gf

d = gf.hub75(
    size = gf.xy( 128, 64 ),
    r1_b2 = 2,
    a_e = 10,
    clk_lat_oe = 26,
    frequency = 1_000_000
)

d.demo()

while True:
    for fg, bg in [
        [ gf.colors.white, gf.colors.black ],
        [ gf.colors.red, gf.colors.blue ]
    ]:
        for t in [
            "",
            "emBO++ 2023",
            "emBO++ 2023\nmore LEDs!",
        ]:
            d.clear( bg )
            d.write( t, ink = fg )
            d.flush()
            gf.sleep_us( 1_000_000 )

