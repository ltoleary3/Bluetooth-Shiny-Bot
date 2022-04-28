import argparse, cv2, nxbt
from time import sleep
from tools import switchController, macros, frames, videostream


ap = argparse.ArgumentParser()
ap.add_argument('name', choices=[
                        'regice'
                    ],
                    help='''The name of the pokemon to hunt for. Currently available pokemon include:
                    regice''')
ap.add_argument('-u', '--update', required=False, default=False, type=bool,
                    help='''Signifies that an update for the game is available. Change how the game launches to prevent the game from updating''')
ap.add_argument("-d", "--display", required=False, default=False, type=bool,
    help="Whether or not video stream should be displayed")
args = ap.parse_args()


# Create nxbt controller instance
nx = nxbt.Nxbt()
controller = switchController.setupController(nx)
# Create input stream, change resolution if needed, and then start display
inStream = videostream.VideoStream().start()
nx.macro(controller, '5s\nHOME 0.25s\n0.1s')
# Get template to find in frame and create var to store valid frames
temp = cv2.imread('assets/{0}/{0}Appeared.jpg'.format(args.name), 0)
toStore = None
# Scale template image based on input stream resolution
frame = inStream.read()
wRatio = float(frame.shape[1])/1280
hRatio = float(frame.shape[0])/720
res = (int(temp.shape[1] * wRatio), int(temp.shape[0] * hRatio))
template = cv2.resize(temp, res, interpolation=cv2.INTER_AREA)

# Start game
print('Starting game...', end='\r')
if args.update:
    switchController.startMacro(controller, macros.startGameUpdate, nx)
else:
    switchController.startMacro(controller, macros.startGame, nx)
print('Game started. Now getting frame...', end='\r')

# Get valid Frame
while True:
    frame = inStream.read()
    if args.display:
        cv2.imshow('Preparing for the shiny hunt', frame)

    # Check if current frame is a valid image
    if frames.validFrame(frame, template):
        toStore = frame
    # Once there are no more valid images, save image
    elif toStore is not None:
        cv2.imshow('Is this {} shiny?'.format(args.name), toStore)
        resp = input('Is this Pokemon shiny? Please respond with [Y/n]')
        if resp.lower() == 'n':
            cv2.imwrite('assets/regice/regiceStandard.jpg', toStore)
            print('Standard version of {} saved. Now ready hunt for shinies!')
            break
        elif resp.lower() == 'y':
            print('Congrats! Stopping program...')
            exit()
        else:
            print('Response not understood. Stopping program...')
            exit()

# Close game
print('Closing game...', end='\r')
switchController.startMacro(controller, macros.closeGame, nx)

# Close windows and stop threads
inStream.stop()
cv2.destroyAllWindows()