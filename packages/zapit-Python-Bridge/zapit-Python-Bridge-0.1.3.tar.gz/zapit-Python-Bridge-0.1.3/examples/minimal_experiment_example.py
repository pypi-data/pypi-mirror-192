"""
run_experiment

Instructions
1. EITHER:
    Set general.openPythonBridgeOnStart to 1 in Zapit's settings file
   OR:
    Run in MATLAB
     zapit.utils.openPythonBridge

2. Start Zapit in MATLAB: start_zapt

3. Load a stim config file and calibrate

4. At the system prompt: python minimal_experiment_example.py


Rob Campbell -- SWC 2023
"""

from time import sleep

import zapit_python_bridge.bridge as zpb


def run_experiment():
    # Create an instance of the bridge object
    hZP = zpb.bridge()
    num_cond = hZP.num_stim_cond()

    # Do not proceed if the user has yet to load a stimulus set into Zapit
    if num_cond == 0:
        print("No stim conditions found. Exiting.")
        return

    numTrials = 10
    currentTrial = 1

    while currentTrial <= numTrials:
        # Send stimuli and do not log because this an example.
        # In a real experiment you likely want to enable both logging
        # and hardware triggering.
        print("Presenting stimulus %d/%d" % (currentTrial, numTrials))
        hZP.send_samples(
            conditionNum=-1, hardwareTriggered=False, logging=False
        )

        sleep(0.5)

        hZP.stop_opto_stim()

        sleep(
            0.3
        )  # This delay is necessary because there is a non-blocking delay
        # of 300 ms before the task is Stopped by zapit.pointer.stopOptoStim
        # It is possible in the future that we no longer stop the task at this
        # stage and so the need for the minimal delay will go away. In practice
        # this delay is likely a non-issue but see:
        # https://github.com/Zapit-Optostim/zapit/issues/102

        currentTrial += 1


if __name__ == "__main__":
    run_experiment()
