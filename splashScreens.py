# Splash screen images: https://hello-tazzina.itch.io/greenwoods-ii
# Splash screen font: https://fonts2u.com/pixel-nes.font
# Splash screen implementation inspired by my previous work
# in Hack112. https://github.com/KyleleeSea/slashnbash
# Death animation
# https://www.craiyon.com/?prompt=Bonzi%20Buddy%20VR%20horror%20game
# https://glitchyimage.com/
from cmu_112_graphics import *
import random

class Death:
    def __init__(self, app):
        self.deadImage = app.loadImage('./assets/newDeadScreen.png')
        self.counter = 0
        self.countTo = 13
        self.ind = random.randint(1,9)

        self.deathImages = []
        self.deathGlitchImages = []
        for i in range(1,10):
            self.deathImages.append(app.loadImage(f'./assets/death{i}.png'))
            self.deathGlitchImages.append(app.loadImage(
                f'./assets/death{i}glitch.png'))

    def timerFired(self, app):
        self.counter += 1

# Using % operations for this animation wouldn't work and returned a white
# screen
    def deathAnimation(self, app, canvas):
        if self.counter < 3:
            canvas.create_image(app.width//2, app.height//2, 
            image=ImageTk.PhotoImage(self.deathImages[self.ind]))

        if self.counter >= 3 and self.counter <= 7:
            canvas.create_image(app.width//2, app.height//2, 
            image=ImageTk.PhotoImage(self.deathGlitchImages[self.ind]))

            self.ind = random.randint(1,9)

        elif self.counter >= 7 and self.counter <= 10:
            canvas.create_image(app.width//2, app.height//2, 
            image=ImageTk.PhotoImage(self.deathImages[self.ind]))

        elif self.counter >= 10 and self.counter <= 13:
            canvas.create_image(app.width//2, app.height//2, 
            image=ImageTk.PhotoImage(self.deathGlitchImages[self.ind]))

            self.ind = random.randint(1,9)

    def redraw(self, app, canvas):
        self.deathAnimation(app, canvas)
        if self.counter >= self.countTo:
            canvas.create_image(app.width//2, app.height//2, 
            image=ImageTk.PhotoImage(self.deadImage))
        
    def mousePressed(self, app, event):
        if self.counter >= self.countTo:
            app.mode = 'start'
            
class Win:
    def __init__(self, app):
        self.winImage = app.loadImage('./assets/newWinScreen.png')
    
    def redraw(self, app, canvas):
            canvas.create_image(app.width//2, app.height//2, 
            image=ImageTk.PhotoImage(self.winImage))
        
    def keyPressed(self, app, event):
        if event.key == 's':
            app.mode = 'start'