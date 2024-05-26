cdef class Memristor:
    cdef int ta_state
    cdef float init_memristor_state
    cdef int number_of_states

    cdef float alpha_off
    cdef float alpha_on
    cdef float v_off
    cdef float v_on
    cdef float r_off
    cdef float r_on
    cdef float k_off
    cdef float k_on
    cdef float d

    cdef float mr_state
