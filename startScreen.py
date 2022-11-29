# Splash screen images: https://ansimuz.itch.io/grunge-horror-environment
# Splash screen font: https://fonts2u.com/pixel-nes.font
# Splash screen implementation inspired by my previous work
# in Hack112. https://github.com/KyleleeSea/slashnbash

from cmu_112_graphics import *
from game import *

# Seperate file from other splash screens to avoid circular import
# in game.py
class StartScreen:
    def __init__(self, app):
        self.startImage = app.loadImage('./assets/startScreen.png')
    
    def redraw(self, app, canvas):
            canvas.create_image(app.width//2, app.height//2, 
            image=ImageTk.PhotoImage(self.startImage))
        
    def keyPressed(self, app, event):
        if event.key == 'w':
            app.game = Game()
            app.game.startGame(app)
            app.mode = 'game'
        if event.key == 's':
            app.instructions = Instructions(app)
            app.mode = 'instructions'