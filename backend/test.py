from Classes.Utilities import *

display = ""
for interface, ip in get_ips():
    display += f"{interface}: {ip}\n"
print(display)
