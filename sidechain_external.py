# The assumption is that if you run this, you *want* ducking to occur
import mido
from utils import * # kill me

delugeIn = getDeluge(device_type="input")
minilougeOut = getDeluge(orOther="minilogue xd", device_type="output")

loud = 127 # I'm fairly sure we can read this from the current state of an input device
quiet = 0 # perhaps we could set this to another value
filter_cutoff_cc = 74

with mido.open_input(delugeIn[0]), mido.open_output(minilougeOut[0]) as deluge, minilouge:
    printGreen("Got the deluge, will redirect cc16 over to volume on channel 10")
    for msg in deluge:
        if 'type' in vars(msg) and msg.type in ('control_change'):
            if msg.control == 16:
                loud = msg.value
            elif msg.control == 17:
                quiet = msg.value
             
           minilouge.send(msg)
           printGreen("minilouge.send({})".format(msg))
        elif "channel" in vars(msg) and msg.channel == 11 and "type" in vars(msg) and "note_" in msg.type:
           additional_message = mido.Message(
               "control_change", 
               control=filter_cutoff_cc,
               value=loud if msg.type == "note_on" else quiet,
               channel=msg.channel
           )
           minilouge.send(additional_message)
           printGreen("minilouge.send({})".format(additional_message))
           minilouge.send(msg)
           printGreen("minilouge.send({})".format(msg))
