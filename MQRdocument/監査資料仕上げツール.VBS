Dim Obj

MsgBox "起動中ですOKボタンを押して少しおまちください"
 
Set Obj = WScript.CreateObject("Excel.Application")
 
Obj.Visible = False
 
CreateObject("WScript.Shell").AppActivate Obj.Caption
 
Set Wb = Obj.Workbooks.Open ("C:\MQRdocument\excel_bug.xlsm")
 
Obj.Application.Run "excel_bug"

