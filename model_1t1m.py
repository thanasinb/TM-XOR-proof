import vteam_params

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

# print(f"dt_off = {dt_off}")
# print(f"dt_on = {dt_on}")
# print(f"dt = {dt}\n")

rm = r_on
print (0, rm)

delta_rm_1 = (r_off-r_on)/d
delta_rm_3_off = k_off * dt_off

for i in range(100):
	delta_rm_2_off = ((((rm * voltage) / (rm + rt_off)) / v_off) - 1) ** alpha_off
	delta_rm_off = delta_rm_1 * delta_rm_2_off * delta_rm_3_off

	rm += delta_rm_off
	print(i+1, rm, delta_rm_off)

rm = r_off
print (0, rm)

delta_rm_1 = (r_off-r_on)/d
delta_rm_3_on = k_on * dt_on

for i in range(100):
	delta_rm_2_on = ((((rm * voltage) / (rm + rt_on)) / v_on) - 1) ** alpha_on
	delta_rm_on = delta_rm_1 * delta_rm_2_on * delta_rm_3_on

	rm -= delta_rm_on
	print(i+1, rm, delta_rm_on)