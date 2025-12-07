# PowerShell 스크립트: 바탕화면과 현재 위치에 .lnk 바로가기 생성
# 저장 인코딩은 UTF-8 with BOM
try {
    # pk_system 루트 디렉토리 경로 설정
    $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)

    Write-Host "[🔧정보] 스크립트 디렉토리: $ScriptDir" -ForegroundColor Cyan
    Write-Host "[🔧정보] 프로젝트 루트: $ProjectRoot" -ForegroundColor Cyan

    $TargetCmd = "$ProjectRoot\run.cmd"
    $ShortcutName = "pk_launcher"
    $IconPath = "$env:SystemRoot\System32\shell32.dll,40"

    # 대상 파일 존재 확인
    if (-not (Test-Path $TargetCmd)) {
        Write-Host "⚠️ 대상 파일을 찾을 수 없음: $TargetCmd" -ForegroundColor Yellow
        Write-Host "⚠️ 스크립트를 pk_system 루트 디렉토리에서 실행하세요." -ForegroundColor Yellow
        Write-Host "[🔧정보] 현재 작업 디렉토리: $(Get-Location)" -ForegroundColor Yellow
        Write-Host "[🔧정보] 프로젝트 루트 존재 여부: $(Test-Path $ProjectRoot)" -ForegroundColor Yellow
        [void][System.Console]::ReadLine()
        exit 1
    }

    Write-Host "[🔧성공] 대상 파일 확인됨: $TargetCmd" -ForegroundColor Cyan

    $ShortcutPaths = @(
        "$env:USERPROFILE\Desktop\$ShortcutName.lnk"
    )

    # 1단계: 작업표시줄에서 기존 고정 제거
    Write-Host "[🔧정보] 1단계: 작업표시줄에서 기존 pk_launcher 제거 중..." -ForegroundColor Cyan
    try {
        # 작업표시줄에서 고정 해제 시도
        $shell = New-Object -ComObject Shell.Application
        $folder = $shell.Namespace(0x1)  # Desktop
        $items = $folder.Items()
        
        $found = $false
        foreach ($item in $items) {
            if ($item.Name -like "*pk_launcher*") {
                Write-Host "[🔧정보] 작업표시줄에서 찾음: $($item.Name)" -ForegroundColor Yellow
                try {
                    $item.InvokeVerb("unpinfromtaskbar")
                    Write-Host "[🔧성공] 작업표시줄에서 고정 해제 완료" -ForegroundColor Cyan
                    $found = $true
                    break
                } catch {
                    Write-Host "⚠️ 고정 해제 실패: $($_.Exception.Message)" -ForegroundColor Yellow
                }
            }
        }
        
        if (-not $found) {
            Write-Host "⚠️ 작업표시줄에서 pk_launcher를 찾을 수 없음" -ForegroundColor Cyan
        }
    } catch {
        Write-Host "⚠️ 작업표시줄 제거 중 오류: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    # 잠시 대기 (작업표시줄 변경사항 반영)
    Start-Sleep -Seconds 1
    
    # 2단계: 바로가기 생성
    Write-Host "[🔧정보] 2단계: 바로가기 생성 중..." -ForegroundColor Cyan
    foreach ($ShortcutPath in $ShortcutPaths) {
        try {
            # 기존 바로가기가 있으면 삭제
            if (Test-Path $ShortcutPath) {
                Remove-Item $ShortcutPath -Force
                Write-Host "⚠️ 기존 바로가기 제거됨: $ShortcutPath" -ForegroundColor Yellow
            }

            $WshShell = New-Object -ComObject WScript.Shell
            if (-not $WshShell) {
                throw "WScript.Shell COM 객체 생성 실패"
            }

            $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
            $Shortcut.TargetPath = "cmd.exe"
            $Shortcut.Arguments = "/c `"$TargetCmd`""
            $Shortcut.IconLocation = $IconPath
            $Shortcut.WindowStyle = 1
            $Shortcut.Save()
            
            Write-Host "[🔧성공] 바로가기 생성됨: $ShortcutPath" -ForegroundColor Cyan
        }
        catch {
            Write-Host "⚠️ 바로가기 생성 실패: $($_.Exception.Message)" -ForegroundColor Yellow
            Write-Host "⚠️ 관리자 권한으로 실행해보세요." -ForegroundColor Yellow
        }
    }
}
catch {
    Write-Host "⚠️ 스크립트 실행 실패: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "⚠️ 오류 상세: $($_.Exception.GetType().Name)" -ForegroundColor Yellow
}
finally {
    # COM 객체 정리
    if ($WshShell) {
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($WshShell) | Out-Null
    }
}
Write-Host "🔧 바로가기 생성이 완료되었습니다!" -ForegroundColor Cyan
Write-Host ""
Write-Host ""
Write-Host "⚠️ [작업표시줄 고정]은 수동으로 진행해 주세요:" -ForegroundColor Yellow
Write-Host "1. 바탕화면 바로가기 우클릭 → [작업 표시줄에 고정]" -ForegroundColor Yellow
Write-Host "2. 작업표시줄 왼쪽에 둘 경우 → Win + 1 단축키 가능" -ForegroundColor Yellow
Write-Host ""
Write-Host ""
Write-Host ""
Write-Host "⚠️ 바탕화면 바로가기 생성 결과를 확인하세요." -ForegroundColor Yellow

try {
    # PowerShell에서 더 안정적인 키 입력 방법
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} catch {
    Write-Host "키 입력이 실패했습니다. 다른 방법을 시도합니다..." -ForegroundColor Yellow
    try {
        # 대체 방법 1: Read-Host 사용
        Read-Host "아무 키나 누르고 Enter를 누르세요"
    } catch {
        Write-Host "대체 방법도 실패했습니다. 창을 수동으로 닫아주세요." -ForegroundColor Yellow
        Write-Host "창을 닫으려면 이 창의 X 버튼을 클릭하세요." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    }
}
exit 0