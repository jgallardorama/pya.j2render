# Sample Test passing with nose and pytest


import os
import shutil
import unittest

from j2tool.core import template_render
from j2tool.core.model_loader import load_model

class TestRender(unittest.TestCase):

    def test_render(self):
        solution_dir = "tests/data/sample01"
        var_file_dirs = [f"{solution_dir}/data"]
        output_dir = "output"
        template_dir = f"{solution_dir}/templates"
        
        shutil.rmtree(output_dir, ignore_errors=True)
        solution = template_render.Solution(solution_dir, output_dir, template_dir, var_file_dirs)        
        model = load_model(solution)
        template_render.render(solution, model)
