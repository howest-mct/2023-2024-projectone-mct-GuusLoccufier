import subprocess

def map_to(value, max_value=1023, map_value=100):
    """
    Maps a value from its original range to a new range [0, map_value].

    :param value: The value to map.
    :param max_value: The maximum value of the original range.
    :param map_value: The maximum value of the new range.
    :return: The mapped value.
    """
    return (value / max_value) * map_value

def map_to_ex(value, max_value=1023, min_map_value=0, max_map_value=100):
    """
    Maps a value from its original range to a new range [min_map_value, max_map_value].

    :param value: The value to map.
    :param max_value: The maximum value of the original range.
    :param min_map_value: The minimum value of the new range.
    :param max_map_value: The maximum value of the new range.
    :return: The mapped value.
    """
    return ((value / max_value) * (max_map_value - min_map_value)) + min_map_value

def get_ips():
    """
    Retrieves the IP addresses of the system.

    :return: A list of tuples containing interface names and their IP addresses.
    """
    try:
        output = subprocess.check_output(['ip', 'a', 'sh']).decode('utf-8')
        lines = output.split('\n')
        ip_addresses = []

        for line in lines:
            if 'inet ' in line and ' lo' not in line:
                parts = line.strip().split()
                interface_name = parts[-1]
                ip_address = parts[1].split('/')[0]
                ip_addresses.append((interface_name, ip_address))
        return ip_addresses
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while getting IP addresses: {e}")
        return []

def power_off():
    subprocess.run(["sudo", "poweroff"])

# Example usage
if __name__ == "__main__":
    print("Mapped value (map_to):", map_to(512))
    print("Mapped value (map_to_ex):", map_to_ex(512, max_value=1023, min_map_value=0, max_map_value=100))
    print("IP addresses:", get_ips())
