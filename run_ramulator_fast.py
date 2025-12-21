import os
import yaml 
from copy import deepcopy
import subprocess

baseline_config_file = "./configs/example/load_store.yaml"
nRCD_list = [10,]

base_config = None
with open(baseline_config_file, 'r') as f:
    base_config = yaml.safe_load(f)

# 改变某个参数
base_config["Frontend"]["Translation"]["impl"] = "NoTranslation"


for i, nRCD in enumerate(nRCD_list):
    config = deepcopy(base_config)
    print(f"======== Running simulation with nRCD = {nRCD} ========")
    config["MemorySystem"]["DRAM"]["timing"]["nRCD"] = nRCD
    cmds = ["./ramulator2", '-c', str(config)]
    subprocess.run(cmds)