# Sample Test passing with nose and pytest


import unittest

from j2render import template_render

class TestRender(unittest.TestCase):

    def test_render(self):
        data_dirs = ["sample/data"]
        output_dir = "sample/output"
        template_dirs = ["sample/templates"]
        
        template_render.render(data_dirs, template_dirs, output_dir)
