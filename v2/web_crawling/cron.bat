@echo off
schtasks /create /tn "MoviePreviewAlarm_morning" /tr "C:\Users\yhsoo\Documents\moviePreviewAlarm\v2\web_crawling\.venv\Scripts\python.exe C:\Users\yhsoo\Documents\moviePreviewAlarm\v2\web_crawling\main.py" /sc daily /st 09:00
schtasks /create /tn "MoviePreviewAlarm_afternoon" /tr "C:\Users\yhsoo\Documents\moviePreviewAlarm\v2\web_crawling\.venv\Scripts\python.exe C:\Users\yhsoo\Documents\moviePreviewAlarm\v2\web_crawling\main.py" /sc daily /st 14:00
echo Tasks have been registered successfully!
pause
