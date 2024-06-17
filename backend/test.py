from repositories.DataRepository import DataRepository
from Classes.Utilities import *
from Classes.MCP3008 import MCP3008
from Classes.PCF8574 import PCF8574
from Classes.Button import Button
from Classes.Buzzer import Buzzer
from Classes.Encoder import Encoder
from Classes.OLEDDisplay import OLEDDisplay
from Classes.SevenSegmentDisplay import SevenSegmentDisplay
import json
import time


buzzer = Buzzer(12)

buzzer.beep(frequency=1000, duration=1)
