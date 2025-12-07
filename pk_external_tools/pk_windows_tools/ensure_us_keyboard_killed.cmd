chcp 65001

@echo off
REM ================================
REM Batch script to apply Globalization Services settings
REM ================================

REM 설정을 적용할 임시 XML 파일 경로 설정
SET "XMLFile=%TEMP%\Remove_en-US.xml"

REM XML 내용 작성
> "%XMLFile%" (
    echo ^<gs:GlobalizationServices xmlns:gs="urn:longhornGlobalizationUnattend"^>
    echo.
    echo     ^<!--User List--^>
    echo     ^<gs:UserList^>
    echo         ^<gs:User UserID="Current"/^>
    echo     ^</gs:UserList^>
    echo.
    echo     ^<!--input preferences--^> 
    echo     ^<gs:InputPreferences^>
    echo         ^<!--add en-US keyboard input--^>
    echo         ^<gs:InputLanguageID Action="add" ID="0409:00000409"/^>
    echo         ^<!--remove en-US keyboard input--^>
    echo         ^<gs:InputLanguageID Action="remove" ID="0409:00000409"/^>
    echo     ^</gs:InputPreferences^>
    echo.
    echo ^</gs:GlobalizationServices^>
)

REM 현재 배치 파일의 디렉토리 경로 가져오기 (필요 시)
FOR /F "delims=" %%I IN ("%~dp0") DO SET "CURRENTDIR=%%I"

REM intl.cpl 제어판을 통해 XML 설정 적용
control intl.cpl,, /f:"%XMLFile%"

REM 임시 XML 파일 삭제 (원하지 않으면 이 줄을 제거하세요)
del "%XMLFile%"

echo 설정이 성공적으로 적용되었습니다.
timeout 60
