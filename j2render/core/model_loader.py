


import os
from j2render.core.template_render import Solution
from ..app import applogging
import yaml

logger = applogging.LogManager().get_app_logger()

def load_model(solution:Solution) -> dict:

    result = {}
    var_file_dirs = solution.var_file_dirs
    
    for var_file_dir in var_file_dirs:
        for filename in os.listdir(var_file_dir):
            fileparts = os.path.splitext(filename)
            extension = fileparts[1]
            if extension == ".lst":
                logger.info(f"process {filename}")
                full_name = os.path.join(var_file_dir, filename)
                with open(full_name, "r") as f:
                    lines = f.read().splitlines()
                result[fileparts[0]] = lines
                
            if extension in [".yml", ".yaml", ".json"]:
                logger.info(f"process {filename}")
                full_name = os.path.join(var_file_dir, filename)
                with open(full_name, "r") as f:
                    lines = yaml.safe_load(f)
                result[fileparts[0]] = lines
                
    return result