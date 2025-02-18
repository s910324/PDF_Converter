@echo off & title %~nx0 & color 5F

goto :DOES_PYTHON_EXIST

:DOES_PYTHON_EXIST
python -V | find /v "Python" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
python -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)
goto :EOF

:PYTHON_DOES_NOT_EXIST
echo Python is not installed on your system.
echo Now starts installation process.
winget install -e --id Python.Python.3.12
goto :INSTALL_DEPENDENCY

:PYTHON_DOES_EXIST
for /f "delims=" %%V in ('python -V') do @set ver=%%V
echo Python found, %ver% is installed...
goto :INSTALL_DEPENDENCY

:INSTALL_DEPENDENCY
echo Now starts install essential packages.
pip install -r ./requirements.txt
goto :EOF
