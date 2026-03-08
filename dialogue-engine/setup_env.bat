@echo off
setlocal

set ROOT=F:\dev-test\dialogue-engine
set PY=C:\Users\charl\AppData\Local\Programs\Python\Python312\python.exe

if not exist "%PY%" (
  echo Python not found at %PY%
  exit /b 1
)

%PY% -m venv "%ROOT%\.venv"
"%ROOT%\.venv\Scripts\python.exe" -m pip install --upgrade pip
"%ROOT%\.venv\Scripts\python.exe" -m pip install -r "%ROOT%\requirements.txt"

echo Environment is ready.
endlocal
