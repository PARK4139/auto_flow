# PowerShell pk_system 별칭 문제 해결 도구
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Windows pk_system 별칭 문제 해결 도구" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host ""

# n. 현재 레지스트리 AutoRun 설정 확인
Write-Host "1. 현재 레지스트리 AutoRun 설정 확인:" -ForegroundColor Yellow
try {
    $autorun = Get-ItemProperty -Path "HKCU:\Software\Microsoft\Command Processor" -Name "AutoRun" -ErrorAction SilentlyContinue
    if ($autorun) {
        Write-Host "현재 AutoRun: $($autorun.AutoRun)" -ForegroundColor Green
    } else {
        Write-Host "AutoRun 설정이 없습니다." -ForegroundColor Red
    }
} catch {
    Write-Host "AutoRun 설정 확인 실패: $_" -ForegroundColor Red
}

Write-Host ""

# n. 기존 AutoRun 설정 제거
Write-Host "2. 기존 AutoRun 설정 제거:" -ForegroundColor Yellow
try {
    Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Command Processor" -Name "AutoRun" -Force -ErrorAction SilentlyContinue
    Write-Host "✅ 기존 AutoRun 설정 제거 완료" -ForegroundColor Green
} catch {
    Write-Host "⚠️ AutoRun 설정 제거 실패: $_" -ForegroundColor Yellow
}

Write-Host ""

# n. 새로운 배치 파일 기반 AutoRun 설정
Write-Host "3. 새로운 배치 파일 기반 AutoRun 설정:" -ForegroundColor Yellow
$pk_PATH = "C:\Users\wjdgn\Downloads\pk_system"
$BATCH_FILE = "$pk_PATH\pk_cache_private\pk_doskey.bat"

if (Test-Path $BATCH_FILE) {
    try {
        Set-ItemProperty -Path "HKCU:\Software\Microsoft\Command Processor" -Name "AutoRun" -Value "`"$BATCH_FILE`"" -Type String
        Write-Host "✅ 새로운 AutoRun 설정 완료: $BATCH_FILE" -ForegroundColor Green
    } catch {
        Write-Host "❌ AutoRun 설정 실패: $_" -ForegroundColor Red
    }
} else {
    Write-Host "❌ 배치 파일을 찾을 수 없습니다: $BATCH_FILE" -ForegroundColor Red
}

Write-Host ""

# n. 수동으로 별칭 등록 (PowerShell에서 CMD 별칭 설정)
Write-Host "4. 수동으로 별칭 등록:" -ForegroundColor Yellow
$aliases = @{
    "0" = "cd `"$pk_PATH`""
    "1" = "cd `"$pk_PATH\pk_external_tools`""
    "2" = "cd `"$pk_PATH\pk_os_layer_resources`""
    "3" = "cd `"$env:USERPROFILE\pk_working`""
    "4" = "cd `"$env:USERPROFILE\pk_memo`""
    "5" = "cd `"$env:USERPROFILE\business_flow`""
    "pk" = "python `"$pk_PATH\pk_internal_tools\pk_wrappers\pk_ensure_pk_enabled.py`""
    "venv" = "`"$pk_PATH\.venv\Scripts\activate`""
    "ls" = "dir"
    "cat" = "type"
    "which" = "where"
    "pwd" = "cd"
    "gpt" = "start https://chat.openai.com"
    "x" = "exit"
}

$successCount = 0
foreach ($alias in $aliases.GetEnumerator()) {
    try {
        $doskeyCmd = "doskey $($alias.Key)=$($alias.Value)"
        $result = cmd /c $doskeyCmd 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $($alias.Key) = $($alias.Value)" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "❌ $($alias.Key) 등록 실패" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ $($alias.Key) 등록 중 오류: $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📊 등록된 별칭: $successCount개" -ForegroundColor Cyan

Write-Host ""

# n. 등록된 별칭 확인
Write-Host "5. 등록된 별칭 확인:" -ForegroundColor Yellow
try {
    $macros = cmd /c "doskey /macros" 2>$null
    if ($macros) {
        Write-Host $macros -ForegroundColor Green
    } else {
        Write-Host "등록된 별칭이 없습니다." -ForegroundColor Red
    }
} catch {
    Write-Host "별칭 확인 실패: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "문제 해결 완료!" -ForegroundColor Green
Write-Host "새 CMD 창을 열어서 별칭이 작동하는지 확인하세요." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

Read-Host "엔터 키를 눌러 종료하세요" 