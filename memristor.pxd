cdef class Memristor:
    cdef int ta_state
    cdef float init_memristor_state
    cdef int number_of_states
    cdef float vtn
    cdef float vtp

    cdef float mr_state

    # cdef void tune(self, float dir)
    # cdef float get_mr_state(self)
