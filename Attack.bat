color 0A
setlocal
set workdir=%~dp0
echo off
if exist "%USERPROFILE%\Python\python.exe" (
	set PYTHONHOME=%USERPROFILE%\Python
	set PYTHONPATH=%USERPROFILE%\Python
)
PATH=%PATH%;%workdir%;%PYTHONPATH%;%ProgramFiles%\Git;%ProgramFiles%\Git\bin
@chcp 1251>nul
mode con: cols=110 lines=20
cls 

"%ProgramFiles%\Git\bin\git" checkout master
"%ProgramFiles%\Git\bin\git" pull

cls

python attack.py