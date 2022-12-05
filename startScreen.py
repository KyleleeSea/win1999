# Splash screen images: https://hello-tazzina.itch.io/greenwoods-ii
# Splash screen font: https://fonts2u.com/pixel-nes.font
# Splash screen implementation inspired by my previous work
# in Hack112. https://github.com/KyleleeSea/slashnbash

from cmu_112_graphics import *
from game import *
import decimal

# Seperate file from other splash screens to avoid circular import
# in game.py
class StartScreen:
    # https://github.com/KyleleeSea/slashnbash/blob/main/backdrop.py
    # by Evelynn Chen & Stephen Mao for hack112
    # evelynnc@andrew.cmu.edu stmao@andrew.cmu.edu
    # Helpers for moving backdrop
    #copied from 15-112 hw9
    def roundHalfUp(self, d):
        # Round to nearest with ties going away from zero.
        rounding = decimal.ROUND_HALF_UP
        # See other rounding options here:
        # https://docs.python.org/3/library/decimal.html#rounding-modes
        return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

    #!change n to change how fast the screen moves
    def rotateList(self, L, n=2):
        return L[n:] + L[0:n]

    def slicingBckg(self, app):
        self.bckgSlices = []
        
        for i in range(400):
            bckgSlice = self.bckgImage.crop((i*self.roundHalfUp(app.width
            /400), 0, (i+1)*self.roundHalfUp(app.width/400), app.height))
            self.bckgSlices.append(bckgSlice)

    def timerFired(self, app):
        self.bckgSlices = self.rotateList(self.bckgSlices)
        
    def __init__(self, app):
        self.bckgImage = app.loadImage('./assets/newStartSplash.png')
        self.bckgSlices = []
        self.slicingBckg(app)
    
    def redraw(self, app, canvas):
        for i in range(400):
            canvas.create_image(i*(self.roundHalfUp(app.width/400)), 0, 
            image=ImageTk.PhotoImage(self.bckgSlices[i]), anchor = 'nw')

            # canvas.create_image(app.width//2, app.height//2, 
            # image=ImageTk.PhotoImage(self.startImage))

    def mousePressed(self, app, event):
        wMargin = app.width//6
        hMargin = app.height//4
        (cX, cY) = app.width//2, app.height//2

        if event.x >= cX-wMargin and event.x <= cX+wMargin:
            if event.y >= cY-hMargin and event.y <= cY+hMargin:
                app.game = Game()
                app.game.startGame(app)
                app.mode = 'game'


    def keyPressed(self, app, event):
        if event.key == 'w':
            app.game = Game()
            app.game.startGame(app)
            app.mode = 'game'