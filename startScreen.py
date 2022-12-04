# Splash screen images: https://hello-tazzina.itch.io/greenwoods-ii
# Splash screen font: https://fonts2u.com/pixel-nes.font
# Splash screen implementation inspired by my previous work
# in Hack112. https://github.com/KyleleeSea/slashnbash

from cmu_112_graphics import *
from game import *

# Seperate file from other splash screens to avoid circular import
# in game.py
class StartScreen:
    def __init__(self, app):
        self.startImage = app.loadImage('./assets/newStartSplash.png')
    
    def redraw(self, app, canvas):
            canvas.create_image(app.width//2, app.height//2, 
            image=ImageTk.PhotoImage(self.startImage))

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