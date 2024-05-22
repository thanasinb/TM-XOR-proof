# cython: language_level=3

cdef class Memristor:
    def __init__(self, float mr_state):
        self.mr_state = mr_state

    cdef float tune(self, float voltage, float dt):
        cdef float dx
        if voltage > 0:
            dx = 1.0
        elif voltage < 0:
            dx = -1.0

        self.mr_state += dx

        return self.mr_state
