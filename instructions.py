# Splash screen image: https://ansimuz.itch.io/grunge-horror-environment
# Splash screen font: https://fonts2u.com/pixel-nes.font
# Splash screen implementation inspired by my previous work
# in Hack112. https://github.com/KyleleeSea/slashnbash
from cmu_112_graphics import *

class Instructions:
    def __init__(self, app):
        self.instructionImage = app.loadImage('./assets/instructions.png')
    
    def redraw(self, app, canvas):
            canvas.create_image(app.width//2, app.height//2, 
            image=ImageTk.PhotoImage(self.instructionImage))
        
    def keyPressed(self, app, event):
        if event.key == 'w':
            app.mode = 'start'