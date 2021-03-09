import mido
import sys
from utils import printRed, printGreen

printGreen("Initializing")
input_devices = mido.get_input_names()
output_devices = mido.get_output_names()
output_devices = list(filter(lambda x: 'dtx' in x.lower(), output_devices))
if len(output_devices) == 0:
    printRed("Failed to found the dtx module")
    sys.exit(1) 

input_devices = list(filter(lambda x: 'deluge' in x.lower(), input_devices))
if len(input_devices) == 0:
    printRed("Failed to found the deluge module")
    sys.exit(1) 
try:
    with mido.open_output(output_devices[0]) as dtx:
        with mido.open_input(input_devices[0]) as deluge:
            printGreen("Ready to forward! In: {0} out: {1}".format(deluge.name, dtx.name))
            for msg in deluge:
                if "channel" in vars(msg) and msg.channel == 9 and "type" in vars(msg) and "note_" in msg.type:
                    printGreen("Message {} matches".format(msg))
                    dtx.send(msg)
                elif 'type' in vars(msg) and msg.type in ("program_change", "control_change"):
                    printGreen("Sending system command {}".format(msg))
                    dtx.send(msg)
except Exception as e:
    printRed("Exception! {}".format(e))
