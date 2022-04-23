from nxbt import PRO_CONTROLLER
from time import sleep
from random import randint

def startMacro(controller, macroName, nx):
    macro_id = nx.macro(controller, macroName, block=False)
    while macro_id not in nx.state[controller]['finished_macros']:
        state = nx.state[controller]
        if state['state'] == 'crashed':
            print('An error occurred while running the macro:')
            print(state['errors'])
            exit()
        sleep(0.25)

def createNewController(nx):
    input('Please navigate to the "Change Grip/Order" menu, then press Enter to continue...')
    controller = nx.create_controller(
        PRO_CONTROLLER,
        adapter_path=nx.get_available_adapters()[0],
        colour_body=[randint(0, 255), randint(0, 255), randint(0, 255)],
        colour_buttons=[randint(0, 255), randint(0, 255), randint(0, 255)])
    # Wait for connection to controller instance
    nx.wait_for_connection(controller)
    print('Controller connected')
    # Go to home menu
    nx.macro(controller, 'B 0.1s\n0.1s')
    if nx.state[controller]['state'] != 'connected':
        print('Controller disconnected leaving the controller menu. This is a known issue. Please restart...')
        exit()
    return controller

def reconnectController(nx):
    controller = nx.create_controller(
        PRO_CONTROLLER,
        reconnect_address=nx.get_switch_addresses(),
        colour_body=[randint(0, 255), randint(0, 255), randint(0, 255)],
        colour_buttons=[randint(0, 255), randint(0, 255), randint(0, 255)])
    # Wait for connection to last controller instance
    nx.wait_for_connection(controller)
    print('Controller connected')
    return controller


def setupController(nx):
    if (len(nx.get_switch_addresses()) < 1):
        # No previous controller instance. Create new one
        return createNewController(nx)
    else:
        # Get previous controller instance
        return reconnectController(nx)
