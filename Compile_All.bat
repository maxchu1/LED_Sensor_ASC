@echo off
REM This file must be saved as ANSI/Big5
:: =============================================================================
:: pyinstaller參數
:: -D , --onedir 預測的打包模式，會在dist資料夾中打包成多個文件
:: -F , --onefile 打包成單一個執行檔
:: -n 產生執行檔的名字
:: -w , --windowed , --noconsole 打包時會去除命令視窗
:: -i icon.ico 改變程式的圖標
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
