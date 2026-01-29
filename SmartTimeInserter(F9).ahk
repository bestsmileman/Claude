; === SmartTimeInserter (AutoHotkey v2 - F9 키 시간 입력 기능만) ===
#Requires AutoHotkey v2.0
#SingleInstance Force
Persistent

; 실행 확인 ToolTip
ToolTip "SmartTimeInserter 실행됨 - Shift+Enter로 줄바꿈 안정 적용"
SetTimer(() => ToolTip(), -2000)

; F9 - 현재 시간 표시 + 문서 입력
F9::
{
    now := FormatTime("", "yyyy-MM-dd HH:mm:ss")
    Send("{Text}" . now)
    ToolTip(now)
    SetTimer(() => ToolTip(), -1500)
}