
pushd %1 & for %%i in (.) do set curr=%%~ni
%cd%\Python3\python.exe Change.py
pause