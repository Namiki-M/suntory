# coding: UTF-8
from tools.Login import Login
from tools.Gui import Gui

class Main():
  def __init__(self):
    self.login = Login()  

    if self.login.judge == "success":
      self.gui = Gui()  

if __name__ == "__main__":
    main = Main()