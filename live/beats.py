from pippi import dsp, tune
from hcj import drums, keys

midi = {'mpk': 5}

def play(ctl):
    mpk = ctl.get('midi').get('mpk')

    ccs = [ i + 48 for i in range(24) ]
    notes = []
    for cc in ccs:
        if mpk.get(cc) < 1:

            notes += [ cc ]

    ssnd = dsp.read('/home/hecanjog/sounds/drums/78sd.wav').data
    ssnd = dsp.read('jesssnare.wav').data
    hsnd = dsp.read('/home/hecanjog/sounds/drums/Shaker.wav').data
    ksnd = dsp.read('/home/hecanjog/sounds/drums/Drybd2.wav').data
    #ksnd = dsp.read('jesskick.wav').data

    beat = dsp.bpm2frames(90)
    #beat = dsp.mstf(290 * 2)
    length = beat * 4

    hat = 'xxx '
    kick =  'x       '
    snare =  '  x '
    #snare =  '  x  xx'
    #snare =  '    '

    def makeHat(length, i, amp):
        h = hsnd
        h = dsp.env(h, 'phasor')
        h = dsp.pad(h, 0, length - dsp.flen(h))

        return h

    def makeKick(length, i, amp):
        k = dsp.mix([ ksnd, drums.sinekick(length, i, amp) ])
        #k = dsp.env(ksnd, 'phasor')

        k = dsp.fill(k, length, silence=True)
        k = dsp.amp(k, 1)

        return k

    def makeSnare(length, i, amp):
        s = ssnd
        s = dsp.amp(s, 1.2)
        s = dsp.transpose(s, dsp.rand(1.5, 3))
        s = dsp.fill(s, length, silence=True)
        #ss = dsp.drift(s, dsp.rand(0.001, 0.1))
        #s = dsp.mix([s, ss])

        return s

    #hats = drums.parsebeat(hat, 16, beat, length, makeHat, 25)
    hats = drums.parsebeat(hat, 16, beat, length, makeHat, 0)
    kicks = drums.parsebeat(kick, 16, beat, length, makeKick, 0)
    snares = drums.parsebeat(snare, 8, beat, length, makeSnare, 0)

    out = dsp.mix([hats,kicks,snares])

    shuf = True
    shuf = False

    if shuf:
        out = dsp.split(out, beat)
        out = dsp.randshuffle(out)
        out = ''.join(out)

    out = dsp.amp(out, 2)

    cuts = True if dsp.rand() > 0.5 else False
    cuts = True
    #cuts = False

    if cuts:
        o = dsp.split(out, beat / 2)
        o = dsp.randshuffle(o)
        o = [ dsp.amp(oo, dsp.rand(0, 2.5)) for oo in o ]
        o = [ dsp.env(oo, 'random') for oo in o ]

        out = dsp.mix([ ''.join(o), out ])

    dsp.log(notes)


    synthy = False
    #synthy = True

    if synthy == True:
        s = ''
        for ii in range(dsp.flen(out) / (beat/2)):
            layers = []

            if len(notes) > 0:
                scale = [ n - 47 for n in notes ]
                scale = [1,5,8,12]
                scale = tune.fromdegrees(scale, octave=3, root='d')
                p = ''.join([ keys.pulsar(scale[ii % len(scale)], pulsewidth=dsp.rand(0.1, 1), amp=0.5, length=(beat/2) / 3) for _ in range(3) ])
                layers += [ p ]
            else:
                layers += [ dsp.pad('', beat / 2, 0) ]

            s += dsp.mix(layers)

        out = dsp.mix([ s, out ])

    #out = dsp.alias(out)

    #out = dsp.drift(out, dsp.rand(0.5, 2))

    return out
