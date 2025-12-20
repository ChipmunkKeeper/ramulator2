import os
import yaml 
from copy import deepcopy
import subprocess

baseline_config_file = "./example_config.yaml"
nRCD_list = [10, 15, 20, 25]

base_config = None
with open(baseline_config_file, 'r') as f:
    base_config = yaml.safe_load(f)


for i, nRCD in enumerate(nRCD_list):
    config = deepcopy(base_config)
    print(f"======== Running simulation with nRCD = {nRCD} ========")
    config["MemorySystem"]["DRAM"]["timing"]["nRCD"] = nRCD
    cmds = ["./ramulator2", '-c', str(config)]
    subprocess.run(cmds)