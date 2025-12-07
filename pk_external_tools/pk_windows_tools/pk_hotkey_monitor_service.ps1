# pk_system Hotkey Monitor Service (PowerShell)
# Windows 시작 프로그램으로 등록하여 백그라운드에서 단축키 모니터링

param(
    [string]$Hotkey = "ctrl+alt+p",
    [string]$ProjectPath = $env:d_pk_system
)

# 프로젝트 경로 설정
if (-not $ProjectPath) {
    $ProjectPath = "C:\Users\wjdgn\Downloads\pk_system"
}

# 작업 디렉토리 변경
Set-Location $ProjectPath

Write-Host "🎯 pk_system 단축키 모니터링 서비스 시작..." -ForegroundColor Cyan
Write-Host "💡 단축키: $Hotkey" -ForegroundColor Cyan
Write-Host "💡 종료하려면 Ctrl+C를 누르세요" -ForegroundColor Yellow
Write-Host ""

# Python virtual environment 경로
$PythonPath = Join-Path $ProjectPath ".venv\Scripts\python.exe"
$ScriptPath = Join-Path $ProjectPath "pk_internal_tools\pk_wrappers\pk_functions\ensure_hotkey_monitor_started.py"

# 스크립트 실행
try {
    & $PythonPath $ScriptPath $Hotkey
}
catch {
    Write-Host "❌ 모니터링 서비스 오류 발생: $_" -ForegroundColor Red
    Read-Host "계속하려면 Enter를 누르세요"
} 