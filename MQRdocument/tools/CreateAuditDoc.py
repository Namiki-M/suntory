from tools import HtmlParser4Manual as p4m
from tools import AuditFileController as afc
from tools import ManualParam as mp
import tkinter as tk
from tkinter import messagebox

#監査資料作成のクラス
class CreateAuditDoc():
    
    manualDir = ""
    targetManuals = []
    searchConditions = []
    
    parse4Manual:'p4m.HtmlParser4Manual' = p4m.HtmlParser4Manual()
    auditFileController = afc.AuditFileController()
    manualparam = mp.ManualParam()
    subjectedDefectMode4xls:str = ""
    subjectedPackaging4xls:str = ""
    subjectedLine4xls:str = ""
    subsection4Xls:str = ""
    subsubsection4Xls:str = ""
    purpose4Xls:str = ""
    task1Procedure4Xlsx:'list[str]' = []
    task1Frequency4Xlsx:'list[str]' = []
    task1Operating4Xlsx:'list[str]' = []
    task2Procedure4Xlsx:'list[str]' = []
    task2Frequency4Xlsx:'list[str]' = []
    task2Operating4Xlsx:'list[str]' = []
    task3Procedure4Xlsx:'list[str]' = []
    task3Frequency4Xlsx:'list[str]' = []
    task3Operating4Xlsx:'list[str]' = []
    task4Procedure4Xlsx:'list[str]' = []
    task4Frequency4Xlsx:'list[str]' = []
    task4Operating4Xlsx:'list[str]' = []
    task5Procedure4Xlsx:'list[str]' = []
    task5Frequency4Xlsx:'list[str]' = []
    task5Operating4Xlsx:'list[str]' = []
    task6Procedure4Xlsx:'list[str]' = []
    task6Frequency4Xlsx:'list[str]' = []
    task6Operating4Xlsx:'list[str]' = []
    task7Procedure4Xlsx:'list[str]' = []
    task7Frequency4Xlsx:'list[str]' = []
    task7Operating4Xlsx:'list[str]' = []
    task8Procedure4Xlsx:'list[str]' = []
    task8Frequency4Xlsx:'list[str]' = []
    task8Operating4Xlsx:'list[str]' = []
    
    
    # コンストラクタ
    def __init__(self):
        print("init:CreateAuditDoc")
        
    # fileNm4Audit:監査資料のファイル名（入力するやつ）,
    # searchCond:チェックされている検索条件(配列を想定),
    # manualFile:マニュアルファイル(配列を想定),
    # priority:（チェックあり：ON、なし：OFF）    
    def makeAuditDoc(self,fileNm4Audit,searchCond,manualFile,priority):
        print("START makeAuditDoc")
        self.searchConditions = searchCond
        self.targetManuals = manualFile
        
        # 検索条件のセット
        selectSection:str = self.convArrangement2String(self,self.searchConditions[0])
        selectDefectMode:str = self.convArrangement2String(self,self.searchConditions[1])
        selectPackage:str = self.convArrangement2String(self,self.searchConditions[2])
        selectLine:str = self.convArrangement2String(self,self.searchConditions[3])
        
        self.manualparam.set_selectedSection(selectSection)
        self.manualparam.set_selectedDefectMode(selectDefectMode)
        self.manualparam.set_selectedPackaging(selectPackage)
        self.manualparam.set_selectedLine(selectLine)
        
        self.manualparam.set_priorityOnly(priority)
            
        # デバッグ用
        debugList:'list[str]' = []
        debugList.append("Foreign material contamination")
        
        # 検索条件のリストとしてすべて詰め込む。
        allCond:'list[str]' = []
        lstSelectDefectMode:'list[str]' = searchCond[1]
        lstSelectPackaging:'list[str]' = searchCond[2]
        lstSelectLine:'list[str]' = searchCond[3]
        for val in lstSelectDefectMode :
            allCond.append(val)
        
        for val in lstSelectPackaging :
            allCond.append(val)
        
        for val in lstSelectLine :
            allCond.append(val)
        
        self.sub_win = tk.Toplevel()
        self.sub_win.geometry("700x250")
        
        self.sub_win.grab_set()
        #ラベル
        lbl = tk.Label(self.sub_win,text='ファイル名')
        lbl.place(x=30, y=50)
         # テキストボックス
        txt = tk.Entry(self.sub_win,width=75)
        txt.place(x=90, y=50)

        sampletxt = tk.Label(self.sub_win,text='入力例:      監査資料1')
        sampletxt.place(x=30,y = 80)
        
        sampletxt = tk.Label(self.sub_win,text='.xlsx')
        sampletxt.place(x=545,y = 50)
        
        

        def name_write():
            fileNm4Audit = txt.get()
           
            if fileNm4Audit == '':
                messagebox.showerror('エラー','ファイル名が入力されていません')
            elif '/' in fileNm4Audit :
                messagebox.showerror('エラー','/は使用できません') 
            elif '-'  in fileNm4Audit:
                messagebox.showerror('エラー','-は使用できません') 
            elif '.'  in fileNm4Audit:
                messagebox.showerror('エラー','.は使用できません') 
            elif '*' in fileNm4Audit :
                messagebox.showerror('エラー','*は使用できません') 
            elif '?' in fileNm4Audit :
                messagebox.showerror('エラー','?は使用できません') 
            elif '{' in fileNm4Audit :
                messagebox.showerror('エラー','{は使用できません') 
            elif '}'in fileNm4Audit :
                messagebox.showerror('エラー','}は使用できません') 
            elif '\\' in fileNm4Audit :
                messagebox.showerror('エラー','\は使用できません') 
            else:
                fileNm4Audit = fileNm4Audit+".xlsx"
                #ここのelseの文の中に実行させたいコードを入力してください
                print(fileNm4Audit)
                # 初期処理内で、デスクトップにファイルをコピーする。
                self.auditFileController.copyOriginalFile(fileNm4Audit)
               
                #ここまでの間に実行させたいファイルを入力してください
                messagebox.showinfo('メッセージ','監査資料を作成しました')
                self.sub_win.destroy()
        def sub_win_del():
            self.sub_win.destroy()

        self.writebtn = tk.Button(self.sub_win,text='名前保存',width=15,height=2, command=lambda:name_write())
        self.writebtn.place(x=130,y=170)
        self.writebtn.bind("<Return>",lambda event:name_write())
        self.writebtn = tk.Button(self.sub_win,text='キャンセル',width=15,height=2, command=lambda:sub_win_del())
        self.writebtn.place(x=300,y=170)
        self.writebtn.bind("<Return>",lambda event:sub_win_del())
        
        self.sub_win.mainloop()
        
        
        for mf in manualFile :
            print(mf)
            # self.manualparam = self.parse4Manual.parseManualData(mf, allCond,self.manualparam)
            # ★★★★★デバッグ中★★★★★
            self.manualparam = self.parse4Manual.parseManualData(mf, debugList,self.manualparam,priority)
            
            self.auditFileController.openTargetAuditDoc(self.manualparam)

    # 配列形式からカンマ区切りの文字データへ変換
    def convArrangement2String(self,val):
        print("START convArrangement2String")
        retStr:'str' = ""
        valList:'list[str]' = val
        for str in valList :
            if retStr == "" :
                retStr = str
            else :
                retStr = retStr + "," + str
        return retStr
 