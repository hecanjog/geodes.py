from pippi import dsp, tune
from hcj import drums, keys

def play(ctl):
    mpk = ctl.get('midi').get('mpk')

    ssnd = dsp.read('/home/hecanjog/sounds/drums/78sd.wav').data
    lssnd = dsp.read('jesssnare.wav').data
    hsnd = dsp.read('/home/hecanjog/sounds/drums/78ch.wav').data
    ohsnd = dsp.read('/home/hecanjog/sounds/drums/78oh.wav').data
    ksnd = dsp.read('jesskick.wav').data

    beat = dsp.bpm2frames(166)
    length = beat * 8

    if dsp.rand() > 0.5:
        kick =   'x--x-x-x--------'
    else:
        kick =   'x----x----------'

    hat =    'x-x-x-x-xx-x-x-x'
    ohat =   'x------x--------'
    lsnare = '---------x--x---'

    if dsp.rand() > 0.5:
        lsnare = '---------x--x---'
    else:
        lsnare = '--x--x--x--x--x-'

    snare =  '--x--x--x--x--x-'

    def makeOHat(length, i, amp):
        return dsp.fill(hsnd, length, silence=True)

    def makeHat(length, i, amp):
        return dsp.fill(ohsnd, length, silence=True)

    def makeKick(length, i, amp):
        k = dsp.fill(ksnd, length, silence=True)
        return dsp.amp(k, 3)

    def makeSnare(length, i, amp):
        s = dsp.fill(ssnd, length, silence=True)
        return dsp.amp(s, 2)

    def makeLSnare(length, i, amp):
        s = dsp.fill(lssnd, length, silence=True)
        return dsp.amp(s, 1)

    hats = drums.parsebeat(hat, 8, beat, length, makeHat, 5)
    ohats = drums.parsebeat(ohat, 8, beat, length, makeOHat, 0)
    kicks = drums.parsebeat(kick, 8, beat, length, makeKick, 0)
    snares = drums.parsebeat(snare, 8, beat, length, makeSnare, 0)
    lsnares = drums.parsebeat(lsnare, 8, beat, length, makeLSnare, 0)

    snaresnstuff = dsp.mix([ohats,snares])
    snaresnstuff= dsp.split(snaresnstuff, dsp.flen(snaresnstuff) / 32)
    snaresnstuff = dsp.randshuffle(snaresnstuff)
    snaresnstuff = ''.join(snaresnstuff)
    snaresnstuff = dsp.amp(snaresnstuff, 0.35)

    out = dsp.mix([kicks,lsnares,snares,hats,ohats,snaresnstuff])

    return out
