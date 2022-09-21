    
import os
import jinja2
from j2render.app import log_manager
import yaml

class Solution():
    def __init__(self, output_dir, template_dir, var_file_dirs = [], var_files = []) -> None:
        self.output_dir = output_dir
        self.template_dir = template_dir
        self.var_file_dirs = var_file_dirs
        self.var_files = var_files
        self.main_template = "main.j2"


logger = log_manager.get_logger(__name__)

def j2r_generate(context, data, template_path, file_path):
    
    template = create_template(context["template_dirs"], template_path)
    
    content = template.render(model = data)
    
    result = ""
    
    if file_path:
        output_file_path = os.path.normpath(os.path.join("sample/output", file_path))
        output_file_dir = os.path.dirname(output_file_path)
        os.makedirs(output_file_dir, exist_ok=True)
    
        with open(output_file_path, "w") as file:
            file.write(content)
        
        result = output_file_path
    
    return result

def create_template(solution: Solution, template_path):
    templateLoader = jinja2.FileSystemLoader(solution.template_dir)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template_path)
    
    func_dict = {
        "j2r_generate": j2r_generate,
        "j2r_solution": solution
    }                

    template.globals.update(func_dict)
    return template



def render(solution: Solution):
    try:        
        model = {}
        data_dirs = solution.var_file_dirs
        template_dirs = solution.template_dir
        
        for data_dir in data_dirs:
            for filename in os.listdir(data_dir):
                fileparts = os.path.splitext(filename)
                extension = fileparts[1]
                if extension == ".lst":
                    logger.info(f"process {filename}")
                    full_name = os.path.join(data_dir, filename)
                    with open(full_name, "r") as f:
                        lines = f.read().splitlines()
                    model[fileparts[0]] = lines
                    
                if extension in [".yml", ".yaml"]:
                    logger.info(f"process {filename}")
                    full_name = os.path.join(data_dir, filename)
                    with open(full_name, "r") as f:
                        lines = yaml.safe_load(f)
                    model[fileparts[0]] = lines                    
        
        TEMPLATE_FILE = "main.j2"

        template = create_template(template_dirs, TEMPLATE_FILE)        
        outputText = template.render(model = model)  # this is where to put args to the template renderer

        logger.info(f"Render: {outputText}")
    
    except:
        logger.exception("ERROR ")   