

class Ui:
    score = 0
    def __init__(self):
        self._score = 0

    def AddScore(self, x):
        self._score += x
        print("x:", x)
        print("score: "+ str(self._score))
        #return(self._score)


