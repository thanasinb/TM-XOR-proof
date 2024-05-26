cdef class Memristor:
    cdef int ta_state
    cdef float init_memristor_state
    cdef int number_of_states
    cdef float vtn
    cdef float vtp

    cdef float mr_state

    cdef float tune(self, float voltage, float dt)
    # cdef float get_mr_state(self)
