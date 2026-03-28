@echo off
git add -A
git status
set /p MSG=commit message:
git commit -m "%MSG%"
git push origin main
pause
