@echo off
:loop
cls

:: TEST_TYPE - Possible values:
:: BASIC = Runs all tests except the slow and external ones
:: ALL = Runs the basic and slow tests. Slow tests are those that create local
::   servers etc.
:: EXTERNAL = Runs only external test. These tests make use of resources
::   outside the local machine. For example downloading a file from github. 
::   Avoid running these tests frequently; we want to be nice to others :)
:: COVERAGE = Checks the test coverage after running ALL tests
set TEST_TYPE=ALL

echo %TEST_TYPE% TESTS
python --version

if "%TEST_TYPE%"=="BASIC" (
:: Add --nocapture to show stdout
nosetests -a "!slow,!external"
)
if "%TEST_TYPE%"=="ALL" (
nosetests -a "!external"
)
if "%TEST_TYPE%"=="EXTERNAL" (
nosetests -a "external"
)
 if "%TEST_TYPE%"=="COVERAGE" (
nosetests -a "!external" --with-coverage --cover-package=vimswitch --cover-branches
)

pause
goto loop
