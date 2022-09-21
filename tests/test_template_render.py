# Sample Test passing with nose and pytest


import os
import shutil
import unittest

from j2render.core import template_render
from j2render.core.model_loader import load_model

class TestRender(unittest.TestCase):

    def test_render(self):
        var_file_dirs = ["sample/model"]
        output_dir = "sample/output"
        solution_dir = "sample"
        template_dir = "sample/templates"
        
        shutil.rmtree(output_dir, ignore_errors=True)
        solution = template_render.Solution(solution_dir, output_dir, template_dir, var_file_dirs)        
        model = load_model(solution)
        template_render.render(solution, model)
