import os
import subprocess

from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


def get_current_mac():
    """
    Get the MAC address of the Mac's en0 network interface.
    """

    try:
        result = subprocess.run(
            ["ifconfig", "en0"],
            capture_output=True,
            text=True,
            check=True
        )

        for line in result.stdout.splitlines():

            line = line.strip()

            if line.startswith("ether "):
                return line.split()[1].lower()

    except Exception as error:
        print(f"Could not get device MAC: {error}")

    return None


def is_registered_device():
    """
    Compare the current device MAC with the registered MAC.
    """

    current_mac = get_current_mac()

    registered_mac = os.getenv("DEVICE_MAC")

    if not current_mac:
        return False

    if not registered_mac:
        print("ERROR: DEVICE_MAC is not configured.")
        return False

    return current_mac == registered_mac.lower()