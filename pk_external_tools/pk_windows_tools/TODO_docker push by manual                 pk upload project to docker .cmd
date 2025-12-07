:: CONSOLE SETTING
title %~n0
color df
chcp 65001 >nul
@echo off
@rem @echo on
setlocal
for /f "delims=" %%i in ('Powershell.exe get-date -Format 'yyyy MM dd HH mm ss'') do set yyyyMMddHHmmss=%%i
cls


:: MINIMIZED WINDOW SETTING
:: if not "%minimized%"=="" goto :minimized
:: set minimized=true
:: start /min cmd /C "%~dpnx0"
:: goto :EOF
:: :minimized


:: pk_system/ubuntu_image
@REM docker run -d -p 8022:22 --name ubuntu_container ubuntu:latest --cgroupns=host
@REM docker run -d -p 8022:22 --name ubuntu_container ubuntu-image
@REM docker run -d -p 8022:22 --name ubuntu_container pk_system/ubuntu_image
@REM docker tag ubuntu-image pk_system/ubuntu_image
@REM docker push pk_system/ubuntu_image
@REM docker pull pk_system/ubuntu_image


:: pk_system/image_project_fastapi
docker build -t image_project_fastapi -f project_fastapi.Dockerfile .
docker tag image_project_fastapi pk_system/image_project_fastapi
docker push pk_system/image_project_fastapi
@REM sudo docker pull pk_system/image_project_fastapi:latest
@REM docker run --network pk_docker_network -d --name test_project_fastapi_container -p 8080:80 pk_system/image_project_fastapi
@REM docker commit test_project_fastapi_container pk_system/image_project_fastapi


:: pk_system/mysql_image
@REM docker commit mysql_container mysql:latest
@REM docker commit mysql_container pk_system/mysql_image
@REM docker tag mysql pk_system/mysql_image
@REM docker push pk_system/mysql_image
@REM docker pull pk_system/mysql_image
@REM docker run -d --network pk_docker_network --name mysql_container -p 3306:3306 -e MYSQL_ROOT_PASSWORD=admin123! -v /home/ubuntu/mysql/data:/var/lib/mysql -e MYSQL_PASSWORD=admin123! pk_system/mysql_image --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci



:: DEBUG SET UP
:: timeout 600