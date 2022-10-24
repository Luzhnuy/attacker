color 0A
SETLOCAL EnableDelayedExpansion
set workdir=%~dp0
PATH=%PATH%;%workdir%;
@chcp 1251>nul
mode con: cols=88 lines=20
cls
echo off
:m1
Echo  #-----------------------------------------#-----------------------------------------# 
Echo  *                  Commands               *                  Êîìàíäè                *
Echo  #-----------------------------------------#-----------------------------------------#
Echo  *             Install tools               *  Âñòàíîâëåííÿ ³íñòðóìåíò³â ³ ñåðåäîâèùà *
Echo  *  Install Python          (step 1)     1 *  Âñòàíîâèòè Python            (Êðîê 1)  *
Echo  *  Install Git for Windows (step 2)     2 *  Âñòàíîâèòè Git               (Êðîê 2)  *
Echo  *  Get attacker repository (step 3)     3 *  Îòðèìàòè attacker            (Êðîê 3)  *
Echo  #-----------------------------------------#-----------------------------------------# 
Echo.
Set /p choice="Your choice (Âàø âèá³ð): "

if "%choice%"=="1" (
	if not exist "%systemdrive%\Program Files (x86)" (
		%workdir%\resources\wget https://www.python.org/ftp/python/3.8.7/python-3.8.7.exe -O "%TMP%\python.exe"
	) else (
		%workdir%\resources\wget https://www.python.org/ftp/python/3.8.7/python-3.8.7-amd64.exe -O "%TMP%\python.exe"
	)
	
	%TMP%\python.exe /passive InstallAllUsers=0 PrependPath=1 Include_pip=1 Include_launcher=1 AssociateFiles=1 TargetDir=%USERPROFILE%\Python
	if exist "%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\python.exe" (
		del %USERPROFILE%\AppData\Local\Microsoft\WindowsApps\python.exe
		del %USERPROFILE%\AppData\Local\Microsoft\WindowsApps\python3.exe
		del %USERPROFILE%\AppData\Local\Microsoft\WindowsApps\pip.exe
		mklink %USERPROFILE%\AppData\Local\Microsoft\WindowsApps\python.exe %USERPROFILE%\Python\python.exe
		mklink %USERPROFILE%\AppData\Local\Microsoft\WindowsApps\python3.exe %USERPROFILE%\Python\python.exe
		mklink %USERPROFILE%\AppData\Local\Microsoft\WindowsApps\pip.exe %USERPROFILE%\Python\Scripts\pip.exe
		mklink %USERPROFILE%\AppData\Local\Microsoft\WindowsApps\pip3.exe %USERPROFILE%\Python\Scripts\pip.exe
	)
	if exist "%USERPROFILE%\Python\python.exe" (
		mklink %USERPROFILE%\Python\python3.exe %USERPROFILE%\Python\python.exe
		mklink %USERPROFILE%\Python\Scripts\pip3.exe %USERPROFILE%\Python\Scripts\pip.exe
		set PYTHONHOME=%USERPROFILE%\Python
		set PYTHONPATH=%USERPROFILE%\Python
	)
)


if "%choice%"=="2" (
	if not exist "%systemdrive%\Program Files (x86)" (
		%workdir%\resources\wget https://github.com/git-for-windows/git/releases/download/v2.30.0.windows.2/Git-2.30.0.2-32-bit.exe -O %TMP%\git.exe
	) else (
		%workdir%\resources\wget https://github.com/git-for-windows/git/releases/download/v2.30.0.windows.2/Git-2.30.0.2-64-bit.exe -O %TMP%\git.exe
	)
	
	%TMP%\git.exe /SILENT
	del %TMP%\git.exe
)

if "%choice%"=="3" (
	Set /p diskInstal="Enter a drive letter C,D etc. (Ââåäèòå áóêâó äèñêà C,D è ò.ï): "
	rem echo  test !%diskInstal!
	if not exist "!diskInstal!:\" (
		echo Disk letter is wrong!
		pause
		cls
		goto m1

	) else (
		echo "Firmware repo wil be instaled on disk !diskInstal!:"
		!diskInstal!:
		if exist "!diskInstal!:\Attacker" (rmdir /S /Q !diskInstal!:\Attacker)
		"%ProgramFiles%\Git\bin\git" clone https://github.com/Luzhnuy/attacker.git
		pip install -r requirements.txt
		start .\Attacker
	)
)


pause

cls
goto m1
