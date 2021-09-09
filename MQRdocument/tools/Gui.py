# coding: UTF-8
from os import path
import tkinter as tk
import webbrowser
from tkinter import messagebox
import threading
from tkinter import ttk

import tools.filter_data as fd
from tools.Filter import Filter
from tools.Save import Save
from tools.Search_log import Search_log
from tools.CreateAuditDoc import CreateAuditDoc
from natsort import natsorted
 

class Gui():
  #チェック項目
  

  section_bln_list:'list[str]' = []
  defect_bln_list:'list[str]' = []
  packaging_bln_list:'list[str]' = []
  line_bln_list:'list[str]' = []
  priority_bln = ''
  manual_name:'list[str]' = [] # 特定した各ファイルのページ名(section Div4 title)をまとめる配列、これの要素を一つ一つをウィンドウに表示
  manual_name_CAD:'list[str]' = [] # 特定した各ファイルのページ名(section Div4 title)をまとめる配列、これの要素を一つ一つをウィンドウに表示
  manual_path:'list[str]' = [] # 特定した各ファイルのパス情報をまとめる配列

  #チェックの入ったテキスト
  selected_section:'list[str]' = []
  selected_section2:'list[str]' = []
  selected_defect:'list[str]' = []
  selected_packaging:'list[str]' = []
  selected_line:'list[str]' = []

  # 検索機能で取得される情報
  manual_info_list:'list[list[str]]' = []

  # 各検索履歴に格納されている検索ワードリスト（自動チェックが入る項目）
  check_section_list:'list[str]' = []
  check_defect_list:'list[str]' = []
  check_packaging_list:'list[str]' = []
  check_line_list:'list[str]' = []

  # ログファイルに保存されている全検索履歴
  search_log_list:'list[list[list[str]]]' = []

  #セクションの判別
  section_judgment_list:'list[str]' = []

  #フィルター結果の配列
  section_result:'list[list[str]]' = [[]]
  defect_result:'list[list[str]]' = [[]]
  line_result:'list[list[str]]' = [[]]
  All_line_result:'list[list[str]]' = [[]]
  packaging_result:'list[list[str]]' = [[]]
  All_packaging_result:'list[list[str]]' = [[]]


#ボタン全解除or全選択
  def checkbtn_click( self ,boo): 
    for bln in self.section_bln_list:
      bln.set(boo)
    for bln in self.defect_bln_list:
      bln.set(boo)
    for bln in self.packaging_bln_list:
      bln.set(boo)
    for bln in self.line_bln_list:
        bln.set(boo)  

  def checksectionbtn_click( self ,boo): 
    for bln in self.section_bln_list:
      bln.set(boo)
  
  def checkdefectbtn_click( self ,boo): 
    for bln in self.defect_bln_list:
      bln.set(boo)

  def checkpackagingbtn_click( self ,boo): 
    for bln in self.packaging_bln_list:
      bln.set(boo)

  def checklinebtn_click( self ,boo): 
    for bln in self.line_bln_list:
        bln.set(boo)  
    
  
  # 検索結果出力ボタン押下時のクリックイベント
  def filter_btn_click(self, Filter):
    self.prg.pack()
    self.prg.start(5)
    

    # 検索結果ウィンドウの初期化
    self.result_window.destroy()
    self.result_window_frame = tk.Frame(self.main, bg="white")
    self.result_window_frame.place(x=950,y=380, width=320, height=240)
    self.result_window = tk.Canvas(self.main, bg="white")
    self.result_window.place(x=950,y=380, width=305, height=225)
    self.result_ybar = tk.Scrollbar(self.result_window_frame, orient=tk.VERTICAL)
    self.result_xbar = tk.Scrollbar(self.result_window_frame, orient=tk.HORIZONTAL)
    self.result_ybar.pack(side=tk.RIGHT, fill=tk.Y)
    self.result_xbar.pack(side=tk.BOTTOM, fill=tk.X)
    self.result_ybar.config(command=self.result_window.yview)
    self.result_xbar.config(command=self.result_window.xview)
    self.result_window.config(yscrollcommand=self.result_ybar.set, xscrollcommand=self.result_xbar.set)
    self.result_window.config(scrollregion=(0,0,1000,10000))
    self.result_frame = tk.Frame(self.result_window, bg="white")
    self.result_window.create_window((0,0), window=self.result_frame, anchor=tk.NW, width=1000, height=10000)

    # Sectionの検索処理
    self.selected_section.clear()
    self.section_judgment_list.clear()
    self.selected_section2.clear()
    self.section_result.clear()
    for i, bln in enumerate(self.section_bln_list):
      if bln.get():
        idx = fd.section_list[i].find('\u3000')
        r = fd.section_list[i][:idx]
        r2 = fd.section_list[i][idx:]
        s_s2 = r+r2
        table = str.maketrans({'\u3000':' '})
        s_s2 = s_s2.translate(table)
        r += '.'
        self.section_judgment_list.append(r.rstrip('.'))
        self.selected_section.append(r)
        self.selected_section2.append(s_s2)
        
    self.section_result = Filter.filter_by_section(Filter, self.selected_section)

    # Defect modeの検索処理
    self.selected_defect.clear()
    self.defect_result.clear()
    for i, bln in enumerate(self.defect_bln_list):
      if bln.get():
        self.selected_defect.append(fd.defect_list[i])
    self.defect_result = Filter.filter_by_defect(Filter, self.selected_defect)

    # Subjected packagingの検索処理
    self.selected_packaging.clear()
    self.packaging_result.clear()
    for i, bln in enumerate(self.packaging_bln_list):
      if bln.get():
        self.selected_packaging.append(fd.packaging_list[i])
    self.packaging_result = Filter.filter_by_packaging(Filter, self.selected_packaging)

    # Subjected lineの検索処理
    self.selected_line.clear()
    self.line_result.clear()
    for i, bln in enumerate(self.line_bln_list):
      if bln.get():
        self.selected_line.append(fd.line_list[i])
    self.line_result = Filter.filter_by_line(Filter, self.selected_line)

    #All_lineの検索処理
    self.All_line_result = Filter.filter_by_All_line(Filter)

    #All_packagingの検索処理
    self.All_packaging_result= Filter.filter_by_All_packaging(Filter)

    #検索キャッシュの削除
    Filter.log_delete(Filter)

     
    # 重複回避処理(名寄せ)
    def get_unique_list(seq):
      seen = []
      return [x for x in seq if x not in seen and not seen.append(x)]

    #Sectionフィルターでの絞り込みの処理
    #x[0]で配列の一つ目を指定
    def section_judgment(s_j,seq):
      seen = []
      for y in s_j:
        for x in seq:
          if y in x[0]:
            
            seen.append(x)
      return seen
    
    
    # 検索情報取得、表示
    # 特定した各ファイルの['ページ名(section Div4 title)', 'ファイル名(Manual-x-x-x-x.html)']の情報をまとめた二次元配列
   
    
    self.section_judgment_list = get_unique_list(self.section_judgment_list)
    self.manual_info_list =  self.defect_result + self.packaging_result + self.line_result + self.All_line_result + self.All_packaging_result
    print(self.manual_info_list)
    self.manual_info_list = get_unique_list(self.manual_info_list)
    self.manual_info_list = natsorted(self.manual_info_list)
    
    #右3つがはいっていない時
    if not self.manual_info_list:
      self.manual_info_list = self.section_result
    #Sectionフィルターでの絞り込み
    if len(self.section_judgment_list) :
      self.manual_info_list = section_judgment(self.section_judgment_list,self.manual_info_list)
    
    self.manual_info_list = get_unique_list(self.manual_info_list)
 

    self.manual_name.clear() # 特定した各ファイルのページ名(section Div4 title)をまとめる配列、これの要素を一つ一つをウィンドウに表示
    self.manual_path.clear() # 特定した各ファイルのパス情報をまとめる配列
    self.manual_name_CAD.clear()
    
    def open_file(num): # ページ名押下時のクリックイベント
      self.manual_name[num].bind("<Button-1>",lambda e:webbrowser.open_new_tab(self.manual_path[num]))
      
   
    for i, manual_info in enumerate(self.manual_info_list):
      self.manual_name.append(tk.Label(self.result_frame, bg="white", text=manual_info[0]))
      self.manual_path.append(f"file:///C:/MQRdocument/manual_data/{manual_info[1]}")
      self.manual_name[i].place(x=10, y=10+ 20*i)
      self.manual_name[i]['command'] = open_file(i) 
      self.manual_name_CAD.append(manual_info[1])
    print(len(self.manual_name))

      
      
    self.prg.stop()
    self.prg.pack_forget()
    messagebox.showinfo('メッセージ', '検索が完了しました')  


  # 検索条件保存ボタン押下時のクリックイベント
  def save_btn_click(self, Save): 
    if self.selected_section == [] and self.selected_defect == [] and self.selected_packaging == [] and self.selected_line == [] :
      messagebox.showerror('エラー', '検索処理を行ってください')
    else:
      Save.save_search_paramaters(Save, self.selected_section, self.selected_defect, self.selected_packaging, self.selected_line)

  def createfile(self,CreateAuditDoc):
    def get_unique_list(seq):
      seen = []
      return [x for x in seq if x not in seen and not seen.append(x)]
    filename = ''
    priority_word = ''
    searchCond = []
    self.selected_section2 = get_unique_list(self.selected_section2)
    searchCond.append(self.selected_section2)
    searchCond.append(self.selected_defect)
    searchCond.append(self.selected_packaging)
    searchCond.append(self.selected_line)
   
    if self.priority_bln.get() ==True:
      priority_word = 'ON'
    else:
      priority_word = 'OFF'
    
    CreateAuditDoc.makeAuditDoc(CreateAuditDoc,filename,searchCond,self.manual_name_CAD,priority_word)
 

  def loading(self):
    
    t = threading.Thread(target=self.filter_btn_click,args=(Filter,))  #スレッド立ち上げ
    t.start()
    
   
  
  



  # ログファイル読み込みボタン押下時のクリックイベント
  def log_btn_click(self, Search_log):

    # 検索ログウィンドウの初期化
    self.log_window.destroy()
    self.log_window_frame = tk.Frame(self.main)#アルゴリズム改修未 上田
    self.log_window_frame.place(x=0, y=20, width=950, height=490)
    self.log_window = tk.Canvas(self.main, bg="white")#アルゴリズム改修未 上田
    self.log_window.place(x=0, y=25, width=930, height=490)
    self.log_ybar = tk.Scrollbar(self.log_window_frame, orient=tk.VERTICAL)
    self.log_ybar.pack(side=tk.RIGHT, fill=tk.Y)
    self.log_ybar.config(command=self.log_window.yview)
    self.log_window.config(yscrollcommand=self.log_ybar.set)
    self.log_window.config(scrollregion=(0,0,1000,1000))
    self.log_frame = tk.Frame(self.log_window, bg="white")
    self.log_window.create_window((0,0), window=self.log_frame, anchor=tk.NW, width=305, height=10000)
    





    # 自動チェック処理
    def auto_check(search_log):

      # チェック状態の初期化
      for bln in self.section_bln_list:
        bln.set(False)
      for bln in self.defect_bln_list:
        bln.set(False)
      for bln in self.packaging_bln_list:
        bln.set(False)
      for bln in self.line_bln_list:
        bln.set(False)    
       
      # section 自動チェック      
      self.check_section_list = search_log[1]
      for check_section in self.check_section_list:
        idx = check_section.rfind('.')
        check_section = check_section[:idx]
        for i, section in enumerate(fd.section_list):
          if check_section in section:
            self.section_bln_list[i].set(True)
      # defect mode 自動チェック
      self.check_defect_list = search_log[2]
      for check_defect in self.check_defect_list:
        for i, defect in enumerate(fd.defect_list):
          if check_defect == defect:
            self.defect_bln_list[i].set(True) 
      # subjected packaging 自動チェック
      self.check_packaging_list = search_log[3]
      for check_packaging in self.check_packaging_list:
        for i, packaging in enumerate(fd.packaging_list):
          if check_packaging == packaging:
            self.packaging_bln_list[i].set(True) 
      # subjected line 自動チェック
      self.check_line_list = search_log[4]
      for check_line in self.check_line_list:
        for i, line in enumerate(fd.line_list):
          if check_line == line:
            self.line_bln_list[i].set(True)          
      messagebox.showinfo('メッセージ', '検索履歴よりチェック入力完了')        

    # 各ログファイル名押下時のクリックイベント
    def confirm(num, search_log):
      self.log_name[num].bind("<Button-1>", lambda e:auto_check(search_log))

    # ログファイルの読み込み・表示
    self.search_log_list = Search_log.get_search_paramaters(Search_log)
    self.log_name = []

    if self.search_log_list == []:
      messagebox.showinfo('メッセージ', 'ログファイルが存在しません')
    else:
      for i, search_log in enumerate(self.search_log_list):
        self.log_name.append(tk.Label(self.log_frame, bg="white", text=search_log[0]))
        self.log_name[i].place(x=10, y=10+ 20*i)
        self.log_name[i]['command'] = confirm(i, search_log)
      
  
  
  def __init__(self):
    #画面の作成
    self.main = tk.Tk()
    self.main.title("MQRフィルターツール")
    self.main.geometry("1250x700")
    #下地フレーム
    self.groundwork_window = tk.Frame(self.main,bg="#f0f8ff")
    self.groundwork_window.place(x=0,y=0, width=1250, height=700)
    #インジケータ#非確定的
    self.prg = ttk.Progressbar(self.main,mode="indeterminate")
    self.prg.pack_forget()
    # MQR全体表示
    def mqr_view():
      mqr_path = "file:///C:/MQRdocument/manual_data/_index.html" 
      webbrowser.open_new_tab(mqr_path)  
    #内部フレーム
    self.base_window = tk.Frame(self.groundwork_window,bg="#f0f8ff")
    self.base_window.place(x=20,y=0, width=1200, height=630)
    # 大分類ノートブック1
    self.note_window = ttk.Notebook(self.base_window)
    # タブの作成
    tab1 = tk.Frame(self.note_window, bg="#f0f8ff")
    tab2 = tk.Frame(self.note_window, bg="#f0f8ff")
    tab3 = tk.Frame(self.note_window, bg="#f0f8ff")
    self.note_window.add(tab1, text='検索項目Tab', padding=10)
    self.note_window.add(tab2, text='検索結果Tab', padding=10)
    self.note_window.add(tab3, text='検索履歴Tab', padding=10)
    self.note_window.pack(expand=1, fill='both')
    # 中分類ノートブック2
    self.note2_window = ttk.Notebook(tab1)
    # タブの作成
    tab4 = tk.Frame(self.note2_window, bg="#f0f8ff")
    tab5 = tk.Frame(self.note2_window, bg="#f0f8ff")
    tab6 = tk.Frame(self.note2_window, bg="#f0f8ff")
    tab7 = tk.Frame(self.note2_window, bg="#f0f8ff")
    self.note2_window.add(tab4, text='Section', padding=0)
    self.note2_window.add(tab5, text='Defect mode', padding=0)
    self.note2_window.add(tab6, text='Subject packaging', padding=0)
    self.note2_window.add(tab7, text='Subject line', padding=0)
    self.note2_window.pack(expand=1,pady=23,fill='both')
    #検索項目
    self.search = tk.Label(tab1, text="検索項目", bg="#f0f8ff")
    self.search.place(x=5, y=0)
    #検索結果
    self.search = tk.Label(tab2, text="検索結果", bg="#f0f8ff")
    self.search.place(x=5, y=0)
    #検索ログ
    self.search = tk.Label(tab3, text="検索ログ", bg="#f0f8ff")
    self.search.place(x=5, y=0)







    #ボタンの作成tab1
    self.view_btn = tk.Button(tab1, text='MQR全体表示', width=15, height=2, command=mqr_view,fg ="blue",bg="#f0f8ff")
    self.view_btn.place(x=1000, y=85)
    self.txt_btn = tk.Button(tab1, text='検索結果出力', width=15, height=2, command=lambda:self.loading(),fg ="blue",bg="#f0f8ff")
    self.txt_btn.place(x=1000, y=155)
    self.save_btn = tk.Button(tab1, text='検索条件保存', width=15, height=2, command=lambda:self.save_btn_click(Save),fg ="blue",bg="#f0f8ff")
    self.save_btn.place(x=1000, y=225)
    self.excel_btn = tk.Button(tab1, text='監査資料生成', width=15, height=2 , command=lambda:self.createfile(CreateAuditDoc),fg ="blue",bg="#f0f8ff")
    self.excel_btn.place(x=1000, y=295)

    #priorityチェックボタン
    self.priority = tk.Label(tab1, text="priority",fg ="blue",bg="#f0f8ff")
    self.priority.place(x=1020, y=345)
    self.priority_bln = tk.BooleanVar()
    self.priority_bln.set(False)
    priority_chk = tk.Checkbutton(tab1, variable=(self.priority_bln),bg="#f0f8ff")
    priority_chk.place(x=1050, y=345)
    self.priority = self.priority_bln.get()
    self.priority = tk.Label(tab1, text="該当",fg ="blue",bg="#f0f8ff")
    self.priority.place(x=1070, y=345)

    self.check_off_btn = tk.Button(tab1, text='チェックボタン全解除', width=15, height=2, command=lambda:self.checkbtn_click(False),fg ="blue",bg="#f0f8ff")
    self.check_off_btn.place(x=1000, y=385)
    self.check_on_btn = tk.Button(tab1, text='チェックボタン全選択', width=15, height=2, command=lambda:self.checkbtn_click(True),fg ="blue",bg="#f0f8ff")
    self.check_on_btn.place(x=1000, y=455)

    #ボタンの作成tab2
    self.save_btn = tk.Button(tab2, text='検索条件保存', width=15, height=2, command=lambda:self.save_btn_click(Save),fg ="blue",bg="#f0f8ff")
    self.save_btn.place(x=1000, y=225)

    #ボタンの作成tab3
    self.log_btn = tk.Button(tab3, text='ログファイル読み込み', width=15, height=2, command=lambda:self.log_btn_click(Search_log),fg ="blue",bg="#f0f8ff")
    self.log_btn.place(x=1000, y=225)


    #検索項目ウィンドウ
    #self.search = tk.Label(self.main, text="検索項目")
    #self.search.place(x=30, y=40)
    #大元のフレーム
    #self.search_window_frame = tk.Frame(self.main, bg="white")
    #self.search_window_frame.place(x=30,y=70, width=715, height=550)

    #キャンバス
    #self.search_window = tk.Canvas(self.main, bg="white")
    #self.search_window.place(x=30,y=70, width=700, height=535)


    #sectionフレーム
    #self.search_frame = tk.Frame(self.search_window, bg="white")
    #self.search_window.create_window((0,0), window=self.search_frame, anchor=tk.NW, width=1500, height=1500)

    

    #スクロール
    #self.search_ybar = tk.Scrollbar(self.search_window_frame, orient=tk.VERTICAL, command=self.search_window.yview)
    #self.search_xbar = tk.Scrollbar(self.search_window_frame, orient=tk.HORIZONTAL)
    #self.search_ybar.pack(side=tk.RIGHT, fill=tk.Y)
    #self.search_xbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    #各種要素設定
    #self.search_window.config(yscrollcommand=self.search_ybar.set, xscrollcommand=self.search_xbar.set)
    #self.search_window.config(scrollregion=(0,0,1500,1200))
    #情報反映スクロール(機能してない、恐らくコードがケンカしている:上田)
    #self.search_ybar.config(command=self.search_window.yview)
    #self.search_xbar.config(command=self.search_window.xview)
    #部品の動きをスクロールバーに反映させる
    #self.search_ybar["command"]=self.search_window.yview




    #sectionチェックボタン
    self.section = tk.Label(tab4, text="Section", bg="#f0f8ff")
    self.section.place(x=5, y=10)
    self.section_window = tk.Canvas(tab4, bg="white")
    self.section_window.place(x=0, y=35, width=950, height=490)
    self.section_ybar = tk.Scrollbar(self.section_window, orient=tk.VERTICAL)
    self.section_ybar.pack(side=tk.RIGHT, fill=tk.Y)
    self.section_ybar.config(command=self.section_window.yview)
    self.section_window.config(yscrollcommand=self.section_ybar.set)
    self.section_window.config(scrollregion=(0,0,1000,10000))
    
    self.check_off_btn = tk.Button(tab4, text='全解除', width=7, height=1, command=lambda:self.checksectionbtn_click(False),fg ="blue",bg="#f0f8ff")
    self.check_off_btn.place(x=50, y=5)
    self.check_on_btn = tk.Button(tab4, text='全選択', width=7, height=1, command=lambda:self.checksectionbtn_click(True),fg ="blue",bg="#f0f8ff")
    self.check_on_btn.place(x=110, y=5)

    for i in fd.section_list:
      section_bln = tk.BooleanVar()
      section_bln.set(False)
      self.section_bln_list.append(section_bln)

    for i, search_word in enumerate(fd.section_list):
      section_chk = tk.Checkbutton(self.section_window, variable=(self.section_bln_list[i]), text=search_word, bg="white")
      section_chk.place(x=20, y=-10+ 25*(i+1))



    #defectチェックボタン
    self.defect = tk.Label(tab5, text="Defect mode", width=10,bg="#f0f8ff")
    self.defect.place(x=5, y=10)
    self.defect_window = tk.Canvas(tab5, bg="white")
    self.defect_window.place(x=0, y=35, width=950, height=490)
    self.defect_window.config(scrollregion=(0,0,1000,10000))

    self.check_off_btn = tk.Button(tab5, text='全解除', width=7, height=1, command=lambda:self.checkdefectbtn_click(False),fg ="blue",bg="#f0f8ff")
    self.check_off_btn.place(x=80, y=5)
    self.check_on_btn = tk.Button(tab5, text='全選択', width=7, height=1, command=lambda:self.checkdefectbtn_click(True),fg ="blue",bg="#f0f8ff")
    self.check_on_btn.place(x=140, y=5)

    for i in fd.defect_list:
      defect_bln = tk.BooleanVar()
      defect_bln.set(False)
      self.defect_bln_list.append(defect_bln)

    for i, search_word in enumerate(fd.defect_list):
      defect_chk = tk.Checkbutton(self.defect_window, variable=(self.defect_bln_list[i]), text=search_word, bg="white")
      defect_chk.place(x=20, y=-10+ 25*(i+1))



    #packagingチェックボタン
    self.packaging = tk.Label(tab6, text="Subjected packaging", bg="#f0f8ff")
    self.packaging.place(x=5, y=10)
    self.packaging_window = tk.Canvas(tab6, bg="white")
    self.packaging_window.place(x=0, y=35, width=950, height=490)
    self.packaging_window.config(scrollregion=(0,0,1000,10000))

    self.check_off_btn = tk.Button(tab6, text='全解除', width=7, height=1, command=lambda:self.checkpackagingbtn_click(False),fg ="blue",bg="#f0f8ff")
    self.check_off_btn.place(x=120, y=5)
    self.check_on_btn = tk.Button(tab6, text='全選択', width=7, height=1, command=lambda:self.checkpackagingbtn_click(True),fg ="blue",bg="#f0f8ff")
    self.check_on_btn.place(x=180, y=5)

    for i in fd.packaging_list:
      packaging_bln = tk.BooleanVar()
      packaging_bln.set(False)
      self.packaging_bln_list.append(packaging_bln)

    for i, search_word in enumerate(fd.packaging_list):
      packaging_chk = tk.Checkbutton(self.packaging_window, variable=(self.packaging_bln_list[i]), text=search_word, bg="white")
      packaging_chk.place(x=20, y=-10+ 25*(i+1))





    #lineチェックボタン
    self.line = tk.Label(tab7, text="Subjected line", bg="#f0f8ff")
    self.line.place(x=5, y=10)
    self.line_window = tk.Canvas(tab7, bg="white")
    self.line_window.place(x=0, y=35, width=950, height=490)
    self.line_window.config(scrollregion=(0,0,1000,10000))

    self.check_off_btn = tk.Button(tab7, text='全解除', width=7, height=1, command=lambda:self.checklinebtn_click(False),fg ="blue",bg="#f0f8ff")
    self.check_off_btn.place(x=85, y=5)
    self.check_on_btn = tk.Button(tab7, text='全選択', width=7, height=1, command=lambda:self.checklinebtn_click(True),fg ="blue",bg="#f0f8ff")
    self.check_on_btn.place(x=145, y=5)

    for i in fd.line_list:
      line_bln = tk.BooleanVar()
      line_bln.set(False)
      self.line_bln_list.append(line_bln)

    for i, search_word in enumerate(fd.line_list):
      line_chk = tk.Checkbutton(self.line_window, variable=(self.line_bln_list[i]), text=search_word, bg="white")
      line_chk.place(x=20, y=-10+ 25*(i+1))




    #priorityチェックボタン
    #self.priority = tk.Label(self.main, text="priority")
    #self.priority.place(x=770, y=270)
    
    #self.priority_bln = tk.BooleanVar()
    #self.priority_bln.set(False)
  
    #priority_chk = tk.Checkbutton(self.main, variable=(self.priority_bln))
    #priority_chk.place(x=820, y=270)
    #self.priority = self.priority_bln.get()


   #検索結果ウィンドウ
    self.result = tk.Label(tab2, text="検索結果", bg="#f0f8ff")
    self.result.place(x=5, y=0)
    self.result_window_frame = tk.Frame(tab2)
    self.result_window_frame.place(x=0,y=20, width=950, height=490)
    self.result_window = tk.Canvas(tab2, bg="white")
    self.result_window.place(x=0,y=25, width=930, height=490)
    self.result_ybar = tk.Scrollbar(self.result_window_frame, orient=tk.VERTICAL)
    self.result_ybar.pack(side=tk.RIGHT, fill=tk.Y)
    self.result_ybar.config(command=self.result_window.yview)
    self.result_window.config(yscrollcommand=self.result_ybar.set)
    self.result_window.config(scrollregion=(0,0,1000,10000))
    self.result_frame = tk.Frame(self.result_window, bg="white")
    self.result_window.create_window((0,0), window=self.result_frame, anchor=tk.NW, width=305, height=10000)


    #検索ログウィンドウ
    self.log = tk.Label(tab3, text="検索ログ", bg="#f0f8ff")
    self.log.place(x=5, y=0)
    self.log_window_frame = tk.Frame(tab3)
    self.log_window_frame.place(x=0, y=20, width=950, height=490)
    self.log_window = tk.Canvas(tab3, bg="white")
    self.log_window.place(x=0, y=25, width=930, height=490)
    self.log_ybar = tk.Scrollbar(self.log_window_frame, orient=tk.VERTICAL)
    self.log_ybar.pack(side=tk.RIGHT, fill=tk.Y)
    self.log_ybar.config(command=self.log_window.yview)
    self.log_window.config(yscrollcommand=self.log_ybar.set)
    self.log_window.config(scrollregion=(0,0,1000,1000))
    self.log_frame = tk.Frame(self.log_window, bg="white")
    self.log_window.create_window((0,0), window=self.log_frame, anchor=tk.NW, width=305, height=10000)
    


    #画面表示
    self.main.mainloop()