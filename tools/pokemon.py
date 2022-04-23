import cv2, time, os

class pokemon:
    def __init__(self, name):
        self.name = name
        self.isShiny = False
        self.battling = False
        self.battleStartTime = 0
        self.attempts = 0
        self.template = cv2.imread(os.path.join(os.path.dirname(__file__), '..', 'assets/{0}/{0}Appeared.jpg'.format(self.name)), 0)
        self.standardImg = cv2.imread(os.path.join(os.path.dirname(__file__), '..', 'assets/{0}/{0}Standard.jpg'.format(self.name)))
    
    def shiny(self):
        self.isShiny = True
        self.stopBattle()

    def startBattle(self):
        self.battling = True
        self.battleStartTime = time.time()

    def stopBattle(self):
        self.battling = False
    
    def attempt(self):
        self.attempts += 1