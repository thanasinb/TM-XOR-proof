# cython: language_level=3

import numpy as np
import pyximport; pyximport.install(setup_args={
                              "include_dirs":np.get_include()},
                            reload_support=True)
from model_1t1m import Model1T1M
import vteam_params

number_of_states = 100
ta_state = 0
init_memristor_state = 0.5
voltage = 1.2
rt_off = 2160
rt_on = 5600

selected_params = vteam_params.get_vteam_params("Seiler2024")
alpha_off = selected_params["alpha_off"]
alpha_on = selected_params["alpha_on"]
v_off = selected_params["v_off"]
v_on = selected_params["v_on"]
r_off = selected_params["r_off"]
r_on = selected_params["r_on"]
k_off = selected_params["k_off"]
k_on = selected_params["k_on"]
d = selected_params["d"]
dt_off = 10 * (10 ** -9)
dt_on = 40 * (10 ** -9)

clause = 0
feature = 0
negated = 0
rm = r_on

my_1t1m = Model1T1M(ta_state,
                    init_memristor_state,
                    number_of_states,
                    alpha_off,
                    alpha_on,
                    v_off,
                    v_on,
                    r_off,
                    r_on,
                    k_off,
                    k_on,
                    d,
                    clause,
                    feature,
                    negated,
                    rt_off,
                    rt_on)

for i in range(100):
    my_1t1m.tune(voltage, dt_off)
    print(i+1, my_1t1m.get_mr_xdx())

for i in range(100):
    my_1t1m.tune(-voltage, dt_on)
    print(i+1, my_1t1m.get_mr_xdx())