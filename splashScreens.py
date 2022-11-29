# Splash screen images: https://ansimuz.itch.io/grunge-horror-environment
# https://www.deviantart.com/thenoahguy1/art/Bonzi-spritesheet-440805977
# https://www.clipartmax.com/middle/m2i8A0H7b1m2K9Z5_tombstone-tombstone-
# pixel-art/
# Splash screen font: https://fonts2u.com/pixel-nes.font
# Splash screen implementation inspired by my previous work
# in Hack112. https://github.com/KyleleeSea/slashnbash

from cmu_112_graphics import *

class Death:
    def __init__(self, app):
        self.deathImage = app.loadImage('./assets/death.png')
    
    def redraw(self, app, canvas):
            canvas.create_image(app.width//2, app.height//2, 
            image=ImageTk.PhotoImage(self.deathImage))
        
    def keyPressed(self, app, event):
        if event.key == 'f':
            app.mode = 'start'

class Instructions:
    def __init__(self, app):
        self.instructionImage = app.loadImage('./assets/instructions.png')
    
    def redraw(self, app, canvas):
            canvas.create_image(app.width//2, app.height//2, 
            image=ImageTk.PhotoImage(self.instructionImage))
        
    def keyPressed(self, app, event):
        if event.key == 'w':
            app.mode = 'start'

class Win:
    def __init__(self, app):
        self.winImage = app.loadImage('./assets/win.png')
    
    def redraw(self, app, canvas):
            canvas.create_image(app.width//2, app.height//2, 
            image=ImageTk.PhotoImage(self.winImage))
        
    def keyPressed(self, app, event):
        if event.key == 's':
            app.mode = 'start'