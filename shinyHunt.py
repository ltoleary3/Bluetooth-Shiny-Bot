import nxbt, argparse
from random import randint
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--update', required=False, default=False, type=bool,
                    help="""Signifies that an update for the game is available. Will change how the game launches to prevent the game from updating""")
args = parser.parse_args()

def randomColor():

    return [
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    ]

def startMacro(controller, macroName):
    macro_id = nx.macro(controller, macroName, block=False)
    while macro_id not in nx.state[controller]["finished_macros"]:
        state = nx.state[controller]
        if state['state'] == 'crashed':
            print("An error occurred while running the demo:")
            print(state['errors'])
            exit(1)
        sleep(0.25)

startGameUpdate = """
5.0s
A 0.25s
0.5s
DPAD_UP 0.25s
0.5s
A 0.25s
25s
A 0.25s
0.5s
A 0.25s
0.5s
A 0.25s
0.5s
"""
startGame = """
5.0s
A 0.25s
25s
A 0.25s
0.5s
A 0.25s
0.5s
A 0.25s
0.5s
"""
closeGame = """
5.0s
HOME 0.25s
0.5s
X 0.25s
0.5s
A 0.25s
0.5s
"""

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
    nx.press_buttons(controller, [nxbt.Buttons.HOME], 0.25, 1, True)
    # Start game function
    print("Starting game...")
    if args.update:
        startMacro(controller, startGameUpdate)
    else:
        startMacro(controller, startGame)
    print("Started game. Now closing...")
    # Close game function
    startMacro(controller, closeGame)
    
    print("Closed game. Removing controller")
    nx.clear_macros(controller)
    nx.remove_controller(controller)
    print("Controller removed")