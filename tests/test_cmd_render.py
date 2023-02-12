# Sample Test passing with nose and pytest


from j2tool import cli
from tests.helpers import BaseTestSuite, get_runner


class CmdRenderTestSuite(BaseTestSuite):
    def test_cmd_render(self):
        runner = get_runner()

        # @click.option("--solution-dir", "solution_dir", default=".")
        # @click.option("--var-file","var_files", multiple=True)
        # @click.option("--var", "var_values",multiple=True)
        # @click.option("--template-dir", "template_dir")
        # @click.option("--output", "output_dir")
        # @click.option("--clean", "-c", "clean", default=False, is_flag=True, help="Clean output directory")
        # @click.option("--watch", "-w", "watch", default=False, is_flag=True, help="Watch source folder")

        test_data_dir = "tests/data/sample01"

        args = [
            "--no-color",
            "-vvvv",
            "render",
            "--solution-dir",
            "sample",
            "--output",
            "output",
            "--var-file-dir",
            f"{test_data_dir}/data",
            "--template-dir",
            f"{test_data_dir}/templates",
        ]

        result = runner.invoke(cli.main_command, args)

        # helpers.dump_result(result)

        assert result.exit_code == 0
