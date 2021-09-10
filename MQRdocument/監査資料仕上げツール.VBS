Dim Obj

MsgBox "‹N“®’†‚Å‚·OKƒ{ƒ^ƒ“‚ğ‰Ÿ‚µ‚Ä­‚µ‚¨‚Ü‚¿‚­‚¾‚³‚¢"
 
Set Obj = WScript.CreateObject("Excel.Application")
 
Obj.Visible = False
 
CreateObject("WScript.Shell").AppActivate Obj.Caption
 
Set Wb = Obj.Workbooks.Open ("C:\MQRdocument\excel_bug.xlsm")
 
Obj.Application.Run "excel_bug"

