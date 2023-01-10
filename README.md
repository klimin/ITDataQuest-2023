# Danone IT&Data Quest 2023
![IT&Data Quest 2023](app/static/img/title2023.png)

This quest was created «just for fun» and consists of 23 puzzles of various complexity. While some of the questions might sound complicated or technical, never give up, use your knowledge, or look up the answer on the internet. All of them can be solved without any hints, but the hints are available for the majority of questions. The time to complete the quest depends on your skills and can vary from a few minutes to a few days. The winner will be determined according to the elapsed time to complete all 23 questions.

# How to run
1. Install Python
2. Create virtual environment and install requirements
```
python -m venv venv
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Run in development mode:
```
run_Dev.bat
```
or run in Production mode
```
run_Prod.bat
```

# Useful links
- `http://<IT&Data Quest 2023 URL>/hiscore` — View Hall of fame (Hi Scores and progress, TOP-5 only)
- `http://<IT&Data Quest 2023 URL>/hiscore-all` — View Hall of fame (Hi Scores and progress)
- `http://<IT&Data Quest 2023 URL>/reset` — Clean current user session

# Folders
- `logs/*.log` — flask logs
- `data/danquest2023.db` — SQLite database file

# Run using Docker (optional)
```
sudo docker build -t danquest/danquest2023 .
docker run -d -p 2023:2023 danquest/danquest2023
```