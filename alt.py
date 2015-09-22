import sys
from urllib.parse import urljoin
import time
import logging
import requests


LINE_DELIMITER = "="*70


def get_default_logger():
    return logging.getLogger('alt')


def format_time(time_seconds):
    m, s = divmod(time_seconds, 60)
    m = int(round(m))
    if m == 0:
        to_return = "%.2fs" % s
    else:
        to_return = int(round(s))
        h, m = divmod(m, 60)
        if h == 0:
            to_return = str(m) + "m:" + to_return
        else:
            d, h = divmod(h, 24)
            to_return = str(h) + "h:" + to_return
            if d > 0:
                to_return = str(d) + "d:" + to_return
    return to_return


def test_decorator(func):
    def test_executor(self, *args, **kwargs):
        logger = kwargs.get('logger', get_default_logger())
        if 'url' in kwargs:
            kwargs['url'] = kwargs['url'].format(**kwargs)
        if 'endpoint' in kwargs:
            kwargs['endpoint'] = kwargs['endpoint'].format(**kwargs)
        if 'baseurl' in kwargs:
            kwargs['baseurl'] = kwargs['baseurl'].format(**kwargs)
        test = Test(logger, kwargs.get('test_number', "?"), kwargs.get('param_set_number', "?"), func, self, args,
                    kwargs, skip=kwargs.get('skip_test', False), nickname=kwargs.get('nickname', None))
        test.execute()
        return test
    return test_executor


def invoke_rest_method(**kwargs):
        """
        Invokes a rest api test
        :param kwargs:
            REQUIRED:

            method = 'GET', 'POST', 'PUT', 'DELETE'

            url = "http://localhost/api/controller"
                or
            baseurl = "http://localhost/"
            endpoint = "api/controller"

            OPTIONAL:

            headers = {'header_name':'header_value', 'header2_name':'header2_value'}

            json = {'key1':'value1', 'key2':'value2'}   #Will be sent as json encoded data
                or
            form = {'key1':'value1', 'key2':'value2'}   #Will be sent as form encoded data

            api_key = "ey123asdk93e378hsdfsfdf"
            silent = True,False  (to not log request/response. Default False)
        :return:
        """
        logger = kwargs.get('logger', get_default_logger())
        args = {}
        headers = kwargs.get('headers', {})
        api_key = kwargs.get('api_key', None)
        if api_key is not None:
            headers['Authorization'] = api_key
        if headers is not {}:
            args['headers'] = headers
        json = kwargs.get('json', None)
        if json is not None:
            args['json'] = json
        form = kwargs.get('form', None)
        if form is not None:
            args['data'] = form
        if json is not None and form is not None:
            raise ValueError('Cannot specify both json and form parameters')
        url = kwargs.get('url', None)
        if url is None:
            baseurl = kwargs.get('baseurl', None)
            endpoint = kwargs.get('endpoint', None)
            if baseurl is None or endpoint is None:
                raise ValueError('Invalid test arguments. Must specify {url} or {baseurl, endpoint}')
            url = urljoin(baseurl, endpoint)
        method = kwargs.get('method', None)
        if method is None:
            raise ValueError('Invalid test arguments. Must specify {method}')
        silent = kwargs.get('silent', False)
        if not silent:
            logger.debug("Sending {} to url: {}".format(method, url))
        req = requests.request(method, url, **args)
        if not silent:
            logger.debug("Received response code: {}".format(req.status_code))
        return req

AltTest = test_decorator
request = invoke_rest_method


class Test:
    def __init__(self, logger, test_number, param_set_number, test_func, param_self, param_args, param_kwargs, skip=False, nickname=None):
        self.logger = logger
        self.test_func = test_func
        self.param_self = param_self
        self.param_args = param_args
        self.param_kwargs = param_kwargs
        self.test_suite = param_self.__class__.__name__
        self.test_name = test_func.__name__
        self.test_number = test_number
        self.param_set_number = param_set_number
        self.test_skipped = skip
        self.nickname = nickname
        self.executed = False
        self.elapsed_time = 0
        self.test_passed = False

    def execute(self):
        if self.test_skipped is True:
            self.logger.debug("Skipping test: {}".format(self))
            return
        if self.executed is True:
            raise ValueError("Test already executed")
        start = time.time()
        self.logger.debug("Starting test: {}".format(self))
        try:
            self.test_func(self.param_self, *self.param_args, **self.param_kwargs)
            self.test_passed = True
        except:
            self.logger.error("error", exc_info=True)
        self.executed = True
        self.elapsed_time = time.time() - start
        self.logger.debug("Finished test: {}".format(self))

    def __str__(self):
        test_prefix = "#{}.{} {} {}".format(self.test_number, self.param_set_number, self.test_suite, self.test_name)
        if self.nickname is not None:
            test_prefix += " ({})".format(self.nickname)
        if not self.executed:
            return "{} - Not Executed".format(test_prefix)
        else:
            return "{} - ({}) Result: {} ".format(test_prefix, format_time(self.elapsed_time),
                                                  'Passed' if self.test_passed is True else 'Failed')


class AltTestRunner:
    def __init__(self, test_data, logger=None):
        self.test_data = test_data
        if logger is None:
            logger = get_default_logger()
        self.logger = logger

    @staticmethod
    def import_test_module(name):
        m = __import__(name)
        for n in name.split(".")[1:]:
            m = getattr(m, n)
        return m

    def run(self):
        self.logger.debug("Starting {}...".format(self.__class__.__name__))
        start = time.time()
        passed = []
        failed = []
        skipped = []
        test_num = 1
        for bvt in self.test_data['test_suites']:
            module = self.import_test_module(bvt['module_name'])
            class_ = getattr(module, bvt['class_name'])
            my_class = class_()
            tests = bvt['tests']
            for test in tests:
                sub_test_num = 1
                name = test['name']
                test_func = getattr(my_class, name)
                for data_set in test['data_points']:
                    invalid_args = {'logger', 'test_number', 'param_set_number'}.intersection(data_set)
                    if invalid_args:
                        raise ValueError('You cannot use the following arguments in tests: {}'.format(", ".join(invalid_args)))
                    try:
                        self.logger.debug("=" * 70)
                        data_set['test_number'] = test_num
                        data_set['param_set_number'] = sub_test_num
                        data_set['logger'] = self.logger
                        sub_test_num += 1
                        test_obj = test_func(**data_set)
                        if test_obj.test_skipped is True:
                            skipped.append(test_obj)
                        elif test_obj.test_passed is True:
                            passed.append(test_obj)
                        else:
                            failed.append(test_obj)
                    except Exception as e:
                        self.logger.error("Test failed", exc_info=True)
                        self.logger.error("Test failed: {}".format(e), file=sys.stderr)
                        sys.exit(1)
                test_num += 1
        self.logger.debug(LINE_DELIMITER)
        self.logger.debug(LINE_DELIMITER)
        total = len(passed) + len(failed) + len(skipped)
        self.logger.debug("{}/{} Passed: ".format(len(passed), total))
        for test in passed:
            self.logger.debug(test)
        self.logger.debug(LINE_DELIMITER)
        self.logger.debug("{}/{} Failed: ".format(len(failed), total))
        for test in failed:
            self.logger.debug(test)
        self.logger.debug(LINE_DELIMITER)
        self.logger.debug("{}/{} Skipped: ".format(len(skipped), total))
        for test in skipped:
            self.logger.debug(test)
        self.logger.debug(LINE_DELIMITER)
        self.logger.debug("Elapsed time: {}".format(format_time(time.time() - start)))