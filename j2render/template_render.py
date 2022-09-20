    
import os
import jinja2
from j2render import log_manager


logger = log_manager.get_logger(__name__)

def render(data_dirs, template_dirs, output_file):
    try:        

        templateLoader = jinja2.FileSystemLoader(template_dirs[0])
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "main.j2"
        template = templateEnv.get_template(TEMPLATE_FILE)

        model = {}

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
                
        outputText = template.render(model = model)  # this is where to put args to the template renderer

        logger.info(f"Render: {outputText}")
    
    except:
        logger.exception("ERROR ")   