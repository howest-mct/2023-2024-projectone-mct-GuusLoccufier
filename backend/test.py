from repositories.DataRepository import DataRepository
from Classes.OLEDDisplay import OLEDDisplay
from Classes.Encoder import Encoder
from Classes.PCF8574 import PCF8574
import json
import time

PCF = PCF8574(0x20)
current_course = 1

sequence = json.loads(DataRepository.get_sequence(current_course)["sequence"])["sequence"]
for i in sequence:
    if i[-1] in [str(i) for i in range(1, 9)]:
        byte = 1 << int(i[-1])
        byte = ~byte & 0xFF
        PCF.write_byte(byte)
        print(bin(byte))
    else:
        PCF.write_byte(0b11111111)
        print("reload")
    time.sleep(2)
PCF.write_byte(0b11111111)
print("done")
