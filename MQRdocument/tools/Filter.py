# coding: UTF-8
import os
import bs4
from natsort import natsorted

class Filter:
  
  # マニュアルデータが置いてあるディレクトリパス
  MANUAL_PATH:'str' = r'C:\MQRdocument\manual_data'

  # スラッシュ、環境によって違うため
  SLASH:'str' = '/'

  # マニュアルファイルの名前に含まれている文字列
  KEYWORD:'str' = r'Manual'

  # マニュアルのファイル名を格納するリスト
  manual_file_list:'list[str]' = []
  #Section検索をかけた後のマニュアル名を格納するリスト
  manual_file_list2:'list[str]' = []

  # htmlをプログラムで扱いやすくするためにBeautifulSoupで変換したものを保持するリスト
  soup_list:'list[bs4.BeautifulSoup]' = []
  #Section検索をかけた後のsoup_list
  soup_list2:'list[bs4.BeautifulSoup]' = []

  # 検索キーワード
  search_word_list1:'list[str]' = []
  search_word_list2:'list[str]' = []
  search_word_list3:'list[str]' = []
  search_word_list4:'list[str]' = []
  search_word_list5:'list[str]' = []
  search_word_list6:'list[str]' = []

  def log_delete(self):
    self.soup_list2.clear()
    self.manual_file_list2.clear()



  def __init__(self):   
    # "Manual"と4つの"-"を含むファイル名(Manual-x-x-x-x)を読み取りリストに加える
    natsorted_list = natsorted(os.listdir(self.MANUAL_PATH))
    for manual_file in natsorted_list:
      if self.KEYWORD in manual_file and manual_file.count("-") == 4:
        self.manual_file_list.append(manual_file)


  # マニュアルのファイル名のリストからhtmlファイルをプログラム上で扱える形式に変換し、その一つ一つを入れたリストを返す関数  
  def get_soup_list(self, manual_file_list:'list[str]') -> 'list[bs4.BeautifulSoup]':
    print(manual_file_list)
    for manual_file in manual_file_list:
      soup:'bs4.BeautifulSoup' = bs4.BeautifulSoup(open(self.MANUAL_PATH + self.SLASH + manual_file , encoding='UTF-8' ), 'html.parser')
      self.soup_list.append(soup)
    return self.soup_list

  def get_soup_list2(self, manual_file_list:'list[str]') -> 'list[bs4.BeautifulSoup]':
    print(manual_file_list)
    for manual_file in manual_file_list:
      soup:'bs4.BeautifulSoup' = bs4.BeautifulSoup(open(self.MANUAL_PATH + self.SLASH + manual_file , encoding='UTF-8' ), 'html.parser')
      self.soup_list2.append(soup)
    return self.soup_list2


  # tdで抽出したBeautifulSoupの配列を受け取り、空白文字を除去したものを返す関数
  def format_data(self, soup_tags: bs4.element.ResultSet) -> 'list[str]':
    #find_allで取得した情報からtlist格納用の文字列リストを返す
    tmp_text_list:'list[str]' = []
    for inner_tag in soup_tags:
      text:'str' = ''
      text = inner_tag.get_text()
      text = text.replace('\n', '').replace(' ', '').replace('\u3000', '')
      if len(text)>0:
        tmp_text_list.append(text)

    #return_text_list:'list[str]' = [i for i in tmp_text_list if i != '']
    return_text_list = tmp_text_list
    return return_text_list  

  # フィルタリングにヒットしたかどうか判定する関数
  def filter_flag(self, text_list:'list[str]', search_word_list:'list[str]') -> bool:
    flag:bool = False

    for search_word in search_word_list :
      for text in text_list :
        if search_word.replace(' ', '') in text :
          flag = True

    return flag


  def get_div3_title(self, div3_no:'str') -> 'str' :

    natsorted_list = natsorted(os.listdir(self.MANUAL_PATH))
    div3_file_list:'list[str]' = []
    div3_soup_list:'list[str]' = []

    for manual_file in natsorted_list:
      if self.KEYWORD in manual_file and manual_file.count("-") == 3:
        div3_file_list.append(manual_file) 

    for manual_file in div3_file_list:
      soup:'bs4.BeautifulSoup' = bs4.BeautifulSoup(open(self.MANUAL_PATH + self.SLASH + manual_file , encoding='UTF-8' ), 'html.parser')
      div3_soup_list.append(soup)

    for soup in div3_soup_list:
      div3_title:'str' = soup.find('div', {'class':'sectionDiv3_title'}).get_text().replace('\n', '').replace('\u3000', ' ')
      if div3_no in div3_title:
        return div3_title


  # Sectionの検索ワードを元に情報を出力できるように整形、インスタンス変数に格納する関数
  def filter_by_section(self, selected_words):  
    print('1開始')
    
    # Guiファイルからチェックの入ったテキスト情報を受け取る
    self.search_word_list1:'list[str]' = selected_words
    print(self.search_word_list1)


    # マニュアルのファイル名リストからBeautifulSoupのリストを作る
    if self.soup_list == []:
      print(self.manual_file_list)
      self.soup_list = self.get_soup_list(self, self.manual_file_list)

    self.section_filtered_list:'list[list[str]]' = []

    for i, soup in enumerate(self.soup_list):
      soup_tag:'bs4.element.Tag' = soup.find_all('div', {'class':'sectionDiv4_title'}) # 一つ一つのマニュアルファイル(Manual-x-x-x-x.html)のtdタグ要素を取得
      text_list:'list[str]' = self.format_data(self, soup_tag)

      #text_listの中に検索ワードが含まれているか判定するためのフラグ
      flag:bool = self.filter_flag(self, text_list, self.search_word_list1)

      if flag :
        
        div4_title:'str' = soup.find('div', {'class':'sectionDiv4_title'}).get_text().replace('\n', '').replace('\u3000', ' ')
        idx = div4_title.find(' ')
        div4_no = div4_title[:idx]
        idx2 = div4_no.rfind('.')
        div3_no = div4_no[:idx2]
        div3_title:'str' = self.get_div3_title(self, div3_no)

        manual_name = div3_title + ' > ' + div4_title
        self.section_filtered_list.append([manual_name, self.manual_file_list[i]])
    
    print('1終了')
    if len(self.section_filtered_list)>0:
      for x in self.section_filtered_list:
        self.manual_file_list2.append(x[1])
      print(self.manual_file_list2)
    else:
      self.manual_file_list2=self.manual_file_list
    

    return self.section_filtered_list
  


  # Defect modeの検索ワードを元に情報を出力できるように整形、インスタンス変数に格納する関数
  def filter_by_defect(self, selected_words):
    print('2開始')
    # Guiファイルからチェックの入ったテキスト情報を受け取る
    self.search_word_list2:'list[str]' = selected_words
    print(self.manual_file_list2)
    

    # マニュアルのファイル名リストからBeautifulSoupのリストを作る
    if len(self.manual_file_list2)>0:
      if self.soup_list2 == []:
        self.soup_list2 = self.get_soup_list2(self, self.manual_file_list2)
    else :
      if self.soup_list2 == []:
        self.soup_list2 = self.get_soup_list2(self, self.manual_file_list)


    self.defect_filtered_list:'list[list[str]]' = []
    print(len(self.soup_list2))
    for i, soup in enumerate(self.soup_list2):
      soup_tag:'bs4.element.Tag' = soup.find_all('td') # 一つ一つのマニュアルファイル(Manual-x-x-x-x.html)のtdタグ要素を取得
      text_list:'list[str]' = self.format_data(self, soup_tag)

      #text_listの中に検索ワードが含まれているか判定するためのフラグ
      flag:bool = self.filter_flag(self, text_list, self.search_word_list2)

      if flag :

        div4_title:'str' = soup.find('div', {'class':'sectionDiv4_title'}).get_text().replace('\n', '').replace('\u3000', ' ')
        idx = div4_title.find(' ')
        div4_no = div4_title[:idx]
        idx2 = div4_no.rfind('.')
        div3_no = div4_no[:idx2]
        div3_title:'str' = self.get_div3_title(self, div3_no)

        manual_name = div3_title + ' > ' + div4_title
        self.defect_filtered_list.append([manual_name, self.manual_file_list2[i]])
    
    print('2終了')

    return self.defect_filtered_list

  
  # Subjected packagingの検索ワードを元に情報を出力できるように整形、インスタンス変数に格納する関数
  def filter_by_packaging(self, selected_words):
    print('3開始')
    self.search_word_list3:'list[str]' = selected_words
   
    print(self.search_word_list3)
    

    if len(self.manual_file_list2)>0:
      if self.soup_list2 == []:
        self.soup_list2 = self.get_soup_list2(self, self.manual_file_list2)
    else :
      if self.soup_list2 == []:
        self.soup_list2 = self.get_soup_list2(self, self.manual_file_list)

    self.packaging_filtered_list:'list[list[str]]' = []

    for i, soup in enumerate(self.soup_list2):
      soup_tag:'bs4.element.Tag' = soup.find_all('td') # 一つ一つのマニュアルファイル(Manual-x-x-x-x.html)のtdタグ要素を取得
      text_list:'list[str]' = self.format_data(self, soup_tag)
      
      flag:bool = self.filter_flag(self, text_list, self.search_word_list3)

      if flag :
       
        div4_title:'str' = soup.find('div', {'class':'sectionDiv4_title'}).get_text().replace('\n', '').replace('\u3000', ' ')
        idx = div4_title.find(' ')
        div4_no = div4_title[:idx]
        idx2 = div4_no.rfind('.')
        div3_no = div4_no[:idx2]
        div3_title:'str' = self.get_div3_title(self, div3_no)

        manual_name = div3_title + ' > ' + div4_title
        self.packaging_filtered_list.append([manual_name, self.manual_file_list2[i]])

    print('3終了')

    return self.packaging_filtered_list
 

  # Subjected lineの検索ワードを元に情報を出力できるように整形、インスタンス変数に格納する関数
  def filter_by_line(self, selected_words):
    print('4開始')
    self.search_word_list4:'list[str]' = selected_words
    print(self.search_word_list4)
    

    if len(self.manual_file_list2)>0:
      if self.soup_list2 == []:
        self.soup_list2 = self.get_soup_list2(self, self.manual_file_list2)
    else :
      if self.soup_list2 == []:
        self.soup_list2 = self.get_soup_list2(self, self.manual_file_list)

    self.line_filtered_list:'list[list[str]]' = []

    for i, soup in enumerate(self.soup_list2):
      soup_tag:'bs4.element.Tag' = soup.find_all('td') # 一つ一つのマニュアルファイル(Manual-x-x-x-x.html)のtdタグ要素を取得
      text_list:'list[str]' = self.format_data(self, soup_tag)
      
      flag:bool = self.filter_flag(self, text_list, self.search_word_list4)

      if flag :
        
        div4_title:'str' = soup.find('div', {'class':'sectionDiv4_title'}).get_text().replace('\n', '').replace('\u3000', ' ')
        idx = div4_title.find(' ')
        div4_no = div4_title[:idx]
        idx2 = div4_no.rfind('.')
        div3_no = div4_no[:idx2]
        div3_title:'str' = self.get_div3_title(self, div3_no)

        manual_name = div3_title + ' > ' + div4_title
        self.line_filtered_list.append([manual_name, self.manual_file_list2[i]])
    
    print('4終了')
        
    return self.line_filtered_list


  def filter_by_All_line(self):
    print('5開始')
    self.search_word_list5.clear()
    self.search_word_list5.append('All lines') 
    print(self.search_word_list5)
    

    if len(self.manual_file_list2)>0:
      if self.soup_list2 == []:
        self.soup_list2 = self.get_soup_list2(self, self.manual_file_list2)
    else :
      if self.soup_list2 == []:
        self.soup_list2 = self.get_soup_list2(self, self.manual_file_list)

    self.all_line_filtered_list:'list[list[str]]' = []

    for i, soup in enumerate(self.soup_list2):
      soup_tag:'bs4.element.Tag' = soup.find_all('td') # 一つ一つのマニュアルファイル(Manual-x-x-x-x.html)のtdタグ要素を取得
      text_list:'list[str]' = self.format_data(self, soup_tag)
      
      flag:bool = self.filter_flag(self, text_list, self.search_word_list5)

      if flag :
        
        div4_title:'str' = soup.find('div', {'class':'sectionDiv4_title'}).get_text().replace('\n', '').replace('\u3000', ' ')
        idx = div4_title.find(' ')
        div4_no = div4_title[:idx]
        idx2 = div4_no.rfind('.')
        div3_no = div4_no[:idx2]
        div3_title:'str' = self.get_div3_title(self, div3_no)

        manual_name = div3_title + ' > ' + div4_title
        self.all_line_filtered_list.append([manual_name, self.manual_file_list2[i]])
    
    print('5終了')
        
    return self.all_line_filtered_list

  
  def filter_by_All_packaging(self):
    print('6開始')
    self.search_word_list6.clear()
    self.search_word_list6.append('All packaging')
    print(self.search_word_list6)
    

    if len(self.manual_file_list2)>0:
      if self.soup_list2 == []:
        self.soup_list2 = self.get_soup_list2(self, self.manual_file_list2)
    else :
      if self.soup_list2 == []:
        self.soup_list2 = self.get_soup_list2(self, self.manual_file_list)

    self.all_packaging_filtered_list:'list[list[str]]' = []

    for i, soup in enumerate(self.soup_list2):
      soup_tag:'bs4.element.Tag' = soup.find_all('td') # 一つ一つのマニュアルファイル(Manual-x-x-x-x.html)のtdタグ要素を取得
      text_list:'list[str]' = self.format_data(self, soup_tag)
      
      flag:bool = self.filter_flag(self, text_list, self.search_word_list6)

      if flag :
        
        div4_title:'str' = soup.find('div', {'class':'sectionDiv4_title'}).get_text().replace('\n', '').replace('\u3000', ' ')
        idx = div4_title.find(' ')
        div4_no = div4_title[:idx]
        idx2 = div4_no.rfind('.')
        div3_no = div4_no[:idx2]
        div3_title:'str' = self.get_div3_title(self, div3_no)

        manual_name = div3_title + ' > ' + div4_title
        self.all_packaging_filtered_list.append([manual_name, self.manual_file_list2[i]])
    
    print('6終了')
        
    return self.all_packaging_filtered_list  

  

filter = Filter()    


    