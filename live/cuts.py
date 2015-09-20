from pippi import dsp

midi = {'mpk': 5, 'nk': 3}

def play(ctl):
    mpk = ctl.get('midi').get('mpk')
    nk = ctl.get('midi').get('nk')

    amp = mpk.get(4, low=0, high=1, default=0)

    kick = dsp.read('/home/hecanjog/sounds/drums/Junglebd.wav').data
    klength = dsp.mstf(mpk.get(1, low=60, high=1500, default=100))
    k = dsp.fill(kick, klength, silence=True)
    kamp = nk.get(0, low=0, high=1, default=1)
    k = dsp.amp(k, kamp)
    kpitch = nk.get(16, low=0.25, high=1, default=1)
    k = dsp.transpose(k, kpitch)

    snare = dsp.read('/home/hecanjog/sounds/drums/Hipclap1.wav').data
    slength = dsp.mstf(mpk.get(2, low=60, high=500, default=100))
    s = dsp.fill(snare, slength, silence=True)
    soffset = dsp.mstf(mpk.get(6, low=0, high=500, default=0))
    s = dsp.pad(s, soffset, 0)
    samp = nk.get(1, low=0, high=1, default=1)
    s = dsp.amp(s, samp)
    spitch = nk.get(17, low=0.25, high=2, default=1)
    s = dsp.transpose(s, spitch)

    hat = dsp.read('/home/hecanjog/sounds/drums/78ch.wav').data
    hlength = dsp.mstf(mpk.get(3, low=60, high=500, default=100))
    h = dsp.fill(hat, hlength, silence=True)
    hoffset = dsp.mstf(mpk.get(7, low=0, high=500, default=0))
    h = dsp.pad(h, hoffset, 0)
    hamp = nk.get(2, low=0, high=1, default=1)
    h = dsp.amp(h, hamp)
    hpitch = nk.get(18, low=0.25, high=2, default=1)
    h = dsp.transpose(h, hpitch)

    longest = max([ dsp.flen(k), dsp.flen(h), dsp.flen(s) ])

    k = dsp.fill(k, longest)
    h = dsp.fill(h, longest)
    s = dsp.fill(s, longest)

    out = dsp.mix([k, s, h])

    out = dsp.amp(out, amp)

    return out
