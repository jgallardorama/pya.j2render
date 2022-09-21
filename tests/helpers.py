

import unittest

from click.testing import CliRunner
import logging
logger = logging.getLogger("APPTESTING")
logger.setLevel(logging.DEBUG)

class BaseTestSuite(unittest.TestCase):
  pass


def get_runner():
    runner = CliRunner(mix_stderr=False)
    return runner


def dump_result(result):
    # logger.info(f"OUTPUT:\n{result.output}")
    # logger.info(f"STDERR:\n{result.stderr}")

    pass
