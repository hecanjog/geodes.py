from pippi import dsp

main = dsp.read('base_loop.wav').data
synth = dsp.read('synthloop.wav').data
beat = dsp.flen(main) / 128

freq = 430
s = dsp.pine(synth, dsp.flen(main) * 8, freq)
s = dsp.split(s, beat)
s = dsp.randshuffle(s)
s = [ dsp.alias(ss) for ss in s ]
s = [ dsp.amp(ss, dsp.rand(0.5, 2)) for ss in s ]
s = [ dsp.pan(ss, dsp.rand(0, 1)) for ss in s ]
s = ''.join(s)
s = dsp.fill(s, dsp.flen(synth))

s2 = dsp.split(synth, beat)
s2 = dsp.randshuffle(s2)
s2 = [ dsp.transpose(ss, dsp.randchoose([1,2,4])) for ss in s2 ]
s2 = [ dsp.fill(ss, beat) for ss in s2 ]
s2 = [ dsp.env(ss, 'phasor') for ss in s2 ]
s2 = ''.join(s2)

synth = dsp.mix([ s, s2 ])
synth = dsp.fill(synth, dsp.flen(main))

#synth = dsp.fill(synth, dsp.flen(main))

out = dsp.mix([ main, synth ])
#out = synth

dsp.write(out, 'newloop')
