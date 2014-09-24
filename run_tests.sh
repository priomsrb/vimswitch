#!/bin/bash

# TEST_TYPE - Possible values:
# BASIC = Runs all tests except the slow and external ones
# ALL = Runs the basic and slow tests. Slow tests are those that create local
#   servers etc.
# EXTERNAL = Runs only external test. These tests make use of resources
#   outside the local machine. For example downloading a file from github. 
#   Avoid running these tests frequently; we want to be nice to others :)
# COVERAGE = Checks the test coverage after running ALL tests
TEST_TYPE=BASIC

while true; do
    clear
    echo $TEST_TYPE TESTS
    python --version

    case $TEST_TYPE in
    "BASIC")
        # Add --nocapture to show stdout
        nosetests -a "!slow,!external"
        ;;
    "ALL")
        nosetests -a "!external"
        ;;
    "EXTERNAL")
        nosetests -a "external"
        ;;
    "COVERAGE")
        nosetests -a "!external" --with-coverage --cover-package=vimswitch --cover-branches
        ;;
    esac

    read -p "Press Enter to continue..."
done
