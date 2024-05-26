# cython: language_level=3
import numpy as np
cimport numpy as np

cdef class Memristor:
    def __init__(self, int ta_state, float init_memristor_state, int number_of_states, float vtn, float vtp):
        self.ta_state = ta_state
        self.init_memristor_state = init_memristor_state
        self.number_of_states = number_of_states
        self.vtn = vtn
        self.vtp = vtp

        self.mr_state = ta_state/self.number_of_states*self.init_memristor_state

    cdef float tune(self, float voltage, float dt):
        cdef float dx
        if voltage > self.vtp:
            dx = 1.0
        elif voltage < self.vtn:
            dx = -1.0

        self.mr_state += dx

        return self.mr_state

    def get_mr_state(self):
        return round(self.mr_state, 3)

    def get_ta_state(self):
        return int(self.mr_state*self.number_of_states/self.init_memristor_state)