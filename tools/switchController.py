import nxbt
from nxbt import Nxbt, PRO_CONTROLLER
from time import sleep
from random import randint

def startMacro(controller, macroName):
    macro_id = Nxbt().macro(controller, macroName, block=False)
    while macro_id not in Nxbt().state[controller]['finished_macros']:
        state = Nxbt().state[controller]
        if state['state'] == 'crashed':
            print('An error occurred while running the macro:')
            print(state['errors'])
            exit()
        sleep(0.25)


def setupController():
    if (len(Nxbt().get_switch_addresses()) < 1):
        # No previous controller instance. Create new one
        input('Please navigate to the "Change Grip/Order" menu, then press Enter to continue...')
        controller = Nxbt().create_controller(
            nxbt.PRO_CONTROLLER,
            adapter_path=Nxbt().get_available_adapters()[0],
            colour_body=[randint(0, 255), randint(0, 255), randint(0, 255)],
            colour_buttons=[randint(0, 255), randint(0, 255), randint(0, 255)])
        # Wait for connection to controller instance
        Nxbt().wait_for_connection(controller)
        print('Controller connected')
        # Go to home menu
        Nxbt().macro(controller, 'B 0.1s\n0.1s')
        if Nxbt().state[controller]['state'] != 'connected':
            print('Controller disconnected leaving the controller menu. This is a known issue. Please restart...')
            exit()
        return controller
    else:
        # Get previous controller instance
        controller = Nxbt().create_controller(
            nxbt.PRO_CONTROLLER,
            reconnect_address=Nxbt().get_switch_addresses(),
            colour_body=[randint(0, 255), randint(0, 255), randint(0, 255)],
            colour_buttons=[randint(0, 255), randint(0, 255), randint(0, 255)])
        # Wait for connection to last controller instance
        Nxbt().wait_for_connection(controller)
        print('Controller connected')
        return controller
