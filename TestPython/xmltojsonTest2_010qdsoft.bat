cd ../
pushd %1 & for %%i in (.) do set curr=%%~ni
cd ../
%cd%\%curr%\python.exe %~dp0\xmltojsonTest.py 2 010_qdsoft
pause