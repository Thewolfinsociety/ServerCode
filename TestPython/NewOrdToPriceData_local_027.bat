cd ../
pushd %1 & for %%i in (.) do set curr=%%~ni
cd ../
%cd%\%curr%\python.exe %~dp0\NewOrdToPriceData.py 1 027_qdsoft
pause