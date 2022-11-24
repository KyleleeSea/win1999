import math

# https://wynnliam.github.io/raycaster/news/tutorial/2019/04/03/
# raycaster-part-02.html
# Note: I acknowledge I used the psuedocode given almost exactly, and
# do not expect to get credit for this individual file in terms of algorithmic
# complexity. I've included this purely for UI and UX purposes.
def getSpriteCoords(app):
    fov = 60
    hX = app.enemy.xPos - app.player.xPos
    hY = app.enemy.yPos - app.player.yPos
    p = math.atan2(-hY, hX) * (180/math.pi)
    
    if p > 360:
        p -= 360
    if p < 0:
        p += 360

    q = app.player.angle + (fov/2) - p
    # if (app.player.angle >= 90 and app.player.angle <= 180 and 
    # p >= 0 and p <= 90):
    #     q += 360
    # if (app.player.angle >= 0 and app.player.angle <= 90 and
    # p >= 90 and p <= 180):
    #     q -= 360
    
    returnX = q * (app.width / fov)
    returnY = app.height / 2
    return (returnX, returnY)