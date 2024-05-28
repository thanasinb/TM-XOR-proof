import json

json_vteam_params = """ 
[ 
    {
    "id": 1, 
    "description" : "HfO2 Yalon 2012",
    "alpha_off" = "1.0",
    "alpha_on" = "3.0",
    "v_off" = "0.5",
    "v_on" = "-0.53",
    "r_off" = "2.5 * (10 ** 3)",
    "r_on" = "100.0",
    "k_off" = "40.30 * (10 ** -9)",
    "k_on" = "-80.0",
    "d" = "(10 * 10 ** -9)"
    }, 
    {
    "id": 2, 
    "description": "HfO2 Ho 2017",
    "alpha_off" = "2.0",
    "alpha_on" = "1.0",
    "v_off" = "0.7",
    "v_on" = "-0.45",
    "r_off" = "173.8 * (10 ** 3)",
    "r_on" = "7000.0",
    "k_off" = "28.92 * (10 ** -9)",
    "k_on" = "-198.72 * (10 ** -3)",
    "d" = "(10 * 10 ** -9)"
    }
] 
"""

# parse x:
vteam_params = json.loads(json_vteam_params)


def get_vteam_params(id_model):
    return vteam_params[id_model]
