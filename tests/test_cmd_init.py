# Sample Test passing with nose and pytest


import os
import shutil
import unittest
from j2tool import cli
from tests.helpers import BaseTestSuite, get_runner

class CmdInitTestSuite(BaseTestSuite):

    def test_cmd_init(self):
        runner = get_runner()

        output_dir = "output/test_case_init"
        
        shutil.rmtree(output_dir)
# @click.option("--solution-dir", "solution_dir", default=".")
# @click.option("--var-file","var_files", multiple=True)
# @click.option("--var", "var_values",multiple=True)
# @click.option("--template-dir", "template_dir")
# @click.option("--output", "output_dir")
# @click.option("--clean", "-c", "clean", default=False, is_flag=True, help="Clean output directory")
# @click.option("--watch", "-w", "watch", default=False, is_flag=True, help="Watch source folder")

        args = ["--no-color",
                "-vvvv",
                "init",
                "--solution-dir",
                output_dir,
                ]

        result = runner.invoke(cli.main_command, args)

        # helpers.dump_result(result)

        assert result.exit_code == 0
