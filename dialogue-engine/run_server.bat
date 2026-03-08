@echo off
setlocal

set ROOT=F:\dev-test\dialogue-engine
set PY=%ROOT%\.venv\Scripts\python.exe

if not exist "%PY%" (
  echo Missing venv. Run setup_env.bat first.
  exit /b 1
)

set PYTHONPATH=%ROOT%\src
"%PY%" "%ROOT%\main.py"

endlocal
