from pippi import dsp, tune
from hcj import keys

def play(ctl):
    freqs = tune.fromdegrees([1,3,6,8,9], octave=4, root='a')
    freq = dsp.randchoose(freqs)
    length = dsp.stf(dsp.rand(3, 5))
    out = keys.rhodes(length, freq)

    return out
