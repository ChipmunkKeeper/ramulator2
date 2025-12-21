import os
import yaml
import subprocess

# Example configuration files and result file locations
config_directory = "./configs/example"
result_directory = "./results"

if not os.path.exists(result_directory):
    os.makedirs(result_directory)

# # Read the list of config files from the config directory
# config_files = [f for f in os.listdir(config_directory) if f.endswith(".yaml")]
config_files = ["example_config.yaml"]

# Loop over each config file and run ramulator
for config_file in config_files:
    config_path = os.path.join(config_directory, config_file)
    result_filename = os.path.join(result_directory, config_file.replace(".yaml", ".txt"))
    
    print(f"Running ramulator with config: {config_path}")

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Construct the command
    cmd = ["./ramulator2", "-c", str(config)]
    
    with open(result_filename, 'w') as result_file:
        process = subprocess.Popen(cmd, stdout=result_file, stderr=subprocess.PIPE)
        stderr = process.communicate()[1]
        
        if stderr:
            print(f"Error occurred while running ramulator: {stderr.decode()}")
        else:
            print(f"Successfully ran ramulator with config: {config_file}")


