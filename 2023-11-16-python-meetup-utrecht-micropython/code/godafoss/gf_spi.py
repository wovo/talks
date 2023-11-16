import machine

class spi:
    """
    Serial Peripheral Interface bus
    """
    
    soft = const ( 0 )
    hard = const ( 1 )
    
    def __init__(
        self,
        sck: int,
        mosi: int,
        miso: int,
        frequency: int = 10_000_000,
        polarity: int = 1,
        phase: int = 1,
        mechanism: int = 1,
        id: int = None
    ):
        self.baudrate = frequency
        self.polarity = polarity
        self.phase = phase
        self.mechanism = mechanism
        self.sck = sck
        self.mosi = mosi
        self.miso = miso
         
        if self.mechanism == self.soft:
                
            self.bus = machine.SoftSPI( 
                baudrate = frequency,
                polarity = polarity,
                phase = phase,
                sck = machine.Pin( self.sck ),
                mosi = machine.Pin( self.mosi ),
                miso = machine.Pin( self.miso )
            )
                
        elif self.mechanism == self.hard:
            
            if id is None:
            
                import os
                uname = os.uname()[ 0 ]
                
                if uname == "rp2":
                    id = 0
                    
                elif uname == "mimxrt":
                    self.bus = machine.SPI(
                        1,
                        baudrate = frequency,
                        polarity = polarity,
                        phase = phase
                    )
                    return
                
                else:
                    ValueError( "unknown system (%s), specify the id" % uname )
                
            self.bus = machine.SPI(
                id,
                frequency,
                polarity = polarity,
                phase = phase,
                sck = machine.Pin( self.sck ),
                mosi = machine.Pin( self.mosi ),
                miso = machine.Pin( self.miso )
            )
                
        else:
            raise ValueError( "unknown mechanism %d" % self.mechanism )
        
    def write( self, *args, **kwargs ):
        self.bus.write( *args, **kwargs )
