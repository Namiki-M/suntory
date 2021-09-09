# coding: UTF-8
import tkinter as tk
from tkinter import messagebox

class Save():

	log_file = r'C:\MQRdocument\search_log.txt'	

	info_title:'str' = ""
	selected_section:'list[str]' = []
	selected_defect:'list[str]' = []
	selected_packaging:'list[str]' = []
	selected_line:'list[str]' = []

	def save_search_paramaters(self, selected_section, selected_defect, selected_packaging, selected_line):

	  	# 検索履歴.txtの読み取り
		f = open(self.log_file, 'r', encoding='utf-8')
		self.search_paramaters_list = eval(f.read())
		f.close()

		# ポップアップによる確認、名前付け
		self.main = tk.Toplevel()
		self.main.title("検索条件保存")
		self.main.geometry("400x200")


		selected_section2 = []
		for r in selected_section:
    			if r[len(r)-1:len(r)] == '.':
        			r = r.rstrip('.')
        			selected_section2.append(r)
				

		self.selected_section:'list[str]' = selected_section2
		self.selected_defect:'list[str]' = selected_defect
		self.selected_packaging:'list[str]' = selected_packaging
		self.selected_line:'list[str]' = selected_line

		def save_button_click():
			# フォームに入力されたテキストを取得
			self.info_title = self.title_form.get()

			if self.info_title == "":
				messagebox.showerror('エラー', '名前を入力してください')
			else:	
				# 保存する条件を配列に格納
				search_paramaters = []
				search_paramaters.append(self.info_title)
				search_paramaters.append(self.selected_section)
				search_paramaters.append(self.selected_defect)
				search_paramaters.append(self.selected_packaging)
				search_paramaters.append(self.selected_line)

				if len(self.search_paramaters_list) <= 4 :
					self.search_paramaters_list.append(search_paramaters)
				else:
					ret = messagebox.askyesno('確認', 'ログファイルに保存できる検索履歴は20件です。\n最古の履歴を削除してもよろしいですか？')
					if ret == True :
						self.search_paramaters_list.pop(0)
						self.search_paramaters_list.append(search_paramaters)	

				# 検索履歴.txtへの書き込み
				f = open(self.log_file, 'w', encoding='utf-8')
				f.write(str(self.search_paramaters_list))
				f.close()
				messagebox.showinfo('メッセージ','検索履歴を保存しました')
				self.main.destroy()	

		def cancel_button_click():
			self.main.destroy()  	

		self.pass_label = tk.Label(self.main, text="保存する情報に名前をつけてください")
		self.pass_label.place(x=40, y=40)

		self.title_form = tk.Entry(self.main, width=50)
		self.title_form.place(x=40, y=80)

		self.save_button = tk.Button(self.main, text="保存", width=12, command=save_button_click)
		self.save_button.place(x=40, y=120)
		self.save_button.bind("<Return>",lambda event:save_button_click())
		
		self.cancel_button = tk.Button(self.main, text="キャンセル", width=12, command=cancel_button_click)
		self.cancel_button.place(x=150, y=120)
		self.cancel_button.bind("<Return>",lambda event:cancel_button_click())

		self.main.mainloop()
save = Save()


  






