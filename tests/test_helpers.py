# Sample Test passing with nose and pytest


import os
import shutil
import unittest

from j2tool.cross import helpers


class TestRender(unittest.TestCase):

    def test_ident(self):

        text = """hola mundo!
Como estás!!
Muy bien"""
        result = helpers.ident_text(text, 4)

        test_result = """    hola mundo!
    Como estás!!
    Muy bien\n"""

        assert result == test_result
