# Sample Test passing with nose and pytest


import os
import shutil
import unittest

from j2render.core import template_render

class TestRender(unittest.TestCase):

    def test_render(self):
        var_file_dirs = ["sample/data"]
        output_dir = "sample/output"
        template_dir = "sample/templates"
        
        shutil.rmtree(output_dir, ignore_errors=True)
        solution = template_render.Solution(output_dir, template_dir, var_file_dirs)        
        
        template_render.render(solution)
