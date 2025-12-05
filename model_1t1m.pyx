# cython: language_level=3

cdef class Model1T1M:
    def __init__(self,
                 int ta_state,
                 float init_memristor_state,
                 int number_of_states,
                 float alpha_off,
                 float alpha_on,
                 float v_off,
                 float v_on,
                 float r_off,
                 float r_on,
                 float k_off,
                 float k_on,
                 float d,
                 int clause,
                 int feature,
                 int negated,
				 float rt_off,
                 float rt_on):

        self.ta_state = ta_state
        self.init_memristor_state = init_memristor_state
        self.number_of_states = number_of_states
        self.alpha_off = alpha_off
        self.alpha_on = alpha_on
        self.v_off = v_off
        self.v_on = v_on
        self.r_off = r_off
        self.r_on = r_on
        self.k_off = k_off
        self.k_on = k_on
        self.d = d
        self.dx = 0
        self.rt_off = rt_off
        self.rt_on = rt_on
        self.delta_rm_off = 0
        self.delta_rm_2_off = 0
        self.delta_rm_on = 0
        self.delta_rm_2_on = 0

        self.mr_state = (ta_state/self.number_of_states)*self.init_memristor_state
        self.rm = (self.r_off * self.mr_state) + (self.r_on * (1 - self.mr_state))
        # self.x = self.mr_state * self.d

        self.delta_rm_1 = (r_off - r_on) / d

    def tune(self, float voltage, float dt):
        if voltage > self.v_off:
            self.delta_rm_3 = self.k_off * dt
            self.delta_rm_2_off = ((((self.rm * voltage) / (self.rm + self.rt_off)) / self.v_off) - 1) ** self.alpha_off
            self.delta_rm_off = self.delta_rm_1 * self.delta_rm_2_off * self.delta_rm_3
            self.rm += self.delta_rm_off
            self.dx = self.delta_rm_off

        elif voltage < self.v_on:
            voltage = -voltage
            self.delta_rm_3 = self.k_on * dt
            self.delta_rm_2_on = ((((self.rm * voltage) / (self.rm + self.rt_on)) / self.v_on) - 1) ** self.alpha_on
            self.delta_rm_on = self.delta_rm_1 * self.delta_rm_2_on * self.delta_rm_3
            self.rm -= self.delta_rm_on
            self.dx = self.delta_rm_on

        if self.rm > self.r_off:
            self.rm = self.r_off

        if self.rm < self.r_on:
            self.rm = self.r_on

        self.mr_state = (self.rm - self.r_on) / (self.r_off - self.r_on)
        self.ta_state = int(self.mr_state*self.number_of_states/self.init_memristor_state)

    def get_mr_value(self):
        return self.rm

    def get_mr_state(self):
        return self.mr_state

    def get_mr_xdx(self):
        return self.ta_state, self.mr_state, self.dx, self.rm

    def get_ta_state(self):
        return int(self.mr_state*self.number_of_states/self.init_memristor_state)