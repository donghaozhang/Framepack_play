@echo off
echo Installing MoviePy and its dependencies...
echo.

:: Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Python found. Installing required packages...
echo.

:: Install MoviePy and dependencies
pip install --upgrade pip
pip install numpy
pip install decorator
pip install imageio
pip install imageio-ffmpeg
pip install proglog
pip install tqdm
pip install requests
pip install moviepy

:: Check if installation was successful
pip show moviepy > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: MoviePy installation failed.
    echo.
    pause
    exit /b 1
)

echo.
echo ======================================================
echo MoviePy has been successfully installed!
echo.
echo Now you can run combine_videos.py to properly combine
echo your videos with full MP4 support.
echo ======================================================
echo.
pause 