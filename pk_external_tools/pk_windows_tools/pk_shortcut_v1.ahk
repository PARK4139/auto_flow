; windows 11 pro msi 동작 안됨.
; ^!t::  ; Ctrl + Alt + T
; Run, cmd,, Max, cmdPID
; WinWait, ahk_pid %cmdPID%
; WinActivate, ahk_pid %cmdPID%
; Send, venv{Enter}
; return


; windows 10 pro 동작잘됨 ; windows 11 pro msi 동작 안됨.
; ^!t::  ; Ctrl + Alt + T
; Run, cmd,, , pid
; WinWaitActive, ahk_pid %pid%


^!t::  ; Ctrl + Alt + T
    ; 1) cmd.exe 실행
    Run, cmd,, , pid
    WinWaitActive, ahk_pid %pid%

    ; 2) 폰트 크기 조정 (24px 높이)
    RegWrite, REG_SZ,    HKCU, Console,         FaceName,    Consolas
    RegWrite, REG_DWORD, HKCU, Console,         FontFamily,  54                ; TrueType
    ; FontSize = (높이 << 16) | 너비  → 24px 높이
    ; 12px
    ; RegWrite, REG_DWORD, HKCU, Console,         FontSize,    0x000C0000

    ; 14px → 14 << 16 = 0x000E0000
    ; RegWrite, REG_DWORD, HKCU, Console, FontSize, 0x000E0000

    ; 16px → 16 << 16 = 0x00100000
    ; RegWrite, REG_DWORD, HKCU, Console, FontSize, 0x00100000

    ; 18px → 18 << 16 = 0x00120000
    ; RegWrite, REG_DWORD, HKCU, Console, FontSize, 0x00120000

    ; 20px → 20 << 16 = 0x00140000
    RegWrite, REG_DWORD, HKCU, Console, FontSize, 0x00140000

    ; 22px → 22 << 16 = 0x00160000
    ; RegWrite, REG_DWORD, HKCU, Console, FontSize, 0x00160000

    ; 24px → 24 << 16 = 0x00180000
    ; RegWrite, REG_DWORD, HKCU, Console, FontSize, 0x00180000

    ; 26px → 26 << 16 = 0x001A0000
    ; RegWrite, REG_DWORD, HKCU, Console, FontSize, 0x001A0000

    ; 28px → 28 << 16 = 0x001C0000
    ; RegWrite, REG_DWORD, HKCU, Console, FontSize, 0x001C0000

    ; 30px → 30 << 16 = 0x001E0000
    ; RegWrite, REG_DWORD, HKCU, Console, FontSize, 0x001E0000

    ; 32px → 32 << 16 = 0x00200000
    ; RegWrite, REG_DWORD, HKCU, Console, FontSize, 0x00200000

    ; 36px → 36 << 16 = 0x00240000
    ; RegWrite, REG_DWORD, HKCU, Console, FontSize, 0x00240000

    ; 40px → 40 << 16 = 0x00280000
    ; RegWrite, REG_DWORD, HKCU, Console, FontSize, 0x00280000


    ; 화면·창 크기 정보 가져오기
    SysGet, monW, 78    ; 모니터 너비
    SysGet, monH, 79    ; 모니터 높이
    WinGetPos, X, Y, W, H, ahk_pid %pid%

    ; 원하는 새 창 크기 설정
    newW := 1800         ; 창 너비(px)
    newH := H           ; 높이는 기본값 유지(필요시 조정)

    ; 중앙 좌표 계산 (너비·높이 반영)
    newX := (monW - newW) // 2
    newY := (monH - newH) // 2

    ; 이동 및 크기 적용
    WinMove, ahk_pid %pid%, , newX, newY, newW, newH

    ; venv 실행
    ; SendInput, venv{Enter}
return