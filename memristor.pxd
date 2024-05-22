cdef class Memristor:
    cdef float mr_state

    # def __init__(self, float mr_state)
    cdef float tune(self, float voltage, float dt)