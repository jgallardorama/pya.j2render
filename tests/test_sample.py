# Sample Test passing with nose and pytest


import os
import shutil
import unittest

from j2render import template_render

class TestRender(unittest.TestCase):

    def test_render(self):
        
        
        data_dirs = ["sample/data"]
        output_dir = "sample/output"
        template_dirs = ["sample/templates"]
        
        shutil.rmtree(output_dir, ignore_errors=True)
        
        template_render.render(data_dirs, template_dirs, output_dir)
