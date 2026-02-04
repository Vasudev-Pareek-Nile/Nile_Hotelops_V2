@echo off
call C:\virtualenvs\Eric\Scripts\activate
cd C:\pythonproject\HotelOpsPythonHosting
python manage.py GenerateWeekoff
deactivate