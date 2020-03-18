cd ../
pushd %1 & for %%i in (.) do set curr=%%~ni
cd ../
%cd%\%curr%\python.exe %~dp0\xmltojsonTest.py 1 018_qdsoft
pause