import nxbt
from random import randint

closeGame = """
HOME 0.1s
0.5s
X 0.1s
0.5s
A 0.1s
"""

startGame = """
A 0.1s
2.0s
B 0.1s
"""

def randomColor():

    return [
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    ]

if __name__ == "__main__":
    # Start NXBT
    nx = nxbt.Nxbt()

    # Get list of all Bluetooth adapters
    print("Getting bluetooth adapters")
    adapters = nx.get_available_adapters()

    # Create Pro Controller instance
    print("Creating Pro Controller instance")
    if (len(nx.get_switch_addresses()) < 1):
        # No previous controller instance. Creating new ones
        print("Setting up for first time")
        index = nx.create_controller(
            nxbt.PRO_CONTROLLER,
            adapter_path=adapters[0],
            colour_body=randomColor(),
            colour_buttons=randomColor())
        # Wait for connection to controller instance
        print("Connecting...")
        nx.wait_for_connection(index)
        print("Connected")
    else:
        # Get previous controller instance
        print("Getting previous controller instance")
        index = nx.create_controller(
            nxbt.PRO_CONTROLLER,
            reconnect_address=nx.get_switch_addresses(),
            colour_body=randomColor(),
            colour_buttons=randomColor())
        # Wait for connection to last controller instance
        print("Connecting...")
        nx.wait_for_connection(index)
        print("Connected")

    # Start game macro
    nx.macro(index, startGame)