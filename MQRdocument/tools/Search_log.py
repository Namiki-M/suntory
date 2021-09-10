# coding: UTF-8

class Search_log():
	
	log_file = r'C:\MQRdocument\search_log.txt'	

	def get_search_paramaters(self):
		# 検索履歴.txtの読み取り
		f = open(self.log_file, 'r', encoding='utf-8')
		self.search_paramaters_list = eval(f.read())
		f.close()

		return self.search_paramaters_list

search_log = Search_log()



  






