from alt import AltRunner, ConfigFactory
import logging
import os

logger = logging.getLogger('test')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
logger.addHandler(ch)


def work():
    directory = os.path.dirname(__file__)
    config = ConfigFactory(directory)
    data = config.get('tests')
    runner = AltRunner(data, logger)
    runner.run()


if __name__ == '__main__':
    work()