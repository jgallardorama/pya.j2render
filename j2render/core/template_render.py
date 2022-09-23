    
import json
import os
import jinja2
from j2render.app import applogging
import yaml

from j2render.cross.helpers import ensure_dir

CONTEXT_ID="j2r_context"

class Solution():
    def __init__(self, 
                solution_dir, 
                output_dir, 
                template_dir, 
                var_file_dirs = [], 
                var_files = []) -> None:
        self.solution_dir = solution_dir
        self.output_dir = output_dir
        self.template_dir = template_dir
        self.var_file_dirs = var_file_dirs
        self.var_files = var_files
        self.main_template = "main.j2"

    def get_template_dir(self):
        return self.template_dir
    
    def get_main_template(self):
        result = self.main_template
        return result
    
    def get_manifest_path(self):
        return ".j2tool.out"

class RenderContext():
    def __init__(self, solution: Solution) -> None:
        self.solution = solution
        self.file_paths = []
    
    def get_solution(self):
        return self.solution
    
    def add_file(self, file_path):
        norm_file_path = os.path.normpath(file_path)
        
        if not norm_file_path in self.file_paths:
            self.file_paths.append(norm_file_path)
            
    def get_file_paths(self):
        return self.file_paths


logger = applogging.LogManager().get_app_logger()

def j2r_generate(context: RenderContext, model, template_path, file_path):
    
    solution: Solution = context.get_solution()
    template = create_template(context, template_path)
    
    content = template.render(model = model)
    
    result = ""
    
    if file_path:
        output_file_path = os.path.normpath(os.path.join(solution.output_dir, file_path))
        ensure_dir(output_file_path)
                
        context.add_file(output_file_path)
    
        with open(output_file_path, "w") as file:
            file.write(content)
        
        result = output_file_path
    
    return result

def create_template(context: RenderContext, template_path):
    
    template_dir = context.get_solution().get_template_dir()
    templateLoader = jinja2.FileSystemLoader(template_dir)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template_path)
    
    context_dict = {
        "j2r_generate": j2r_generate,
        "j2r_context": context
    }                

    template.globals.update(context_dict)
    return template

def load_manifest(manifest_path: str):
    file_paths = []
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as file:
            file_paths = json.load(file)
    return file_paths


def clean_files(file_paths):    
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)

                    
def save_manifest(manifest_path: str, file_paths):
    with open(manifest_path, "w") as file:
        json.dump(file_paths, file)


def render(solution: Solution, model:dict):
    try:        
        manifest_path = os.path.join(solution.output_dir, solution.get_manifest_path())
        file_paths = load_manifest(manifest_path)
        if file_paths:
            clean_files(file_paths)
        
        renderContext = RenderContext(solution)
        main_template_path = solution.get_main_template()
        template = create_template(renderContext, main_template_path)        
        outputText = template.render(model = model)  # this is where to put args to the template renderer

        save_manifest(manifest_path, renderContext.get_file_paths())

        logger.info(f"Render: {outputText}")
    
    except:
        logger.exception("ERROR ")   