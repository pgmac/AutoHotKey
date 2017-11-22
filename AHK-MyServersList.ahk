; Create the ListView with one column:
Gui, Add, ListView, w380 h580 -Multi -ReadOnly gMyListView, Server|User|ServerIP
Gui, Add, Button, Hidden Default, Default

; Gather a list of file names from a folder and put them into the ListView:
Loop Read, %A_MyDocuments%\servers.all.lst
{
	;LV_Add("", A_LoopReadLine)
	ConnInfo := StrSplit(A_LoopReadLine, "@")
	LV_Add("", ConnInfo[3], ConnInfo[1], ConnInfo[2])
}

LV_ModifyCol()  ; Auto-size each column to fit its contents.
;LV_ModifyCol(2, 100)
LV_ModifyCol(3, 0)
LV_ModifyCol(1, "Sort")

; Display the window and return. The script will be notified whenever the user double clicks a row.
Gui, Show, w400 h600
Return

MyListView:
if A_GuiEvent = DoubleClick
{
	LV_GetText(RowText, A_EventInfo)  ; Get the text from the row's first field.
	; ToolTip You double-clicked row number %A_EventInfo%. Text: "%RowText%"
	LV_GetText(ServerText, LV_GetNext(0, "Focused"), 1)
	LV_GetText(UserText, LV_GetNext(0, "Focused"), 2)
	LV_GetText(IPText, LV_GetNext(0, "Focused"), 3)
	Run %A_WinDir%\System32\bash.exe -c "ssh %UserText%@%IPText%"
	WinSetTitle, C:\Windows\System32\bash.exe, , "%UserText%@%IPText%"
	WinClose
}
Return

ButtonDefault:
GuiControlGet, FocusedControl, Focus
if FocusedControl <> SysListview321
	Return
LV_GetText(ServerText, LV_GetNext(0, "Focused"), 1)
LV_GetText(UserText, LV_GetNext(0, "Focused"), 2)
LV_GetText(IPText, LV_GetNext(0, "Focused"), 3)
Run %A_WinDir%\System32\bash.exe -c "ssh %UserText%@%IPText%"
WinSetTitle, C:\Windows\System32\bash.exe, , "%UserText%@%IPText%"
WinClose
Return

GuiClose:  ; Indicate that the script should exit automatically when the window is closed.
ExitApp

GuiEscape:  ; Ensure the script exits when ESC is pressed
ExitApp