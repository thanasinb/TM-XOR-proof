# cython: language_level=3
import numpy as np
cimport numpy as np

cdef class Memristor:
    def __init__(self, float mr_state, float vtn, float vtp):
        self.mr_state = mr_state
        self.vtn = vtn
        self.vtp = vtp

    cdef float tune(self, float voltage, float dt):
        cdef float dx
        if voltage > self.vtp:
            dx = 1.0
        elif voltage < self.vtn:
            dx = -1.0

        self.mr_state += dx

        return self.mr_state

    cdef float get_mr_state(self):
        """
        Get the current state of the memristor.
        """
        return self.mr_state