# 1줄 한방 커맨드 (관리자 권한 불필요)
$tmp = "$env:TEMP\ClickMonitorDDC.zip"; `
Invoke-WebRequest 'https://github.com/graealex/ClickMonitorDDC/raw/main/ClickMonitorDDC_7_2.zip' -OutFile $tmp; `
$inst = "$env:ProgramFiles\ClickMonitorDDC"; `
if (Test-Path $inst) { Remove-Item $inst -Recurse -Force }; `
Expand-Archive $tmp -DestinationPath $inst; `
$pp = [Environment]::GetEnvironmentVariable('Path','User'); `
if ($pp -notlike "*ClickMonitorDDC*") { `
  [Environment]::SetEnvironmentVariable('Path', "$pp;$inst", 'User') `
}; `
Write-Host "✅ 설치 완료! 터미널을 재시작한 뒤 아래로 확인하세요:`n  ClickMonitorDDC.exe /List"



