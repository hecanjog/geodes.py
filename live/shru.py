from pippi import dsp

midi = {'sh': 6 }

def automate(ctl):
    sh = ctl.get('midi').get('sh')
    i = ctl.get('iterations')
    
    sh.noteon(64)

    dsp.delay(dsp.mstf(dsp.rand(200, 500)))

    sh.noteoff(64)

    dsp.log(i)


