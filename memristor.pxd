cdef class Memristor:
    cdef float mr_state
    cdef float vtn
    cdef float vtp
    cdef float tune(self, float voltage, float dt)
    cdef float get_mr_state(self)
