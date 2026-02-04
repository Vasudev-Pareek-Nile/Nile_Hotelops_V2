@echo off

REM Move from commands → management → PADP → project root
cd /d %~dp0\..\..\..

REM Run Django management command
python manage.py send_padp_notifications

pause
