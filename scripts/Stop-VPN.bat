@echo off
echo Stopping Xray VPN...
taskkill /f /im xray.exe
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f

echo Removing proxy settings from running apps...
powershell -Command "$code = @'
using System;
using System.Runtime.InteropServices;
public class Win32 {
  [DllImport(\"user32.dll\", SetLastError = true, CharSet = CharSet.Auto)]
  public static extern IntPtr SendMessageTimeout(IntPtr hWnd, uint Msg, UIntPtr wParam, string lParam, uint fuFlags, uint uTimeout, out UIntPtr lpdwResult);
}
'@; Add-Type -TypeDefinition $code -Language CSharp; $HWND_BROADCAST = [IntPtr]0xffff; $WM_SETTINGCHANGE = 0x001A; $SMTO_NORMAL = 0x0000; $result = [UIntPtr]::Zero; [Win32]::SendMessageTimeout($HWND_BROADCAST, $WM_SETTINGCHANGE, [UIntPtr]::Zero, 'Internet Settings', $SMTO_NORMAL, 1000, [ref]$result)"

echo VPN Stopped!
pause
