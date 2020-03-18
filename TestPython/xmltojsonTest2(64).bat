cd ../
pushd %1 & for %%i in (.) do set curr=%%~ni
cd ../
D:\Python37\python.exe %~dp0\xmltojsonTest.py 2
pause