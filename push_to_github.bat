@echo off
set /p msg=Input commit message:
git add .
git commit -m "%msg%"
git push
echo.
echo All done!
pause