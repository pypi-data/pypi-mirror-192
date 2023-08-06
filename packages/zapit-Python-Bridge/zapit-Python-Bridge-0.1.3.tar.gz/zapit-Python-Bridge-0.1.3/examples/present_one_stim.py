from time import sleep

import zapit_python_bridge.bridge as zpb

hZP = zpb.bridge()


hZP.send_samples(conditionNum=-1, hardwareTriggered=False)
sleep(0.75)
hZP.stop_opto_stim()
sleep(0.5)
