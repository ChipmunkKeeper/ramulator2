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

archs = ["test"]
arch_configs = {
    "test": {
        "impl": "DDR4",
        "org_preset": "DDR4_8Gb_x8",
        "timing_preset": "DDR4_2400R",
    },
}

with open(os.path.join(config_base_dir, "template.yaml"), 'r') as file:
        base_config = yaml.safe_load(file)

for arch in archs:
    config_path = os.path.join(config_base_dir, f"{arch}.yaml")
    result_filename = os.path.join(result_base_dir, f"{arch}.yaml")
    print(f"Running ramulator with config: {config_path}")

    config = deepcopy(base_config)
    config["Frontend"]["path"] = os.path.join(config_base_dir, "traces/streaming_read.trace")
    config["MemorySystem"]["DRAM"] = {
        "impl": arch_configs[arch]["impl"],
        "org": {
            "preset": arch_configs[arch]["org_preset"],
            "channel": 1,
            "rank": 1,
        },
        "timing": {
            "preset": arch_configs[arch]["timing_preset"],
        },
    } 

    with open(config_path, 'w') as file:
        yaml.safe_dump(config, file)

    cmd = ["../ramulator2", "-c", str(config)]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    
    save_ramulator_output(stdout, result_filename)
