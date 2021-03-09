import mido
input_devices = mido.get_input_names()
output_devices = mido.get_output_names()

def printGreen(m):
    print("\033[1;32m{}\033[0m".format(m))

def printRed(m):
    print("\033[1;31m{}\033[0m".format(m))

def getDeluge(orOther="", device_type="output"):
    device = orOther or "deluge"
    return list(filter(lambda x: device in x.lower(), output_devices if device_type == "output" else input_devices))
