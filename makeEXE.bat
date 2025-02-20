@echo off
pip install pyinstaller

pyinstaller --onedir --icon=icon.ico --windowed --name=YoutubeWTE main.py

echo.
echo.

echo "Now you can use Inno Setup to create Installer"
echo.
pause