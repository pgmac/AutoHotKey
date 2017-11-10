; Create the ListView with one column:
Gui, Add, ListView, -Multi -ReadOnly gMyListView, Server|User
Gui, Add, Button, Hidden Default, Default

; Gather a list of file names from a folder and put them into the ListView:
Loop Read, C:\Downloads\servers.lst
{
	;LV_Add("", A_LoopReadLine)
	ConnInfo := StrSplit(A_LoopReadLine, "@")
	LV_Add("", ConnInfo[2], ConnInfo[1])
}

LV_ModifyCol()  ; Auto-size each column to fit its contents.

; Display the window and return. The script will be notified whenever the user double clicks a row.
Gui, Show
Return

MyListView:
if A_GuiEvent = DoubleClick
{
	LV_GetText(RowText, A_EventInfo)  ; Get the text from the row's first field.
	; ToolTip You double-clicked row number %A_EventInfo%. Text: "%RowText%"
	LV_GetText(ServerText, LV_GetNext(0, "Focused"), 1)
	LV_GetText(UserText, LV_GetNext(0, "Focused"), 2)
	Run %A_WinDir%\System32\bash.exe -c "ssh %UserText%@%ServerText%"
	;WinSetTitle, C:\Windows\System32\bash.exe, , "%UserText%@%ServerText%"
	WinWaitActive, C:\Windows\System32\bash.exe
	WinSetTitle "%UserText%@%ServerText%"
	WinClose
}
Return

ButtonDefault:
GuiControlGet, FocusedControl, Focus
if FocusedControl <> SysListview321
	Return
LV_GetText(ServerText, LV_GetNext(0, "Focused"), 1)
LV_GetText(UserText, LV_GetNext(0, "Focused"), 2)
Run %A_WinDir%\System32\bash.exe -c "ssh %UserText%@%ServerText%"
;WinSetTitle, C:\Windows\System32\bash.exe, , "%UserText%@%ServerText%"
WinWaitActive, C:\Windows\System32\bash.exe
WinSetTitle "%UserText%@%ServerText%"
WinClose
Return

GuiClose:  ; Indicate that the script should exit automatically when the window is closed.
ExitApp

GuiEscape:  ; Ensure the script exits when ESC is pressed
ExitApp