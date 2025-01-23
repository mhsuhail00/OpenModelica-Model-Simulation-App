@echo off
SET PATH=;C:/Program Files/OpenModelica1.24.3-64bit/bin/;%PATH%;
SET ERRORLEVEL=
CALL "%CD%/RLC1.exe" %*
SET RESULT=%ERRORLEVEL%

EXIT /b %RESULT%
