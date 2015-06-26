from pippi import dsp, tune
from hcj import snds, keys

def play(ctl):
    #out = snds.load('genie/piano.wav')

    lenrange = 300
    minlen = 1

    if dsp.rand() > 0.5:
        lengths = dsp.breakpoint([ dsp.rand(0, 1) for _ in range(5) ], 50)
    else:
        lengths = dsp.wavetable('sine', 50)

    lengths = [ dsp.mstf(l * lenrange + minlen) for l in lengths ]

    out = ''

    for length in lengths:
        freq = tune.ntf('f', octave=dsp.randint(2, 5))

        if dsp.rand() > 10.85:
            length = dsp.stf(dsp.rand(0.5, 3))
            freq = dsp.randchoose(tune.fromdegrees([1,3,4,5,6], octave=4, root='f'))

        out += keys.pulsar(freq=freq, length=length, env='phasor')

        if dsp.rand() > 10.75:
            freq = dsp.randchoose(tune.fromdegrees([1,3,4,5,6], octave=4, root='f'))

    return out
