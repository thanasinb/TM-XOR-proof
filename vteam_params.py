import json
import sympy

def get_vteam_params(model):
    json_vteam_params = """ 
    {
        "Yalon2012" : {
        "description" : "HfO2 Yalon 2012",
        "alpha_off" : "1.0",
        "alpha_on" : "3.0",
        "v_off" : "0.5",
        "v_on" : "-0.53",
        "r_off" : "2.5 * (10 ** 3)",
        "r_on" : "100.0",
        "k_off" : "40.30 * (10 ** -9)",
        "k_on" : "-80.0",
        "d" : "(10 * 10 ** -9)"
        }, 
        "Yalon2012mod" : {
        "description" : "HfO2 Yalon 2012",
        "alpha_off" : "1.0",
        "alpha_on" : "3.0",
        "v_off" : "0.5",
        "v_on" : "-0.53",
        "r_off" : "2.5 * (10 ** 3)",
        "r_on" : "100.0",
        "k_off" : "40.30 * (10 ** -9)",
        "k_on" : "-80.0",
        "d" : "(10 * 10 ** -9)"
        }, 
        "Ho2017" : {
        "description": "HfO2 Ho 2017",
        "alpha_off" : "2.0",
        "alpha_on" : "1.0",
        "v_off" : "0.7",
        "v_on" : "-0.45",
        "r_off" : "173.8 * (10 ** 3)",
        "r_on" : "7000.0",
        "k_off" : "28.92 * (10 ** -9)",
        "k_on" : "-198.72 * (10 ** -3)",
        "d" : "(10 * 10 ** -9)"
        }
    }
    """

    # parse x:
    vteam_params = json.loads(json_vteam_params)
    selected_params = vteam_params[model]
    for key in selected_params:
        if key != "description":
            selected_params[key] = float(sympy.sympify(selected_params[key]))
        print(f"{key}:{selected_params[key]}")
    print(f"\n")

    return selected_params
