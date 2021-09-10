# coding: UTF-8
import tkinter as tk
from tkinter import messagebox
import tkinter

class Login():
    def __init__(self):
        self.main = tk.Tk()
        self.main.title("ログインページ")
        self.main.geometry("350x150")
        

        def login_button_click():
            self.password = self.pass_form.get()
            if self.password == "suntory":
                self.judge = "success"
                
                self.main.destroy()
            else:
                messagebox.showerror('エラー', 'パスワードが一致しません')
                #失敗したらテキストボックスの中身を削除するコード(使用するのであればコメントアウトを外すだけで使用可能)
                # self.pass_form.delete(0,tkinter.END)

        self.pass_label = tk.Label(self.main, text="パスワード")
        self.pass_label.place(x=40, y=40)

        self.pass_form = tk.Entry(self.main, show="*", width=30)
        self.pass_form.place(x=100, y=40)

        self.login_button = tk.Button(self.main, text="ログイン", width=15, command=login_button_click)
        self.login_button.bind("<Return>", lambda event:login_button_click())
        self.login_button.place(x=100, y=80)

        self.main.mainloop()
