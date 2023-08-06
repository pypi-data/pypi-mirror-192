import logging
import os
import shutil
import tempfile
import unittest

from fastiot.core import FastIoTService
from fastiot.core.broker_connection import BrokerConnectionDummy
from fastiot.env import env_basic
from fastiot.env.env_constants import FASTIOT_CONFIG_DIR
from fastiot.util.read_yaml import read_config
from fastiot.testlib import populate_test_env

BASIC_YAML = """
config item 1:
  foo: bar
  key: value

config item 2:
  the answer: 42
"""
expected_result = {'config item 1': {'foo': 'bar', 'key': 'value'},
                   'config item 2': {'the answer': 42}}


class SimpleService(FastIoTService):
    """ No methods implemented """


class TestYAMLReader(unittest.TestCase):

    def setUp(self):
        logging.getLogger("yaml_config").setLevel(logging.ERROR)
        populate_test_env()

        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        os.environ[FASTIOT_CONFIG_DIR] = self.test_dir

        self.service = SimpleService(BrokerConnectionDummy())
        self.service.service_id = '1'

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)
        del os.environ[FASTIOT_CONFIG_DIR]

    @staticmethod
    def create_yaml_file(filename, content=BASIC_YAML):
        with open(filename, 'w') as file:
            file.write(content)

    def test_config_per_service(self):
        config_file = os.path.join(env_basic.config_dir, 'SimpleService.yaml')
        self.create_yaml_file(config_file)
        result = read_config(self.service)

        self.assertEqual(expected_result, result)

    def test_config_per_instance(self):
        config_file = os.path.join(env_basic.config_dir, 'SimpleService_1.yaml')
        self.create_yaml_file(config_file)
        result = read_config(self.service)

        self.assertEqual(expected_result, result)

    def test_config_with_filename(self):
        config_file = os.path.join(env_basic.config_dir, 'myconfig.yaml')
        self.create_yaml_file(config_file)
        result = read_config('myconfig.yaml')

        self.assertEqual(expected_result, result)

    def test_no_config(self):
        result = read_config(self.service)
        self.assertEqual({}, result)

    def test_no_content(self):
        config_file = os.path.join(env_basic.config_dir, 'SimpleService_1.yaml')
        self.create_yaml_file(config_file, content="")

        result = read_config(self.service)
        self.assertEqual({}, result)


if __name__ == '__main__':
    unittest.main()
