# ALT:  API Level Tests

Test your web api with minimal effort. 

```
pip install alt
```

###Why alt?:
* Rather than dev testing with a series of commands, write a test once and reuse infinitely
* Write an entire test suite for integration testing your web api. Both localhost or on a development server
* Practice test driven development and write your test before your api
* Extension on unit testing and run the web api tests before merging code.

##Batteries included! Jump in & run sample code!
Running this command will generate a directory "skeleton" in your current directory and populate it with __fully functional__ code (tests, test data, and test runner). Just modify this skeleton to fit your need!
```python
import alt
alt.get_skeleton()
```

##Want to learn more??:

###Tests are simple to write:

```python
from alt import AltTest, request


class SampleSimpleTest:

    @AltTest
    def simple_test(self, expected_response_code, **kwargs):
        """
        Simple test.
        """
        response = request(**kwargs)
        assert response.status_code == expected_response_code
```

###Leverage a YAML ConfigParser to both avoid data duplication and protect your api keys
```yaml
global:
    default_args: &default_args
        url: https://github.com/kevwo
        method: GET
        expected_response_code: 200
        api_key: *secrets_default_api_key  # secret api key stored elsewhere
test_suites:
  - module_name: test_code
    class_name: SampleSimpleTest
    tests:
      - name: simple_test
        data_points:
          - <<: *default_args  #this runs the test with default args
          - <<: *default_args  #this runs the test with a different url
            url: https://github.com/kevwo/alt/tree/master/examples
          - <<: *default_args  #this runs the test with a different url and error code
            url: https://github.com/kevwo/alt/tree/master/examples/thisisnotanexample
            expected_response_code: 404
```

###Human readable output
```
Starting AltRunner...
======================================================================
Starting test: #1.1 SampleSimpleTest simple_test - Not Executed
Sending GET to url: https://github.com/kevwo
Received response code: 200
Finished test: #1.1 SampleSimpleTest simple_test - (0.61s) Result: Passed
======================================================================
Starting test: #1.2 SampleSimpleTest simple_test - Not Executed
Sending GET to url: https://github.com/kevwo/alt/tree/master/examples
Received response code: 200
Finished test: #1.2 SampleSimpleTest simple_test - (0.27s) Result: Passed
======================================================================
Starting test: #1.3 SampleSimpleTest simple_test - Not Executed
Sending GET to url: https://github.com/kevwo/alt/tree/master/examples/thisisnotanexample
Received response code: 404
Finished test: #1.3 SampleSimpleTest simple_test - (0.25s) Result: Passed
======================================================================
======================================================================
3/3 Passed:
#1.1 SampleSimpleTest simple_test - (0.61s) Result: Passed
#1.2 SampleSimpleTest simple_test - (0.27s) Result: Passed
#1.3 SampleSimpleTest simple_test - (0.25s) Result: Passed
======================================================================
0/3 Failed:
======================================================================
0/3 Skipped:
======================================================================
Elapsed time: 1.14s
```

###Use examples as a starting guide
Just copy the directory to your machine and run python testRunner.py
* https://github.com/kevwo/alt/tree/master/examples/basic_tests
* https://github.com/kevwo/alt/tree/master/examples/test_with_secrets
