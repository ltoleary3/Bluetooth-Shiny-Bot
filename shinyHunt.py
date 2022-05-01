import argparse, cv2, nxbt, os
from time import sleep, time
from threading import Thread
from tools import pokemon, switchController, macros, frames, videostream


ap = argparse.ArgumentParser()
ap.add_argument('name', choices=[
                        'regice'
                    ], type=str.lower,
                    help='''The name of the pokemon to hunt for. Currently available pokemon include:
                    regice''')
ap.add_argument('-u', '--update', required=False, default=False, type=bool,
                    help='''Signifies that an update for the game is available. Change how the game launches to prevent the game from updating''')
ap.add_argument("-d", "--display", required=False, default=False, type=bool,
    help="Whether or not video stream should be displayed")
ap.add_argument("-r", "--restart", required=False, default=False, type=bool,
    help="Used to start the program when the game is already open. It will first close the game, then restart it again to begin searching")
args = ap.parse_args()


def useController():
    # If no shiny found, keep looping
    while not mon.isShiny:
        # Start game
        print('Starting game...', end='\r')
        if args.update:
            switchController.startMacro(controller, macros.startGameUpdate, nx)
        else:
            switchController.startMacro(controller, macros.startGame, nx)
        print('Game started. Now checking for shiny...', end='\r')
        mon.startBattle()
        mon.attempt()

        # While battling, wait
        while mon.battling:
            sleep(1)

        # If pokemon not shiny, close game
        if not mon.isShiny:
            print('Closing game...', end='\r')
            switchController.startMacro(controller, macros.closeGame, nx)


# Check if Standard image exists or not
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'assets/{0}/{0}Standard.jpg'.format(args.name))):
    # Set file path
    command = 'sudo python3 prepHunt.py {}'.format(args.name)
    if args.update:
        command = command + ' -update'
    if args.display:
        command = command + ' -display'
    # Call script to setup the shiny hunt
    os.system(command)

# Create pokemon object
mon = pokemon.pokemon(name=args.name)
# Create nxbt controller instance
nx = nxbt.Nxbt()
controller = switchController.setupController(nx)
# Create input stream and then start display
inStream = videostream.VideoStream().start()
# For some reason the first macro to run doesnt send a signal to the Switch for a few seconds. Because of this we run a simple macro that waits 5 seconds to press the home button which shouldnt affect any functionality
nx.macro(controller, '5s\nHOME 0.25s\n0.25s')
# Check if game needs to be restarted
if args.restart:
    print('Restarting game...', end='\r')
    switchController.startMacro(controller, macros.closeGame, nx)
control = Thread(target=useController, args=()).start()
# Scale template image based on input stream resolution
mon.scaleTemplate(inStream.frame)

# Main shiny hunt loop
while True:
    # Get frame from the threaded video stream and resize it
    frame = inStream.read()

    # If display flag provided, show frame
    if args.display:
        cv2.imshow('Stream', frame)

    # While in battle, check shiny status
    if mon.battling:
        # Check if current frame can be used to check for shiny status
        if frames.validFrame(frame, mon.template):
            # Convert valid frame to .jpg and signal that a valid frame has been found
            frame = frames.convertToJPG(frame)
            inStream.foundValidFrame(frame)
        # If there are no more valid frames, use the last one found
        elif inStream.validFrameFound:
            # Compate the difference between the last valid frame and a reference image of a standard version (low difference = less likely to be shiny)
            val = frames.compareFrames(inStream.validFrame, mon.standardImg)
            # If the difference between standard version and the current version is greater than threshold, have user check if pokemon is shiny
            if val >= 0.50:
                resp = input('Is this Pokemon shiny? Please respond with [Y/n]')
                if resp.lower() == "y":
                    print('Congrats on your shiny {0}!! You found it after {1} tries this session. Closing program...'.format(mon.name, mon.attempts))
                    mon.shiny()
                    break
                elif resp.lower() == "n":
                    print('Sorry. If false positives happen too many times, you can increase the threshold found on line 73. NOTE: Increasing the threshold could cause you to miss a shiny, so only small increases are recommended if at all')
                    print('Resuming shiny hunt...')
                    mon.stopBattle()
                    inStream.resetValidFrame()
                else:
                    print('Input not understood. Closing program to prevent potential missed shiny...')
                    mon.shiny() # Set shiny so controller thread can close
                    break
            # Difference between images too small to be shiny, reset
            else:
                print('Not Shiny...                           ', end='\r')
                mon.stopBattle()
                inStream.resetValidFrame()
        # Check if designated amount of time has passed without finding a valid frame
        elif (time()-mon.battleStartTime) > 300:
            print('Valid image could not be found for over 5 mins. Closing program to prevent potential missed shiny...')
            mon.shiny() # Set shiny so controller thread can close
            break

    # Press 'Q' to stop search
    if cv2.waitKey(1) == ord('q'):
        mon.shiny() # Set shiny so controller thread can close
        break

# Close windows and stop threads
inStream.stop()
control.join()
cv2.destroyAllWindows()