1.) Copy this directory onto your machine
2.) Notice assert response.request.headers['authorization'] == 'MY_TOP_SECRET_KEY' in test_code.py
3.) Notice that secrets.yaml contains the string 'MY_TOP_SECRET_KEY', you can .gitignore this file to protect your keys
4.) run: python testRunner.py
5.) You should get this output:

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
Finished test: #1.2 SampleSimpleTest simple_test - (0.30s) Result: Passed
======================================================================
Starting test: #1.3 SampleSimpleTest simple_test - Not Executed
Sending GET to url: https://github.com/kevwo/badurl
Received response code: 404
Finished test: #1.3 SampleSimpleTest simple_test - (0.28s) Result: Passed
======================================================================
======================================================================
3/3 Passed:
#1.1 SampleSimpleTest simple_test - (0.61s) Result: Passed
#1.2 SampleSimpleTest simple_test - (0.30s) Result: Passed
#1.3 SampleSimpleTest simple_test - (0.28s) Result: Passed
======================================================================
0/3 Failed:
======================================================================
0/3 Skipped:
======================================================================
Elapsed time: 1.22s