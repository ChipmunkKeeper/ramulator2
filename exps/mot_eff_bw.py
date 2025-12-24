# motivation part
# run effective bandwidth experiment for different DRAMs
# streaming access pattern

import os
import yaml
import subprocess
from copy import deepcopy
from utils.utils import save_ramulator_output

config_base_dir = "/home/jwuev/projects/HB2/exps/mot_eff_bw/configs"
result_base_dir = "/home/jwuev/projects/HB2/exps/mot_eff_bw/results"

if not os.path.exists(result_base_dir):
    os.makedirs(result_base_dir)

# archs = ["DDR3", "DDR4", "DDR5", "GDDR6", "HB"]
archs = ["HB",]
arch_configs = {
    "HB": {"impl": "HB_DRAM", "org_preset": "HB_16Mb_x64", "timing_preset": "HB_500SDR",},
    "DDR3": {"impl": "DDR3", "org_preset": "DDR3_8Gb_x16", "timing_preset": "DDR3_2133L",},
    "DDR4": {"impl": "DDR4", "org_preset": "DDR4_8Gb_x16", "timing_preset": "DDR4_3200W",},
    "DDR5": {"impl": "DDR5", "org_preset": "DDR5_8Gb_x16", "timing_preset": "DDR5_3200AN","RFM": {"BRC": 2},},
    # "LPDDR5": {"impl": "LPDDR5", "org_preset": "LPDDR5_8Gb_x16", "timing_preset": "LPDDR5_6400",},
    "GDDR6": {"impl": "GDDR6", "org_preset": "GDDR6_8Gb_x16", "timing_preset": "GDDR6_2000_1350mV_quad",},
}


for arch in archs:
    print('-' * 50)
    config_path = os.path.join(config_base_dir, f"{arch}_config.yaml")
    result_filename = os.path.join(result_base_dir, f"{arch}.yaml")
    print(f"Running ramulator with config: {config_path}")

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    if arch in ["HB",]:  # busrt 总长8B
        config["Frontend"]["path"] = os.path.join(config_base_dir, "traces/streaming_read_160MB_step_8B.trace")
    elif arch in ["DDR5", "DDR3", "DDR4"]:  # burst 总长64B
        config["Frontend"]["path"] = os.path.join(config_base_dir, "traces/streaming_read_step_64B.trace")
    else:
        raise NotImplementedError(f"arch {arch} not supported yet.")
    # config["MemorySystem"]["DRAM"] = {
    #     "impl": arch_configs[arch]["impl"],
    #     "org": {
    #         "preset": arch_configs[arch]["org_preset"],
    #         "channel": 1,
    #         "rank": 1,
    #     },
    #     "timing": {
    #         "preset": arch_configs[arch]["timing_preset"],
    #     },
    #     "RFM": arch_configs[arch].get("RFM", {}),
    # } 
    # with open(config_path, 'w') as file:
    #     yaml.safe_dump(config, file)
    print(f"Running simulation for arch: {arch}")

    cmd = ["../build/ramulator2", "-c", str(config)]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    # print(stdout)
    save_ramulator_output(stdout, result_filename)
    print('-' * 50)
