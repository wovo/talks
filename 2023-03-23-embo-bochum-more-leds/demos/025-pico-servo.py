import godafoss as gf
edge = gf.edge()

green = gf.make_pin_out( edge.p0 )
red = gf.make_pin_out( edge.p1 )
yellow = gf.make_pin_out( edge.p2 )
blue = gf.make_pin_out( edge.p3 )
leds = red & green & blue & yellow
leds.write( 1 )

servo = gf.servo( edge.p4 )
last = gf.ticks_us()
visible = True
while True:
    now = gf.ticks_us()
    if now - last > 500_000:
        visible = not visible
        last = now    
    servo.write( gf.fraction( 100 if visible else 0, 100 ) ) 