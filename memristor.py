# memristor paramitor
# init_state = 1
# alpha_off = 1
# alpha_on = 1
# k_off = 11.27
# k_on = -0.00574
# v_off = 0.09
# v_on = -0.15
# r_off = 150000
# r_on = 1400
# state1 = 0
# state2 = 0
# rm = 0

class memristor_paramitor:

    def __init__(self, state, v_off, v_on, k_off,k_on, alpha_off, alpha_on, r_off, r_on, D_nm):
        self.state = state
        self.v_off = v_off
        self.v_on = v_on
        self.k_off = k_off
        self.k_on = k_on
        self.alpha_off = alpha_off
        self.alpha_on = alpha_on
        self.r_off = r_off
        self.r_on = r_on
        self.D_nm = D_nm
        self.rm = 0

    # def memristor(self, memristor_no, state):
    #     voff = memristor_no
    #     von = state

    def tune(self, vt, dt):
        if(vt > self.v_off and vt > 0):
            # self.state = self.state + (self.k_off * pow(((vt/self.v_off)-1), self.alpha_off)) * dt
            self.state += 1
            # self.state = 1

        if (vt < self.v_on and vt < 0):
            # self.state = self.state + (self.k_on * pow(((vt/self.v_on)-1), self.alpha_on)) * dt
            self.state -= 1
            # self.state = -1
            print(f"vt = {vt} ")
            print(f"self.state vt < 0 = {self.state} \n")

        # return self.state

        # if (vt < self.v_off and vt > self.v_on):
        #     self.state = 0

    # def read(self):
    #     return self.state, self.rm

    def getState(self):
        return self.state

    def getRm(self):
        s = self.state/self.D_nm
        self.rm = self.r_on + self.r_off * (1 - s)
        return self.rm



mem = memristor_paramitor(state=0, v_off=0.09, v_on=-0.15, k_off=11.27,k_on=-0.00574, alpha_off=1, alpha_on=1, r_off=150000, r_on=1400, D_nm=0.001)
mem.tune(-1.2, 0.000000001)
mem.getState()
mem.getRm()

print(f"Rm = {mem.rm}")
print(f"state = {mem.state}")
