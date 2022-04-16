import nxbt, argparse
from random import randint
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--updates', required=False, default=False, type=bool,
                    help="""Signifies that an update for the game is available. Will change how the game launches to prevent the game from updating""")
args = parser.parse_args()

closeGame = """
1.0s
HOME 0.25s
0.5s
X 0.25s
0.5s
A 0.25s
1.0s
"""

startGame = """
1.0s
A 0.25s
2.0s
B 0.25s
1.0s
"""

def randomColor():

    return [
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    ]

def startGame(update = False):
    nx.press_buttons(controller, [nxbt.Buttons.A], 0.25, 0.5)
    if update:
        nx.press_buttons(controller, [nxbt.Buttons.DPAD_UP], 0.25, 0.5)
        nx.press_buttons(controller, [nxbt.Buttons.A], 0.25, 10)
        nx.press_buttons(controller, [nxbt.Buttons.A], 0.25, 1)
        nx.press_buttons(controller, [nxbt.Buttons.A], 0.25, 0.5)
        #nx.press_buttons(controller, [nxbt.Buttons.DPAD_UP], 0.25, 0.5)
        #nx.press_buttons(controller, [nxbt.Buttons.A], 0.25, 0.5)

def closeGame():
    nx.press_buttons(controller, [nxbt.Buttons.HOME], 0.25, 0.5)
    nx.press_buttons(controller, [nxbt.Buttons.X], 0.25, 0.5)
    nx.press_buttons(controller, [nxbt.Buttons.A], 0.25, 0.5)


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
        input("Please navigate to the 'Change Grip/Order' menu, then press Enter to continue...")
        controller = nx.create_controller(
            nxbt.PRO_CONTROLLER,
            adapter_path=adapters[0],
            colour_body=randomColor(),
            colour_buttons=randomColor())
        # Wait for connection to controller instance
        print("Connecting...")
        nx.wait_for_connection(controller)
        print("Connected")
    else:
        # Get previous controller instance
        print("Getting previous controller instance")
        controller = nx.create_controller(
            nxbt.PRO_CONTROLLER,
            reconnect_address=nx.get_switch_addresses(),
            colour_body=randomColor(),
            colour_buttons=randomColor())
        # Wait for connection to last controller instance
        print("Connecting...")
        nx.wait_for_connection(controller)
        print("Connected")

    # Go to home menu
    nx.press_buttons(controller, [nxbt.Buttons.HOME], 0.25, 1)
    # Start game function
    if args.update:
        startGame(True)
    else:
        startGame()
    # Close game function
    closeGame()
    
    print("Macro finished. Removing controller")
    nx.remove_controller(controller)
    print("Controller removed")