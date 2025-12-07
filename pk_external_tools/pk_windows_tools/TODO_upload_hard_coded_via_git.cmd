chcp 65001
title %~nx0
@echo off
cls



git add *
git commit -m "gitignore test commit"
git push origin main

git status
:: cmd /k
timeout 60