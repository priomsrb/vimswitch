@echo off
:loop
cls
nosetests --nocapture
pause
goto loop