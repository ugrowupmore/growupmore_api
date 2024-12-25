REM Activate the virtual environment
call venv\Scripts\activate

REM Check if the activation was successful
if errorlevel 1 (
    echo Failed to activate the virtual environment. Make sure it exists and try again.
    pause
    exit /b
)

REM Run the Django development server
echo Starting Django server...
python manage.py runserver

REM Keep the command prompt open to view output
pause