# Sample Test passing with nose and pytest


import shutil
from j2tool import cli
from tests.helpers import BaseTestSuite, get_runner


class CmdInitTestSuite(BaseTestSuite):
    def test_cmd_init(self):
        runner = get_runner()

        output_dir = "output/test_case_init"

        shutil.rmtree(output_dir, ignore_errors=True)

        args = [
            "--no-color",
            "-vvvv",
            "init",
            "--solution-dir",
            output_dir,
        ]

        result = runner.invoke(cli.main_command, args)

        # helpers.dump_result(result)

        assert result.exit_code == 0
