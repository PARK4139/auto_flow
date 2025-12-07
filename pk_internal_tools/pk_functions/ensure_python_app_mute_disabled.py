
import subprocess
import textwrap
import os
from pathlib import Path
import logging
import tempfile



def ensure_python_app_mute_disabled(process_name: str = "python"):
    import subprocess
    import textwrap
    import os
    from pathlib import Path
    import logging
    import tempfile

    """
    지정된 파이썬 애플리케이션의 음소거를 비활성화합니다.
    Windows Core Audio API를 사용하여 PowerShell 스크립트를 실행합니다.

    Args:
        process_name (str): 음소거를 해제할 파이썬 애플리케이션의 프로세스 이름 (예: "python", "pythonw").
                            기본값은 "python"입니다.

    주의:
        이 함수는 관리자 권한으로 실행해야 제대로 작동할 수 있습니다.
        PowerShell 스크립트가 임시 파일로 생성된 후 실행됩니다.
    """
    logging.info(f"'{process_name}' 프로세스의 음소거 비활성화 시도 중...")

    # PowerShell 스크립트 내용
    # 함수 정의와 함수 호출을 포함합니다.
    powershell_script_content = textwrap.dedent(f"""
        function Set-ApplicationAudioMute {{
            param(
                [Parameter(Mandatory=$true)]
                [string]$ProcessName,

                [Parameter(Mandatory=$true)]
                [bool]$Mute
            )

            Add-Type -TypeDefinition @'
                using System;
                using System.Runtime.InteropServices;

                namespace CoreAudio
                {{
                    // Define necessary COM interfaces and GUIDs
                    [Guid("BCDE0395-E52F-467C-8E3D-C4579291692E"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                    public interface IMMDeviceEnumerator
                    {{
                        int EnumAudioEndpoints(EDataFlow dataFlow, EDeviceState dwStateMask, out IMMDeviceCollection ppDevices);

                        int GetDefaultAudioEndpoint(EDataFlow dataFlow, ERole role, out IMMDevice ppDevice);

                        int GetDevice(string pwstrId, out IMMDevice ppDevice);

                        int RegisterEndpointNotificationCallback(IMMNotificationClient pClient);

                        int UnregisterEndpointNotificationCallback(IMMNotificationClient pClient);

                    }}

                    [Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                    public interface IMMDevice
                    {{
                        int Activate(ref Guid iid, uint dwClsCtx, IntPtr pActivationParams, [MarshalAs(UnmanagedType.IUnknown)] out object ppInterface);

                        int OpenPropertyStore(uint stgmAccess, out IPropertyStore ppProperties);

                        int GetId(out string ppstrId);

                        int GetState(out EDeviceState pdwState);

                    }}

                    [Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                    public interface IMMDeviceCollection
                    {{
                        int GetCount(out uint pcDevices);

                        int Item(uint nDevice, out IMMDevice ppDevice);

                    }}

                    [Guid("77F1A6E3-3346-4192-8334-42602736006C"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                    public interface IAudioSessionManager2
                    {{
                        int GetSessionEnumerator(out IAudioSessionEnumerator SessionEnum);

                        int GetSession(EDataFlow dataFlow, ref Guid AudioSessionGuid, out IAudioSessionControl2 SessionControl);

                        int RegisterSessionNotification(IAudioSessionNotification SessionNotification);

                        int UnregisterSessionNotification(IAudioSessionNotification SessionNotification);

                    }}

                    [Guid("E2F5BB11-075B-4854-FA36-E1CD03F35D7F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                    public interface IAudioSessionEnumerator
                    {{
                        int GetCount(out int SessionCount);

                        int GetSession(int SessionCount, out IAudioSessionControl2 Session);

                    }}

                    [Guid("BFB7FF88-7239-4FC9-8FA2-07C950BE9C6D"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                    public interface IAudioSessionControl2
                    {{
                        // IAudioSessionControl methods
                        int GetState(out AudioSessionState pRetVal);

                        int GetDisplayName(out string pRetVal);

                        int GetIconPath(out string pRetVal);

                        int GetGroupingParam(out Guid pRetVal);

                        int SetGroupingParam(ref Guid pRetVal, ref Guid EventContext);

                        int RegisterSessionNotification(IAudioSessionNotification pRetVal);

                        int UnregisterSessionNotification(IAudioSessionNotification pRetVal);


                        // IAudioSessionControl2 methods
                        int GetSessionIdentifier(out string pRetVal);

                        int GetSessionInstanceIdentifier(out string pRetVal);

                        int GetProcessId(out int pRetVal);

                        int GetSessionFlags(out uint pRetVal);

                        int ExpireSession();

                        int RegisterAudioSessionNotification(IAudioSessionNotification pRetVal);

                        int UnregisterAudioSessionNotification(IAudioSessionNotification pRetVal);

                    }}

                    [Guid("87CE5498-68D6-44E5-9215-6DA47EF883D8"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                    public interface ISimpleAudioVolume
                    {{
                        int SetMasterVolume(float fLevel, ref Guid EventContext);

                        int GetMasterVolume(out float pfLevel);

                        int SetMute([MarshalAs(UnmanagedType.Bool)] bool bMute, ref Guid EventContext);

                        int GetMute([MarshalAs(UnmanagedType.Bool)] out bool pbMute);

                    }}


                    // Enums
                    public enum EDataFlow
                    {{
                        eRender,

                        eCapture,

                        eAll

                    }}


                    public enum ERole
                    {{
                        eConsole,

                        eMultimedia,

                        eCommunications

                    }}


                    [Flags]
                    public enum EDeviceState
                    {{
                        Active = 0x00000001,

                        Disabled = 0x00000002,

                        NotPresent = 0x00000004,

                        Unplugged = 0x00000008,

                        All = 0x0000000F

                    }}


                    public enum AudioSessionState
                    {{
                        Inactive = 0,

                        Active = 1,

                        Expired = 2

                    }}


                    // COM objects
                    [ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")]
                    internal class MMDeviceEnumeratorComObject {{ }}


                    // Dummy interfaces for unused methods
                    [Guid("657804FA-D6AD-4496-8A60-3527528F5415"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                    public interface IMMNotificationClient {{ }}


                    [Guid("BBEA4930-B219-4521-9671-7C671A261BC0"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                    public interface IPropertyStore {{ }}


                    [Guid("C8AD0F81-5D6F-4BD2-8429-5218CE55E649"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                    public interface IAudioSessionNotification {{ }}

                }}

            '@ -ErrorAction Stop


            try {{
                $MMDeviceEnumerator = New-Object -TypeName CoreAudio.MMDeviceEnumeratorComObject

                $MMDeviceEnumeratorGuid = [System.Guid]::Parse("BCDE0395-E52F-467C-8E3D-C4579291692E")

                $IMMDeviceEnumerator = [System.Runtime.InteropServices.Marshal]::GetTypedObjectForIUnknown($MMDeviceEnumerator, [CoreAudio.IMMDeviceEnumerator])


                $DefaultRenderDevice = $null

                $IMMDeviceEnumerator.GetDefaultAudioEndpoint([CoreAudio.EDataFlow]::eRender, [CoreAudio.ERole]::eMultimedia, [ref]$DefaultRenderDevice) | Out-Null


                if ($DefaultRenderDevice -eq $null) {{

                    Write-Error "Could not get default audio render device."

                    return

                }}


                $IAudioSessionManager2Guid = [System.Guid]::Parse("77F1A6E3-3346-4192-8334-42602736006C")

                $AudioSessionManager2 = $null

                $DefaultRenderDevice.Activate([ref]$IAudioSessionManager2Guid, 23, [System.IntPtr]::Zero, [ref]$AudioSessionManager2) | Out-Null


                if ($AudioSessionManager2 -eq $null) {{

                    Write-Error "Could not get audio session manager."

                    return

                }}


                $IAudioSessionManager2 = [System.Runtime.InteropServices.Marshal]::GetTypedObjectForIUnknown($AudioSessionManager2, [CoreAudio.IAudioSessionManager2])


                $AudioSessionEnumerator = $null

                $IAudioSessionManager2.GetSessionEnumerator([ref]$AudioSessionEnumerator) | Out-Null


                if ($AudioSessionEnumerator -eq $null) {{

                    Write-Error "Could not get audio session enumerator."

                    return

                }}


                $IAudioSessionEnumerator = [System.Runtime.InteropServices.Marshal]::GetTypedObjectForIUnknown($AudioSessionEnumerator, [CoreAudio.IAudioSessionEnumerator])


                $SessionCount = 0

                $IAudioSessionEnumerator.GetCount([ref]$SessionCount) | Out-Null


                $found = $false

                for ($i = 0; $i -lt $SessionCount; $i++) {{

                    $SessionControl2 = $null

                    $IAudioSessionEnumerator.GetSession($i, [ref]$SessionControl2) | Out-Null


                    if ($SessionControl2 -eq $null) {{

                        continue

                    }}


                    $IAudioSessionControl2 = [System.Runtime.InteropServices.Marshal]::GetTypedObjectForIUnknown($SessionControl2, [CoreAudio.IAudioSessionControl2])


                    $pid = 0

                    $IAudioSessionControl2.GetProcessId([ref]$pid) | Out-Null


                    $process = Get-Process -Id $pid -ErrorAction SilentlyContinue

                    if ($process -ne $null -and $process.ProcessName -eq $ProcessName) {{

                        $ISimpleAudioVolumeGuid = [System.Guid]::Parse("87CE5498-68D6-44E5-9215-6DA47EF883D8")

                        $SimpleAudioVolume = $null

                        $IAudioSessionControl2.Activate([ref]$ISimpleAudioVolumeGuid, 23, [System.IntPtr]::Zero, [ref]$SimpleAudioVolume) | Out-Null


                        if ($SimpleAudioVolume -ne $null) {{

                            $ISimpleAudioVolume = [System.Runtime.InteropServices.Marshal]::GetTypedObjectForIUnknown($SimpleAudioVolume, [CoreAudio.ISimpleAudioVolume])

                            $eventContext = [System.Guid]::NewGuid()

                            $ISimpleAudioVolume.SetMute($Mute, [ref]$eventContext) | Out-Null

                            Write-Host "Successfully set mute state for process '$ProcessName' to '$Mute'."

                            $found = $true

                        }}

                    }}

                    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($SessionControl2) | Out-Null

                }}


                if (-not $found) {{

                    Write-Warning "No active audio session found for process '$ProcessName'."

                }}


            }} catch {{

                Write-Error "An error occurred: $($_.Exception.Message)"

            }} finally {{

                # Release COM objects to prevent memory leaks
                if ($IAudioSessionEnumerator -ne $null) {{ [System.Runtime.InteropServices.Marshal]::ReleaseComObject($IAudioSessionEnumerator) | Out-Null }}

                if ($IAudioSessionManager2 -ne $null) {{ [System.Runtime.InteropServices.Marshal]::ReleaseComObject($IAudioSessionManager2) | Out-Null }}

                if ($DefaultRenderDevice -ne $null) {{ [System.Runtime.InteropServices.Marshal]::ReleaseComObject($DefaultRenderDevice) | Out-Null }}

                if ($IMMDeviceEnumerator -ne $null) {{ [System.Runtime.InteropServices.Marshal]::ReleaseComObject($IMMDeviceEnumerator) | Out-Null }}

                if ($MMDeviceEnumerator -ne $null) {{ [System.Runtime.InteropServices.Marshal]::ReleaseComObject($MMDeviceEnumerator) | Out-Null }}

            }}

        }}


        # 함수 호출
        Set-ApplicationAudioMute -ProcessName '$TARGET_PROCESS_NAME
    """)

    # tempfile을 사용하여 임시 PowerShell 스크립트 파일 생성
    # delete=True로 설정하여 파일이 닫힐 때 자동으로 삭제되도록 합니다.
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False, encoding='utf-8') as temp_ps_file:
        temp_ps_file.write(powershell_script_content.replace('$ProcessName', process_name))
        temp_ps_file_path = temp_ps_file.name
    logging.debug(f"임시 PowerShell 스크립트 파일 경로: {temp_ps_file_path}")

    try:
        # PowerShell 명령 실행
        command = [
            "powershell.exe",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(temp_ps_file_path)
        ]
        logging.debug(f"실행할 PowerShell 명령: {' '.join(command)}")

        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=False)

        if result.returncode == 0:
            logging.info(f"'{process_name}' 프로세스의 음소거 비활성화 성공.")
            if result.stdout:
                logging.debug(f"PowerShell stdout: {result.stdout}")
        else:
            logging.error(f"'{process_name}' 프로세스의 음소거 비활성화 실패. 오류 코드: {result.returncode}")
            if result.stdout:
                logging.error(f"PowerShell stdout: {result.stdout}")
            if result.stderr:
                logging.error(f"PowerShell stderr: {result.stderr}")

    except Exception as e:
        logging.error(f"PowerShell 스크립트 실행 중 예외 발생: {e}")
    finally:
        # 임시 파일 삭제 (tempfile.NamedTemporaryFile의 delete=False로 생성했으므로 수동 삭제 필요)
        if os.path.exists(temp_ps_file_path):
            os.remove(temp_ps_file_path)
            logging.debug(f"임시 PowerShell 스크립트 파일 삭제 완료: {temp_ps_file_path}")

