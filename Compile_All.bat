@echo off
REM This file must be saved as ANSI/Big5
:: =============================================================================
:: pyinstaller�Ѽ�
:: -D , --onedir �w�������]�Ҧ��A�|�bdist��Ƨ������]���h�Ӥ��
:: -F , --onefile ���]����@�Ӱ�����
:: -n ���Ͱ����ɪ��W�r
:: -w , --windowed , --noconsole ���]�ɷ|�h���R�O����
:: -i icon.ico ���ܵ{�����ϼ�
:: =============================================================================
set FileName=LED_Sensor_ASC
echo Compile %FileName%.py to %FileName%.exe ...
pyinstaller --clean Settings.spec
if errorlevel==1 goto End1

:DeleteStep2
if not exist Build goto DeleteStep3
echo Remove Build Directory...
rd /s /q Build

:DeleteStep3
if not exist __pycache__ goto MoveFile
echo Remove __pycache__ Directory...
rd /s /q __pycache__

:MoveFile
::if not exist dist\%FileName%.exe goto End1
::move dist\%FileName%.exe .
::rd dist
goto End2

:End1
Echo Error: Create Execute File Fail....

:End2
pause
