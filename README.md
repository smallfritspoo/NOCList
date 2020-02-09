NOCList - Retrieve VIP user list
===========
A script to connect to the BADSEC vip user api, retrieve the userlist and format a json list.

## Tests
Tests are included in `tests/`, and a script to run the tests is provided as `run_tests.sh`

Tests can be manually run from the projects root directory with

    python -m pytest -v --cov=noclist ./tests/

_Note_: Tests can take a little bit of time to complete the requirements of the project involved writing the retry and
backoff logic by hand and this has not been mocked out. This caveat could be mitigated by using a requests plugin that 
allow retries or something like tenacity that can be easily mocked out.

    ================================================ test session starts ================================================
    platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1 -- /usr/bin/python3
    cachedir: .pytest_cache
    rootdir: /root/noclist
    plugins: requests-mock-1.7.0, cov-2.8.1
    collected 3 items
    
    tests/test_noclist.py::test_connection_error PASSED                                                           [ 33%]
    tests/test_noclist.py::test_exit_on_status_code PASSED                                                        [ 66%]
    tests/test_noclist.py::test_successful_retrieval PASSED                                                       [100%]
    
    ----------- coverage: platform linux, python 3.6.9-final-0 -----------
    Name                  Stmts   Miss  Cover
    -----------------------------------------
    noclist/__init__.py       1      0   100%
    noclist/noclist.py       56      4    93%
    -----------------------------------------
    TOTAL                    57      4    93%
    
    
    ================================================ 3 passed in 36.16s =================================================

## Requirements
    requests-mock
    requests
    pytest
    pytest-cov

also included is a `requirements.txt` file for use with pip.

## Logging
Logging has been configured using the standard python logging library. The log will be written to `noclist.log`
and is set to debug by default.

Logger attributes can be configured through the following environment variables:

    LOG_LEVEL defaults to 'DEBUG'
    LOG_FILE defaults to 'noclist.log'
    LOG_FORMAT defaults to '%(asctime)s %(levelname)s %(message)s'


## Documentation
Code is documented using google-style doc strings that are compatible with the sphinx extenstion napoleon.
These tend to be  bit easier to read than the standard reST format.

## Run Script
The script is expecting the api to be available on 127.0.0.1:8888 by default.

I highly recommend setting up a virtualenvironment to work in.

    python -m venv virtualenvironment

Activate the virtualenvironment

    source virtualenvironment/bin/activate

Install the requirements

    pip install -r requirements.txt

Run the script

    python noclist.py

If the service is available you will see the following output.

    ["18207056982152612516", "7692335473348482352", "6944230214351225668", ...

If the service fails to respond within 3 attempts or responds with any status_code other than `200` you
will see

    Maximum retries attempted to http://http://127.0.0.1:8888/auth. Exiting

with an exit code of `1`

    # echo $?
    1

when you are finished, deactivate your virtualenvironment

    deactivate

