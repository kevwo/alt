from alt import ConfigFactory, AbsoluteConfigFactory
import os
import unittest
from ddt import ddt, data, unpack


@ddt
class ConfigFactories(unittest.TestCase):
    @data((os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'examples', 'basic_tests'), 'tests', []),
          (os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'examples', 'basic_tests'), 'tests.yaml', []),
          (os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'examples', 'test_with_secrets'), 'tests.yaml', ['secrets']),
          (os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'examples', 'test_with_secrets'), 'tests.yaml', ['secrets.yaml']))
    @unpack
    def test_relative(self, base_dir, test_name, secrets):
        config = ConfigFactory(base_dir, *secrets)
        data = config.get(test_name)
        self.assertTrue('test_suites' in data)

    @data((os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'examples', 'test_with_secrets'), 'tests.yaml', []))
    @unpack
    def test_relative_negative(self, base_dir, test_name, secrets):
        config = ConfigFactory(base_dir, *secrets)
        self.assertRaises(Exception, config.get, test_name)

    @data((os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'examples', 'basic_tests', 'tests.yaml'), []),
          (os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'examples', 'test_with_secrets', 'tests.yaml'), [os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'examples', 'test_with_secrets', 'secrets.yaml')]))
    @unpack
    def test_absolute(self, test_name, secrets):
        config = AbsoluteConfigFactory(*secrets)
        data = config.get(test_name)
        self.assertTrue('test_suites' in data)

    @data((os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'examples', 'basic_tests', 'tests'), []),
          (os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'examples', 'test_with_secrets', 'tests'), []))
    @unpack
    def test_absolute_negative(self, test_name, secrets):
        config = AbsoluteConfigFactory(*secrets)
        self.assertRaises(Exception, config.get, test_name)