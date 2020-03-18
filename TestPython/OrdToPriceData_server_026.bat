cd ../
pushd %1 & for %%i in (.) do set curr=%%~ni
cd ../
%cd%\%curr%\python.exe %~dp0\OrdToPriceData.py 0 026_qdsoft
pause