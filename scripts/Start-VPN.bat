@echo off
echo Starting Xray VPN...
set "XRAY_PATH=C:\Users\PC\.gemini\antigravity\playground\metallic-chromosphere\xray2\xray.exe"
set "XRAY_CONF=C:\Users\PC\.gemini\antigravity\playground\metallic-chromosphere\test-xray.json"

if not exist "%XRAY_PATH%" (
    echo Error: Xray not found at %XRAY_PATH%
    pause
    exit /b 1
)

start "XRAY_VPN_BACKGROUND" /min "%XRAY_PATH%" run -c "%XRAY_CONF%"

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d "127.0.0.1:2082" /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /t REG_SZ /d "127.0.0.1;localhost;<local>" /f

echo Applying proxy settings to running apps...
powershell -Command "$code = @'
using System;
using System.Runtime.InteropServices;
public class Win32 {
  [DllImport(\"user32.dll\", SetLastError = true, CharSet = CharSet.Auto)]
  public static extern IntPtr SendMessageTimeout(IntPtr hWnd, uint Msg, UIntPtr wParam, string lParam, uint fuFlags, uint uTimeout, out UIntPtr lpdwResult);
}
'@; Add-Type -TypeDefinition $code -Language CSharp; $HWND_BROADCAST = [IntPtr]0xffff; $WM_SETTINGCHANGE = 0x001A; $SMTO_NORMAL = 0x0000; $result = [UIntPtr]::Zero; [Win32]::SendMessageTimeout($HWND_BROADCAST, $WM_SETTINGCHANGE, [UIntPtr]::Zero, 'Internet Settings', $SMTO_NORMAL, 1000, [ref]$result)"

echo VPN Started! System proxy enabled.
echo Note: If your browser still doesn't open blocked sites, please restart the browser once!
pause
