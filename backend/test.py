from repositories.DataRepository import DataRepository
from Classes.OLEDDisplay import OLEDDisplay
from Classes.Encoder import Encoder
import json

current_course = 1

sequence = json.loads(DataRepository.get_sequence(current_course)["sequence"])["sequence"]
for i in sequence:
    print(i[-1])
