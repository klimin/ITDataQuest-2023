cd c:\klimin\Python\DanQuest2023
set VIRTUAL_ENV=c:\klimin\Python\DanQuest2023\venv
set PATH=%VIRTUAL_ENV%\Scripts;%PATH%

set FLASK_APP=runner.py
set FLASK_ENV=development

flask run --host=0.0.0.0 --port=2023

rem python runner.py runserver --host=0.0.0.0 --port=5000