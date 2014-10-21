# VimSwitch

For an overview and installation steps visit [https://priomsrb.github.io/vimswitch/](https://priomsrb.github.io/vimswitch/).

## Requirements
Running VimSwitch only requires Python 2.7 or 3.2+. However, if you want to build and test VimSwitch you need to install its dependencies using `pip install -r requirements.txt`

## Testing
VimSwitch needs to support multiple Python versions over multiple operating systems. Therefore, it's important to maintain a high test coverage.

To run the test suite against the current Python version use `run_tests.sh` or `run_tests.bat`.

To run tests against all supported versions of Python use `tox`.
