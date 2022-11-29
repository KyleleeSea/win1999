class PlayerShadow:
    def __init__(self, app):
        self.allVisited = []
        self.shadow = []

        # Timer logic
        # only change secondsToWait
        secondsToWaitAdd = 1
        msToWaitAdd = secondsToWaitAdd*1000
        self.AddIntervalsToWait = msToWaitAdd//app.timerDelay
        self.currentIntervalAdd = 0

        secondsToWaitRemove = 15
        msToWaitRemove = secondsToWaitRemove*1000
        self.RemoveIntervalsToWait = msToWaitRemove//app.timerDelay
        self.currentIntervalRemove = 0
    
    def addToVisited(self, cell):
        self.allVisited.append(cell)
    
    def timerFired(self, app):
        self.currentIntervalAdd += 1
        self.currentIntervalRemove += 1
        if self.currentIntervalAdd >= self.AddIntervalsToWait:
            self.currentIntervalAdd = 0
            # Check allVisited has cells 
            if len(self.allVisited) >= 3:
                for i in range(3):
                    self.shadow.append(self.allVisited.pop(0))
        
        if self.currentIntervalRemove >= self.RemoveIntervalsToWait:
            self.currentIntervalRemove = 0

            if len(self.shadow) >= 1:
                self.shadow.pop(0)