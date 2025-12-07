chcp 65001 >nul
title %~nx0
setlocal enabledelayedexpansion
set "SCRIPT_NAME=%~nx0"
git add .
git commit -m "make save point by !SCRIPT_NAME!"
git push
pause