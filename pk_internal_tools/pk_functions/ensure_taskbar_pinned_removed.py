"""
윈도우 작업표시줄에서 고정된 프로그램을 제거하는 함수들
"""
import subprocess
import time
from typing import List, Optional

from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
from pk_internal_tools.pk_functions.is_os_windows_11 import is_os_windows_11


def ensure_taskbar_pinned_removed(shortcut_name: str = "pk_launcher") -> bool:
    """
    윈도우 작업표시줄에서 고정된 바로가기를 자동으로 제거합니다.
    
    Windows에서 작업표시줄 바로가기 자동 제거는 다음 방법들을 순차적으로 시도합니다:
    1. 직접 파일 삭제: 작업표시줄 고정 폴더에서 바로가기 파일 직접 삭제 (가장 확실)
    2. Shell COM 객체: Windows Shell COM을 통한 unpinfromtaskbar 호출
    3. PowerShell 명령어: PowerShell을 통한 고정 해제
    4. 레지스트리 수정: 레지스트리를 통한 간접 제거
    5. Taskbar API: Windows API를 통한 Explorer 재시작
    
    Args:
        shortcut_name: 제거할 바로가기 이름 (예: "pk_launcher")
                      번호가 붙은 변형도 자동 처리 (예: "pk_launcher (1)", "pk_launcher (2)")
    
    Returns:
        bool: 제거 성공 여부
    
    Examples:
        >>> ensure_taskbar_pinned_removed("pk_launcher")
        True  # 제거 성공
        
        >>> ensure_taskbar_pinned_removed("my_app")
        True  # "my_app", "my_app (1)" 등 모두 제거
    """
    YELLOW = PK_ANSI_COLOR_MAP.get("YELLOW", "")
    RESET = PK_ANSI_COLOR_MAP.get("RESET", "")
    
    # Windows 버전 확인 및 출력
    is_win11 = is_os_windows_11()
    windows_version = "Windows 11" if is_win11 else "Windows 10"
    print(f"{YELLOW}# Windows 버전 감지: {windows_version}{RESET}")
    
    # 디버깅: 작업표시줄에 있는 모든 바로가기 목록 확인
    _debug_list_taskbar_shortcuts(shortcut_name)
    
    # Windows 버전에 따라 최적화된 방법 순서 결정
    if is_win11:
        # Win11: Shell COM과 PowerShell을 우선 시도 (Taskband blob 때문에 파일 삭제가 덜 효과적)
        methods = [
            _remove_via_shell_com,              # Win11: Shell COM 우선
            _remove_via_powershell_commands,    # Win11: PowerShell 명령어
            _remove_via_registry,               # Win11: Taskband 레지스트리 확인
            _remove_via_direct_file_deletion,   # Win11: 파일 삭제 (일부 환경에서만 동작)
            _remove_via_taskbar_api             # Win11: Explorer 재시작
        ]
    else:
        # Win10: 파일 직접 삭제가 가장 확실
        methods = [
            _remove_via_direct_file_deletion,  # Win10: 가장 직접적이고 확실한 방법
            _remove_via_shell_com,              # Win10: Shell COM 객체 사용
            _remove_via_powershell_commands,    # Win10: PowerShell 명령어
            _remove_via_registry,               # Win10: 레지스트리
            _remove_via_taskbar_api             # Win10: Windows API (Explorer 재시작)
        ]
    
    for i, method in enumerate(methods, 1):
        try:
            print(f"{YELLOW}방법 {i}: {method.__name__} 시도 중...{RESET}")
            if method(shortcut_name):
                print(f"{YELLOW}✅ 방법 {i}로 제거 성공: {shortcut_name}{RESET}")
                return True
        except Exception as e:
            print(f"{YELLOW}⚠️ 방법 {i} 실패: {e}{RESET}")
            continue
    
    print(f"{YELLOW}⚠️ 모든 방법으로 제거 실패: {shortcut_name}{RESET}")
    print(f"{YELLOW}💡 참고: 작업표시줄에 해당 바로가기가 실제로 고정되어 있지 않을 수 있습니다.{RESET}")
    return False


def _remove_via_direct_file_deletion(shortcut_name: str) -> bool:
    r"""
    작업표시줄 고정 폴더에서 바로가기 파일을 직접 삭제하는 방법 (Win10 기준, 가장 확실)
    
    Win10: C:\Users\<USER>\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar
    Win11: 일부 설정 유지된 환경에서도 동작하지만, 새 Taskbar 구조에서는 완전히 안 먹히는 경우가 있음
    """
    ps_command = f"""
    try {{
        $baseName = "{shortcut_name}"
        $taskbarPath = "$env:APPDATA\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar"
        
        if (-not (Test-Path $taskbarPath)) {{
            Write-Host "작업표시줄 폴더가 존재하지 않음: $taskbarPath"
            return $false
        }}
        
        $removedCount = 0
        $allShortcuts = Get-ChildItem -Path $taskbarPath -ErrorAction SilentlyContinue
        
        foreach ($shortcut in $allShortcuts) {{
            $name = $shortcut.Name -replace '\\.lnk$', ''
            # 기본 이름으로 시작하는 모든 변형 찾기 (괄호와 숫자 포함)
            if ($name -match "^$([regex]::Escape($baseName))($|\\s*\\(\\d+\\)$)") {{
                Write-Host "작업표시줄 바로가기 발견: $($shortcut.Name)"
                try {{
                    # 먼저 unpin 시도
                    try {{
                        $shell = New-Object -ComObject Shell.Application
                        $folder = $shell.Namespace($taskbarPath)
                        $item = $folder.ParseName($shortcut.Name)
                        if ($item) {{
                            $item.InvokeVerb("unpinfromtaskbar")
                            Write-Host "고정 해제 시도 완료: $($shortcut.Name)"
                            Start-Sleep -Milliseconds 500
                        }}
                    }} catch {{
                        Write-Host "고정 해제 시도 실패 (무시하고 파일 삭제 진행): $($_.Exception.Message)"
                    }}
                    
                    # 바로가기 파일 직접 삭제
                    Remove-Item $shortcut.FullName -Force -ErrorAction Stop
                    Write-Host "바로가기 파일 삭제 성공: $($shortcut.Name)"
                    $removedCount++
                }} catch {{
                    Write-Host "파일 삭제 실패: $($_.Exception.Message)"
                }}
            }}
        }}
        
        if ($removedCount -gt 0) {{
            Write-Host "총 $removedCount 개의 바로가기 파일 삭제 완료"
            # Explorer 새로고침
            try {{
                $explorer = Get-Process explorer -ErrorAction SilentlyContinue
                if ($explorer) {{
                    Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
                    Start-Sleep -Seconds 1
                    Start-Process explorer
                    Write-Host "Explorer 재시작으로 작업표시줄 새로고침 완료"
                }}
            }} catch {{
                Write-Host "Explorer 재시작 실패 (무시): $($_.Exception.Message)"
            }}
            return $true
        }}
        
        Write-Host "작업표시줄에서 해당 이름의 바로가기를 찾을 수 없음"
        return $false
    }} catch {{
        Write-Host "직접 삭제 오류: $($_.Exception.Message)"
        return $false
    }}
    """
    
    result = _run_powershell(ps_command)
    return result and ("삭제 성공" in result or "삭제 완료" in result)


def _remove_via_shell_com(shortcut_name: str) -> bool:
    """Shell COM 객체를 사용하여 작업표시줄에서 제거 - 번호가 붙은 변형도 처리"""
    ps_command = f"""
    try {{
        # 패턴: pk_launcher, pk_launcher (1), pk_launcher (2) 등 모두 찾기
        $baseName = "{shortcut_name}"
        $patterns = @(
            "$baseName",
            "$baseName *",
            "$baseName (*)"
        )
        
        # 방법 1: 작업표시줄 고정 폴더에서 직접 찾기
        $taskbarPath = "$env:APPDATA\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar"
        if (Test-Path $taskbarPath) {{
            $allShortcuts = Get-ChildItem -Path $taskbarPath -ErrorAction SilentlyContinue
            foreach ($shortcut in $allShortcuts) {{
                $name = $shortcut.Name -replace '\\.lnk$', ''
                # 기본 이름으로 시작하는 모든 변형 찾기 (괄호 포함)
                if ($name -match "^$([regex]::Escape($baseName))($|\\s*\\(\\d+\\)$)") {{
                    Write-Host "작업표시줄 폴더에서 찾음: $($shortcut.Name)"
                    try {{
                        $shell = New-Object -ComObject Shell.Application
                        $folder = $shell.Namespace($taskbarPath)
                        $item = $folder.ParseName($shortcut.Name)
                        if ($item) {{
                            $item.InvokeVerb("unpinfromtaskbar")
                            Write-Host "작업표시줄 폴더에서 제거 성공: $($shortcut.Name)"
                            # 바로가기 파일도 삭제
                            try {{
                                Remove-Item $shortcut.FullName -Force -ErrorAction SilentlyContinue
                                Write-Host "바로가기 파일 삭제 완료"
                            }} catch {{
                                Write-Host "파일 삭제 실패 (무시)"
                            }}
                        }}
                    }} catch {{
                        Write-Host "작업표시줄 폴더 제거 실패: $($_.Exception.Message)"
                    }}
                }}
            }}
        }}
        
        # 방법 2: 바탕화면에서 찾기
        $shell = New-Object -ComObject Shell.Application
        $folder = $shell.Namespace(0x1)  # Desktop
        $items = $folder.Items()
        
        foreach ($item in $items) {{
            $name = $item.Name -replace '\\.lnk$', ''
            if ($name -match "^$([regex]::Escape($baseName))($|\\s*\\(\\d+\\)$)") {{
                Write-Host "바탕화면에서 찾음: $($item.Name)"
                try {{
                    $item.InvokeVerb("unpinfromtaskbar")
                    Write-Host "바탕화면에서 제거 성공: $($item.Name)"
                    return $true
                }} catch {{
                    Write-Host "바탕화면 제거 실패: $($_.Exception.Message)"
                }}
            }}
        }}
        
        # 방법 3: 시작 메뉴에서 찾기
        $startMenuPath = "$env:APPDATA\\Microsoft\\Windows\\Start Menu\\Programs"
        if (Test-Path $startMenuPath) {{
            $allShortcuts = Get-ChildItem -Path $startMenuPath -Recurse -ErrorAction SilentlyContinue
            foreach ($shortcut in $allShortcuts) {{
                $name = $shortcut.Name -replace '\\.lnk$', ''
                if ($name -match "^$([regex]::Escape($baseName))($|\\s*\\(\\d+\\)$)") {{
                    Write-Host "시작 메뉴에서 찾음: $($shortcut.FullName)"
                    try {{
                        $shell = New-Object -ComObject Shell.Application
                        $folder = $shell.Namespace($shortcut.DirectoryName)
                        $item = $folder.ParseName($shortcut.Name)
                        if ($item) {{
                            $item.InvokeVerb("unpinfromtaskbar")
                            Write-Host "시작 메뉴에서 제거 성공: $($shortcut.Name)"
                            return $true
                        }}
                    }} catch {{
                        Write-Host "시작 메뉴 제거 실패: $($_.Exception.Message)"
                    }}
                }}
            }}
        }}
        
        return $false
    }} catch {{
        Write-Host "Shell COM 오류: $($_.Exception.Message)"
        return $false
    }}
    """
    
    result = _run_powershell(ps_command)
    return result and ("제거 성공" in result or "작업표시줄 폴더에서 제거 성공" in result)


def _remove_via_powershell_commands(shortcut_name: str) -> bool:
    """PowerShell 명령어를 사용하여 작업표시줄에서 제거 - 번호가 붙은 변형도 처리"""
    ps_command = f"""
    try {{
        $baseName = "{shortcut_name}"
        $removedCount = 0
        
        # 작업표시줄 고정 폴더에서 직접 찾기 (모든 변형)
        $taskbarPath = "$env:APPDATA\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar"
        if (Test-Path $taskbarPath) {{
            $allShortcuts = Get-ChildItem -Path $taskbarPath -ErrorAction SilentlyContinue
            foreach ($shortcut in $allShortcuts) {{
                $name = $shortcut.Name -replace '\\.lnk$', ''
                # 기본 이름으로 시작하는 모든 변형 찾기 (괄호와 숫자 포함)
                if ($name -match "^$([regex]::Escape($baseName))($|\\s*\\(\\d+\\)$)") {{
                    Write-Host "작업표시줄 바로가기 발견: $($shortcut.Name)"
                    try {{
                        $shell = New-Object -ComObject Shell.Application
                        $folder = $shell.Namespace($taskbarPath)
                        $item = $folder.ParseName($shortcut.Name)
                        
                        if ($item) {{
                            # 모든 동사(verbs) 확인
                            $verbs = $item.Verbs()
                            $foundUnpin = $false
                            foreach ($verb in $verbs) {{
                                $verbName = $verb.Name
                                Write-Host "동사 확인: $verbName"
                                # 영어/한국어 모두 확인
                                if ($verbName -match "unpin|고정.*해제|작업.*표시줄.*제거") {{
                                    Write-Host "고정 해제 동사 발견: $verbName"
                                    try {{
                                        $verb.DoIt()
                                        Write-Host "고정 해제 완료: $($shortcut.Name)"
                                        $foundUnpin = $true
                                        $removedCount++
                                        break
                                    }} catch {{
                                        Write-Host "동사 실행 실패: $($_.Exception.Message)"
                                    }}
                                }}
                            }}
                            
                            if (-not $foundUnpin) {{
                                # 직접 unpinfromtaskbar 시도
                                try {{
                                    $item.InvokeVerb("unpinfromtaskbar")
                                    Write-Host "직접 unpinfromtaskbar 호출 성공: $($shortcut.Name)"
                                    $foundUnpin = $true
                                    $removedCount++
                                }} catch {{
                                    Write-Host "직접 호출 실패: $($_.Exception.Message)"
                                }}
                            }}
                            
                            if ($foundUnpin) {{
                                # 바로가기 파일 삭제
                                try {{
                                    Remove-Item $shortcut.FullName -Force -ErrorAction SilentlyContinue
                                    Write-Host "바로가기 파일 삭제 완료: $($shortcut.Name)"
                                }} catch {{
                                    Write-Host "파일 삭제 실패 (무시): $($_.Exception.Message)"
                                }}
                            }}
                        }}
                    }} catch {{
                        Write-Host "처리 실패: $($_.Exception.Message)"
                    }}
                }}
            }}
        }}
        
        # 바탕화면에서도 시도 (모든 변형)
        $desktop = [Environment]::GetFolderPath("Desktop")
        $allDesktopShortcuts = Get-ChildItem -Path $desktop -ErrorAction SilentlyContinue
        foreach ($shortcut in $allDesktopShortcuts) {{
            $name = $shortcut.Name -replace '\\.lnk$', ''
            if ($name -match "^$([regex]::Escape($baseName))($|\\s*\\(\\d+\\)$)") {{
                Write-Host "바탕화면 바로가기 발견: $($shortcut.Name)"
                try {{
                    $shell = New-Object -ComObject Shell.Application
                    $folder = $shell.Namespace(0x1)
                    $item = $folder.ParseName($shortcut.Name)
                    
                    if ($item) {{
                        try {{
                            $item.InvokeVerb("unpinfromtaskbar")
                            Write-Host "바탕화면에서 고정 해제 완료: $($shortcut.Name)"
                            $removedCount++
                        }} catch {{
                            Write-Host "바탕화면 고정 해제 실패: $($_.Exception.Message)"
                        }}
                    }}
                }} catch {{
                    Write-Host "바탕화면 처리 실패: $($_.Exception.Message)"
                }}
            }}
        }}
        
        if ($removedCount -gt 0) {{
            Write-Host "총 $removedCount 개의 바로가기 제거 완료"
            return $true
        }}
        
        return $false
    }} catch {{
        Write-Host "PowerShell 명령어 오류: $($_.Exception.Message)"
        return $false
    }}
    """
    
    result = _run_powershell(ps_command)
    return result and ("고정 해제 완료" in result or "unpinfromtaskbar 호출 성공" in result or "제거 성공" in result or "총" in result)


def _remove_via_registry(shortcut_name: str) -> bool:
    r"""
    레지스트리를 통해 작업표시줄 설정 확인 및 수정
    
    Win10: 파일 기반 (.lnk 파일 직접 삭제)
    Win11: HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Taskband (바이너리 blob)
          - Win11의 Taskband는 바이너리 blob이라 직접 파싱/수정이 거의 불가능
          - 이 방법은 주로 확인용으로 사용
    """
    ps_command = f"""
    try {{
        # Win10: 작업표시줄 관련 레지스트리 키들 확인
        $regKeys = @(
            "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\People",
            "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\Taskbar",
            "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\TaskbarDa"
        )
        
        foreach ($regKey in $regKeys) {{
            if (Test-Path $regKey) {{
                $properties = Get-ItemProperty -Path $regKey -ErrorAction SilentlyContinue
                Write-Host "레지스트리 키 확인: $regKey"
                foreach ($prop in $properties.PSObject.Properties) {{
                    if ($prop.Name -notlike "PS*") {{
                        Write-Host "  $($prop.Name): $($prop.Value)"
                    }}
                }}
            }}
        }}
        
        # Win11: Taskband 레지스트리 확인 (바이너리 blob - 직접 수정 불가)
        $taskbandKey = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Taskband"
        if (Test-Path $taskbandKey) {{
            Write-Host "Win11 Taskband 레지스트리 발견 (바이너리 blob - 직접 수정 불가)"
            $taskband = Get-ItemProperty -Path $taskbandKey -ErrorAction SilentlyContinue
            if ($taskband) {{
                Write-Host "Taskband 데이터 존재 (크기: $($taskband.PSObject.Properties.Count) 속성)"
                # Win11에서는 Taskband blob을 직접 수정할 수 없으므로
                # Explorer 재시작으로 간접적으로 새로고침 시도
                try {{
                    $explorer = Get-Process explorer -ErrorAction SilentlyContinue
                    if ($explorer) {{
                        Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
                        Start-Sleep -Seconds 1
                        Start-Process explorer
                        Write-Host "Win11 Taskband: Explorer 재시작으로 새로고침 시도"
                        return $true
                    }}
                }} catch {{
                    Write-Host "Explorer 재시작 실패: $($_.Exception.Message)"
                }}
            }}
        }}
        
        # Win10: 작업표시줄 고정 해제를 위한 레지스트리 수정 시도
        try {{
            $taskbarKey = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\Taskbar"
            if (Test-Path $taskbarKey) {{
                # People Band 비활성화 시도
                Set-ItemProperty -Path $taskbarKey -Name "PeopleBand" -Value 0 -ErrorAction SilentlyContinue
                Write-Host "People Band 비활성화 시도 완료"
            }}
        }} catch {{
            Write-Host "레지스트리 수정 실패: $($_.Exception.Message)"
        }}
        
        return $false
    }} catch {{
        Write-Host "레지스트리 확인 오류: $($_.Exception.Message)"
        return $false
    }}
    """
    
    result = _run_powershell(ps_command)
    return result and ("People Band 비활성화 시도 완료" in result or "Explorer 재시작" in result or "새로고침 시도" in result)


def _remove_via_taskbar_api(shortcut_name: str) -> bool:
    """Windows API를 사용하여 작업표시줄에서 제거"""
    ps_command = f"""
    try {{
        # Windows 10/11 작업표시줄 API 사용 시도
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        
        public class TaskbarHelper {{
            [DllImport("user32.dll")]
            public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
            
            [DllImport("user32.dll")]
            public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
            
            [DllImport("user32.dll")]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
        }}
"@
        
        Write-Host "Windows API 로드 완료"
        
        # 작업표시줄 창 찾기
        $taskbar = [TaskbarHelper]::FindWindow("Shell_TrayWnd", $null)
        if ($taskbar -ne [IntPtr]::Zero) {{
            Write-Host "작업표시줄 창 발견: $taskbar"
            
            # 작업표시줄 새로고침 시도
            try {{
                $explorer = Get-Process explorer -ErrorAction SilentlyContinue
                if ($explorer) {{
                    Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
                    Start-Sleep -Seconds 2
                    Start-Process explorer
                    Write-Host "Explorer 재시작으로 작업표시줄 새로고침 완료"
                    return $true
                }}
            }} catch {{
                Write-Host "Explorer 재시작 실패: $($_.Exception.Message)"
            }}
        }}
        
        return $false
    }} catch {{
        Write-Host "Windows API 사용 오류: $($_.Exception.Message)"
        return $false
    }}
    """
    
    result = _run_powershell(ps_command)
    return result and "작업표시줄 새로고침 완료" in result


def _debug_list_taskbar_shortcuts(target_name: str) -> None:
    """디버깅: 작업표시줄에 있는 모든 바로가기 목록을 출력합니다."""
    YELLOW = PK_ANSI_COLOR_MAP.get("YELLOW", "")
    RESET = PK_ANSI_COLOR_MAP.get("RESET", "")
    
    ps_command = """
    try {
        $taskbarPath = "$env:APPDATA\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar"
        if (Test-Path $taskbarPath) {
            $allShortcuts = Get-ChildItem -Path $taskbarPath -ErrorAction SilentlyContinue
            Write-Host "작업표시줄 폴더 경로: $taskbarPath"
            Write-Host "총 바로가기 개수: $($allShortcuts.Count)"
            Write-Host "바로가기 목록:"
            foreach ($shortcut in $allShortcuts) {
                $name = $shortcut.Name -replace '\\.lnk$', ''
                Write-Host "  - $name"
            }
        } else {
            Write-Host "작업표시줄 폴더가 존재하지 않음: $taskbarPath"
        }
    } catch {
        Write-Host "디버깅 오류: $($_.Exception.Message)"
    }
    """
    
    result = _run_powershell(ps_command)
    if result:
        # 대상 이름과 일치하는지 확인
        if target_name.lower() in result.lower():
            print(f"{YELLOW}✅ 대상 바로가기 발견: {target_name}{RESET}")
        else:
            print(f"{YELLOW}⚠️ 대상 바로가기를 찾을 수 없음: {target_name}{RESET}")
            print(f"{YELLOW}💡 위 목록에서 정확한 이름을 확인하세요.{RESET}")


def _run_powershell(command: str) -> Optional[str]:
    """PowerShell 명령어를 실행하고 결과를 반환합니다."""
    YELLOW = PK_ANSI_COLOR_MAP.get("YELLOW", "")
    RESET = PK_ANSI_COLOR_MAP.get("RESET", "")
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            shell=True,
            timeout=30
        )
        
        # 출력 결과를 항상 표시 (디버깅용)
        if result.stdout:
            output_lines = result.stdout.strip().split('\n')
            for line in output_lines:
                if line.strip():
                    print(f"{YELLOW}  {line}{RESET}")
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"{YELLOW}PowerShell 실행 실패 (코드: {result.returncode}){RESET}")
            if result.stderr:
                stderr_lines = result.stderr.strip().split('\n')
                for line in stderr_lines:
                    if line.strip():
                        print(f"{YELLOW}  오류: {line}{RESET}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"{YELLOW}PowerShell 실행 시간 초과{RESET}")
        return None
    except Exception as e:
        print(f"{YELLOW}PowerShell 실행 중 오류: {e}{RESET}")
        return None


def ensure_multiple_pinned_removed(shortcut_names: List[str]) -> dict:
    """여러 바로가기를 작업표시줄에서 제거합니다."""
    results = {}
    
    for name in shortcut_names:
        print(f"{'='*50}")
        print(f"처리 중: {name}")
        print(f"{'='*50}")
        
        start_time = time.time()
        success = ensure_taskbar_pinned_removed(name)
        elapsed = time.time() - start_time
        
        results[name] = {
            'success': success,
            'elapsed_time': elapsed,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 다음 처리 전 잠시 대기
        time.sleep(1)
    
    return results


def print_removal_summary(results: dict) -> None:
    """제거 결과 요약을 출력합니다."""
    print(f"{'='*60}")
    print(" 작업표시줄 제거 결과 요약")
    print(f"{'='*60}")
    
    total = len(results)
    successful = sum(1 for r in results.values() if r['success'])
    failed = total - successful
    
    print(f"총 처리 항목: {total}")
    print(f"성공: {successful} ")
    print(f"실패: {failed} ")
    print(f"성공률: {(successful/total*100):.1f}%")
    
    print(f"\n 상세 결과:")
    for name, result in results.items():
        status = " 성공" if result['success'] else " 실패"
        print(f"  {name}: {status} ({result['elapsed_time']:.2f}초)")
    
    print(f"\n 처리 완료 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")


# 직접 실행 시 테스트
if __name__ == "__main__":
    print(" 작업표시줄 제거 테스트 시작...")
    
    # 단일 항목 테스트
    print("1. 단일 항목 제거 테스트")
    success = ensure_taskbar_pinned_removed("pk_launcher")
    print(f"결과: {'성공' if success else '실패'}")
    
    # 여러 항목 테스트
    print("2. 여러 항목 제거 테스트")
    test_names = ["pk_launcher", "test_app", "sample_app"]
    results = ensure_multiple_pinned_removed(test_names)
    
    # 결과 요약
    print_removal_summary(results)
    
    print(" 테스트 완료!")
