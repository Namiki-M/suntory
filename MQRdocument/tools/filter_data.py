# coding: UTF-8
import bs4
import os
from natsort import natsorted

MANUAL_PATH:'str' = r'C:\MQRdocument\manual_data'
SLASH:'str' = '/'
KEYWORD:'str' = r'Manual'
manual_file_list:'list[str]' = []
soup_list:'list[bs4.BeautifulSoup]' = []
section_list = []

natsorted_list = natsorted(os.listdir(MANUAL_PATH))

for manual_file in natsorted_list:
  if KEYWORD in manual_file and manual_file.count("-") == 3:
    manual_file_list.append(manual_file)

for manual_file in manual_file_list:
  soup:'bs4.BeautifulSoup' = bs4.BeautifulSoup(open(MANUAL_PATH + SLASH + manual_file , encoding='UTF-8' ), 'html.parser')
  soup_list.append(soup)

for soup in soup_list:
  soup_tag:'bs4.element.Tag' = soup.find('div', {'class':'sectionDiv3_title'}).get_text().replace('\n', '')
  section_list.append(soup_tag)


defect_list = [
                'Label error', 'Different packaging', 'Low or excessive filling', 'Lack of products in secondary packaging', 
                'Usage of restricted ingredients/packaging', 'Others (violation of law)', 
                'Microbe contamination', 'Foreign material contamination', 'Mixing different liquid',
                'Allergen contamination', 'Organoleptic defect', 'Sealing defect', 
                'BBD coding defect', 'Scratched packaging which may cause injury', 'Packaging appearance defect', 
                'Difficult to open', 'Shipping non-conforming products or test sample', 'Others',
              ]


packaging_list = ['PET', 'Can', 'Glass bottle', 'Cup', 'Pouch', 'Paper pack']


line_list = ['Cold filling', 'Hot filling', 'Aseptic filling', 'Aseptic filling (paper pack)', 'Retort']
