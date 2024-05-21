import cython

class Memristor:
    def __init__(self, mr_state):
        self.mr_state = mr_state

    def tune(self, dir, num):
        if dir == 1:
            self.mr_state = self.mr_state + num
        elif dir == -1:
            self.mr_state = self.mr_state - num

    def get_mr_state(self):
        return self.mr_state
