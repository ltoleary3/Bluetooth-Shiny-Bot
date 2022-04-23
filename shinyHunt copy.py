import numpy as np
import nxbt, argparse, cv2, threading
from random import randint
from time import sleep, time


parser = argparse.ArgumentParser()
parser.add_argument('name', choices=[
                        'regice'
                    ],
                    help='''The name of the pokemon to hunt for. Currently available pokemon include:
                    regice''')
parser.add_argument('-u', '--update', required=False, default=False, type=bool,
                    help='''Signifies that an update for the game is available. Change how the game launches to prevent the game from updating''')
parser.add_argument('-o', '--output', required=False, default=False, type=bool,
                    help='''Enables a display of the video stream as its read''')
args = parser.parse_args()


def startMacro(controller, macroName):
    macro_id = nx.macro(controller, macroName, block=False)
    while macro_id not in nx.state[controller]['finished_macros']:
        state = nx.state[controller]
        if state['state'] == 'crashed':
            print('An error occurred while running the macro:')
            print(state['errors'])
            exit()
        sleep(0.25)

def useController():
    # As long as pokemon is not shiny, keep looping
    while not shiny:
        # Start game
        print('Starting game...', end='\r')
        if args.update:
            startMacro(controller, startGameUpdate)
        else:
            startMacro(controller, startGame)
        print('Game started. Now checking for shiny...', end='\r')
        checkShiny = True
        loopTime = time()

        # Wait for shiny check
        while checkShiny and not shiny:
            sleep(1)

        # If not shiny, close game
        if not shiny:
            print('Closing game...', end='\r')
            startMacro(controller, closeGame)
            print('Game closed...', end='\r')

def validFrame(rgbImage, template):
    grayFrame = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2GRAY)

    # Match template image to frame
    result = cv2.matchTemplate(grayFrame, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        return True
    return False

def compareFrames(toCompare):
    # Convert to HSV
    standardHSV = cv2.cvtColor(standardImg, cv2.COLOR_BGR2HSV)
    compHSV = cv2.cvtColor(toCompare, cv2.COLOR_BGR2HSV)

    # Generate histograms and normalize
    standardHist = cv2.calcHist([standardHSV], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(standardHist, standardHist).flatten()
    compHist = cv2.calcHist([compHSV], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(compHist, compHist).flatten()

    # Return metric val
    return cv2.compareHist(standardHist, compHist, cv2.HISTCMP_CHISQR)


startGameUpdate = '''
1.0s
A 0.25s
0.5s
DPAD_UP 0.25s
0.25s
A 0.25s
25s
A 0.25s
1s
A 0.25s
1s
A 0.25s
15s
A 0.25s
0.5s
A 0.25s
'''
startGame = '''
1.0s
A 0.25s
25s
A 0.25s
1s
A 0.25s
1s
A 0.25s
15s
A 0.25s
0.5s
A 0.25s
'''
closeGame = '''
1.0s
HOME 0.25s
1.0s
X 0.25s
0.5s
A 0.25s
0.5s
'''


if __name__ == '__main__':

    # Set vars
    pokemon = args.name
    checkShiny = False
    shiny = False
    template = cv2.imread('assets/{0}/{0}Appeared.jpg'.format(pokemon), 0)
    standardImg = cv2.imread('assets/{0}/{0}Standard.jpg'.format(pokemon))
    h,w,c = standardImg.shape
    toCompare = None
    counter = 0
    loopTime = 0

    # Start NXBT
    nx = nxbt.Nxbt()    
    # Get list of all Bluetooth adapters
    adapters = nx.get_available_adapters()
    if (len(nx.get_switch_addresses()) < 1):
        # No previous controller instance. Create new one
        print('Setting up for first time...')
        input('Please navigate to the "Change Grip/Order" menu, then press Enter to continue...', end='\r')
        controller = nx.create_controller(
            nxbt.PRO_CONTROLLER,
            adapter_path=adapters[0],
            colour_body=[randint(0, 255), randint(0, 255), randint(0, 255)],
            colour_buttons=[randint(0, 255), randint(0, 255), randint(0, 255)])
        # Wait for connection to controller instance
        print('Connecting...'),
        nx.wait_for_connection(controller)
        print('Connected')
        # Go to home menu
        nx.macro(controller, "B 0.1s\n0.1s")
        if nx.state[controller]['state'] != 'connected':
            print('Controller disconnected leaving the controller menu. This is a known issue. Please restart...')
            exit()
    else:
        # Get previous controller instance
        print('Getting previous controller instance')
        controller = nx.create_controller(
            nxbt.PRO_CONTROLLER,
            reconnect_address=nx.get_switch_addresses(),
            colour_body=[randint(0, 255), randint(0, 255), randint(0, 255)],
            colour_buttons=[randint(0, 255), randint(0, 255), randint(0, 255)])
        # Wait for connection to last controller instance
        print('Connecting...'),
        nx.wait_for_connection(controller)
        print('Connected')
    
    # Start video capture (this reserves the video capture device)
    print('Starting video capture...'),
    vidCap = cv2.VideoCapture(0)
    if (vidCap.isOpened() == False):
        print('Error opening video stream. Please ensure the correct video capture device is being used')
        exit()
    print('Video capture stream opened')

    vidCap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    vidCap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    print('w: {0}\nh: {1}'.format(vidCap.get(cv2.CAP_PROP_FRAME_WIDTH), vidCap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # Create controller thread and start it
    controllerThread = threading.Thread(target=useController)
    controllerThread.start()

    # Loop through frames
    while True:
        ret, frame = vidCap.read()
        if not ret: break

        # Display Frame if output flag given
        if args.output:
            cv2.imshow('Video Stream', frame)

        if checkShiny:
            # Check if frame can be used to determine shiny status
            if validFrame(frame, template):
                # Have to convert frame to be jpg image to accurately compare
                toCompare = cv2.imdecode(cv2.imencode('.jpg', frame)[1], cv2.IMREAD_UNCHANGED)
            elif toCompare is not None:
                val = compareFrames(toCompare)
                counter+=1
                #  Choosing 0.25 to differentiate based on testing (mock shiny returning value over 1.00 while testing frames were lower than 0.10). This can be adjusted down to make it more likely to find shiny or up to make it more strict if its reporting too much
                if val >= 0.25:
                    resp = input('Shiny?! Please type "y" if it is shiny or "n" if it is not...', end='\r')
                    if resp.lower() == "y":
                        print('Congrats on your shiny {0}!! You found it after {1} tries this session. Closing program...'.format(pokemon, counter))
                        shiny = True
                        controllerThread.join()
                        break
                    elif resp.lower() == "n":
                        print('Resuming shiny hunt...', end='\r')
                        checkShiny = False
                        toCompare = None
                    else:
                        print('Input not understood, closing program...')
                        # Shiny set to true to break out of controller thread loop
                        shiny = True
                        controllerThread.join()
                        break
                else:
                    print('Not Shiny pepeHands...', end='\r')
                    checkShiny = False
                    toCompare = None
            
            # If no valid images found for over 5 mins then close
            if (time()-loopTime) > 300:
                print('Could not find a valid image to use when checking for shiny status for over 5 minutes. Closing Program...')
                # Shiny set to true to break out of controller thread loop
                shiny = True
                controllerThread.join()
                break
        
        # Esc key closes program
        if cv2.waitKey(1) == 27:
            break
    
    vidCap.release()
    cv2.destroyAllWindows()