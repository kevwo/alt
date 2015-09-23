1.) Copy this directory onto your machine
2.) run: python testRunner.py
3.) You should get this output:

Starting AltRunner...
======================================================================
Starting test: #1.1 SampleSimpleTest simple_test - Not Executed
Sending GET to url: https://github.com/kevwo
Received response code: 200
Finished test: #1.1 SampleSimpleTest simple_test - (0.64s) Result: Passed
======================================================================
Skipping test: #1.2 SampleSimpleTest simple_test - Not Executed
======================================================================
Starting test: #1.3 SampleSimpleTest simple_test (expects a 404) - Not Executed
Sending GET to url: https://github.com/kevwo/notarepo
Received response code: 404
Finished test: #1.3 SampleSimpleTest simple_test (expects a 404) - (0.28s) Result: Passed
======================================================================
Starting test: #1.4 SampleSimpleTest simple_test (this test will fail) - Not Executed
Sending GET to url: https://github.com/kevwo
Received response code: 200
error
Traceback (most recent call last):
  File "D:\Tools\Python34\lib\site-packages\alt.py", line 138, in execute
    self.test_func(self.param_self, *self.param_args, **self.param_kwargs)
  File "D:\dev\alt\examples\ex01\test_code.py", line 12, in simple_test
    assert response.status_code == expected_response_code
AssertionError
Finished test: #1.4 SampleSimpleTest simple_test (this test will fail) - (0.34s) Result: Failed
======================================================================
======================================================================
2/4 Passed:
#1.1 SampleSimpleTest simple_test - (0.64s) Result: Passed
#1.3 SampleSimpleTest simple_test (expects a 404) - (0.28s) Result: Passed
======================================================================
1/4 Failed:
#1.4 SampleSimpleTest simple_test (this test will fail) - (0.34s) Result: Failed
======================================================================
1/4 Skipped:
#1.2 SampleSimpleTest simple_test - Not Executed
======================================================================
Elapsed time: 1.28s