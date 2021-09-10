from bs4 import BeautifulSoup
from _ast import Pass

# マニュアルファイルから読み取ったデータの受け渡しクラス。
# 各変数に対し、getter、setterを用意する
class ManualParam():
    
    # Section情報。1.1.1 はんまはんま　の情報。対象マニュアルにつき1つ。E列への書き込み対象。
    section:str = ""

    # SubSection情報。1.1.1.1 はんまかんま の情報。対象マニュアルそのもの。F列への書き込み対象。
    subSection:str = ""
    
    # SubSubSection情報。a. さんまさんま の情報。対象マニュアルそのもの。G列への書き込み対象。
    # ヒットした内容のみの情報とする。
    subsubSection:str = ""
    
    # purpose情報。Subsubsectionと対の情報。H列への書き込み対象。
    purpose:str = ""
    
    # B列の情報。subsubSectionと対。
    subjectedDefectMode:str = ""
    
    # C列の情報。subsubSectionと対。
    subjectedPackaging:str = ""
    
    # D列の情報。subsubSectionと対。
    subjectedLine:str = ""
    
    howToAchieve:'list[str]' = []
    howToAchievePriority:'list[str]' = []
    
    task1AllPriority:bool = False
    task2AllPriority:bool = False
    task3AllPriority:bool = False
    task4AllPriority:bool = False
    task5AllPriority:bool = False
    task6AllPriority:bool = False
    task7AllPriority:bool = False
    task8AllPriority:bool = False
    
    task1Procedure:'list[str]' = []
    task1Frequency:'list[str]' = []
    task1Operating:'list[str]' = []
    task2Procedure:'list[str]' = []
    task2Frequency:'list[str]' = []
    task2Operating:'list[str]' = []
    task3Procedure:'list[str]' = []
    task3Frequency:'list[str]' = []
    task3Operating:'list[str]' = []
    task4Procedure:'list[str]' = []
    task4Frequency:'list[str]' = []
    task4Operating:'list[str]' = []
    task5Procedure:'list[str]' = []
    task5Frequency:'list[str]' = []
    task5Operating:'list[str]' = []
    task6Procedure:'list[str]' = []
    task6Frequency:'list[str]' = []
    task6Operating:'list[str]' = []
    task7Procedure:'list[str]' = []
    task7Frequency:'list[str]' = []
    task7Operating:'list[str]' = []
    task8Procedure:'list[str]' = []
    task8Frequency:'list[str]' = []
    task8Operating:'list[str]' = []
    
    task1ChildPriority:'list[str]' = []
    task2ChildPriority:'list[str]' = []
    task3ChildPriority:'list[str]' = []
    task4ChildPriority:'list[str]' = []
    task5ChildPriority:'list[str]' = []
    task6ChildPriority:'list[str]' = []
    task7ChildPriority:'list[str]' = []
    task8ChildPriority:'list[str]' = []
    
    task1OutputCnt:int = 0
    task2OutputCnt:int = 0
    task3OutputCnt:int = 0
    task4OutputCnt:int = 0
    task5OutputCnt:int = 0
    task6OutputCnt:int = 0
    task7OutputCnt:int = 0
    task8OutputCnt:int = 0
    
    #===========================================================================
    # 検索条件
    #===========================================================================
    selectedDefectMode:str = ""
    selectedPackaging:str = ""
    selectedLine:str = ""
    selectedSection:str = ""
    priorityOnly:str = ""
    
    # コンストラクタ
    def __init__(self):
        print("ManualParam START")
        
    # クラス変数の初期化
    # 繰り返し書き込む項目のみの初期化とする。
    def clearAllMember(self):
        self.section = ""
        self.subSection = ""
        self.subsubSection = ""
        self.purpose = ""
        self.subjectedDefectMode = ""
        self.subjectedPackaging = ""
        self.subjectedLine = ""
        
        
    #===========================================================================
    # setter定義
    #===========================================================================
    
    # sectionSetter
    def set_section(self, val):
        self.section = val

    # subSectionSetter
    def set_subSection(self, val):
        self.subSection = val

    # subsubSectionSetter
    def set_subsubSection(self, val):
        self.subsubSection = val
    
    # purposeSetter
    def set_purpose(self, val):
        self.purpose = val
    
    # subjectedDefectModeSetter 
    def set_subjectedDefectMode(self,val):
        self.subjectedDefectMode = val

    # subjectedPackagingSetter 
    def set_subjectedPackaging(self,val):
        self.subjectedPackaging = val
    
    # subjectedLineSetter 
    def set_subjectedLine(self,val):
        self.subjectedLine = val
    
    def set_selectedDefectMode(self,val):
        self.selectedDefectMode = val
    
    def set_selectedPackaging(self,val):
        self.selectedPackaging = val

    def set_selectedLine(self,val):
        self.selectedLine = val
        
    def set_selectedSection(self,val):
        self.selectedSection = val
        
    def set_priorityOnly(self,val):
        self.priorityOnly = val
    
    def set_howToAchieve(self,val):
        self.howToAchieve = val
        
    def set_howToAchievePriority(self,val):
        self.howToAchievePriority = val

    def set_task1AllPriority(self,val):
        self.task1AllPriority = val

    def set_task1Procedure(self,val):
        self.task1Procedure = val
    
    def set_task1Frequency(self,val):
        self.task1Frequency = val
    
    def set_task1Operating(self,val):
        self.task1Operating = val
        
    def set_task2AllPriority(self,val):
        self.task2AllPriority = val
    
    def set_task2Procedure(self,val):
        self.task2Procedure = val
    
    def set_task2Frequency(self,val):
        self.task2Frequency = val
    
    def set_task2Operating(self,val):
        self.task2Operating = val
        
    def set_task3AllPriority(self,val):
        self.task3AllPriority = val
    
    def set_task3Procedure(self,val):
        self.task3Procedure = val
    
    def set_task3Frequency(self,val):
        self.task3Frequency = val
    
    def set_task3Operating(self,val):
        self.task3Operating = val
        
    def set_task4AllPriority(self,val):
        self.task4AllPriority = val
    
    def set_task4Procedure(self,val):
        self.task4Procedure = val
    
    def set_task4Frequency(self,val):
        self.task4Frequency = val
    
    def set_task4Operating(self,val):
        self.task4Operating = val
        
    def set_task5AllPriority(self,val):
        self.task5AllPriority = val
    
    def set_task5Procedure(self,val):
        self.task5Procedure = val
    
    def set_task5Frequency(self,val):
        self.task5Frequency = val
    
    def set_task5Operating(self,val):
        self.task5Operating = val
        
    def set_task6AllPriority(self,val):
        self.task6AllPriority = val
    
    def set_task6Procedure(self,val):
        self.task6Procedure = val
    
    def set_task6Frequency(self,val):
        self.task6Frequency = val
    
    def set_task6Operating(self,val):
        self.task6Operating = val
        
    def set_task7AllPriority(self,val):
        self.task7AllPriority = val
    
    def set_task7Procedure(self,val):
        self.task7Procedure = val
    
    def set_task7Frequency(self,val):
        self.task7Frequency = val
    
    def set_task7Operating(self,val):
        self.task7Operating = val
        
    def set_task8AllPriority(self,val):
        self.task7AllPriority = val
    
    def set_task8Procedure(self,val):
        self.task8Procedure = val
    
    def set_task8Frequency(self,val):
        self.task8Frequency = val
    
    def set_task8Operating(self,val):
        self.task8Operating = val

    def set_task1ChildPriority(self,val):
        self.task1ChildPriority = val

    def set_task2ChildPriority(self,val):
        self.task2ChildPriority = val

    def set_task3ChildPriority(self,val):
        self.task3ChildPriority = val

    def set_task4ChildPriority(self,val):
        self.task4ChildPriority = val

    def set_task5ChildPriority(self,val):
        self.task5ChildPriority = val

    def set_task6ChildPriority(self,val):
        self.task6ChildPriority = val

    def set_task7ChildPriority(self,val):
        self.task7ChildPriority = val

    def set_task8ChildPriority(self,val):
        self.task8ChildPriority = val
        
    def set_task1OutputCnt(self,val):
        self.task1OutputCnt = val

    def set_task2OutputCnt(self,val):
        self.task2OutputCnt = val

    def set_task3OutputCnt(self,val):
        self.task3OutputCnt = val

    def set_task4OutputCnt(self,val):
        self.task4OutputCnt = val

    def set_task5OutputCnt(self,val):
        self.task5OutputCnt = val

    def set_task6OutputCnt(self,val):
        self.task6OutputCnt = val

    def set_task7OutputCnt(self,val):
        self.task7OutputCnt = val

    def set_task8OutputCnt(self,val):
        self.task8OutputCnt = val
        
    #===========================================================================
    # getter定義
    #===========================================================================
    def get_section(self):
        return self.section
    
    def get_subSection(self):
        return self.subSection
    
    def get_subsubSection(self):
        return self.subsubSection
    
    def get_selectedSection(self):
        return self.selectedSection

    def get_selectedDefectMode(self):
        return self.selectedDefectMode
    
    def get_selectedPackaging(self):
        return self.selectedPackaging

    def get_selectedLine(self):
        return self.selectedLine
    
    def get_purpose(self):
        return self.purpose
    
    def get_subjectedDefectMode(self):
        return self.subjectedDefectMode
    
    def get_subjectedPackaging(self):
        return self.subjectedPackaging
    
    def get_subjectedLine(self):
        return self.subjectedLine
    
    def get_priorityOnly(self):
        return self.priorityOnly
    
    def get_howToAchieve(self):
        return self.howToAchieve

    def get_howToAchievePriority(self):
        return self.howToAchievePriority
    
    def get_task1AllPriority(self):
        return self.task1AllPriority
    
    def get_task1Procedure(self):
        return self.task1Procedure

    def get_task1Frequency(self):
        return self.task1Frequency
    
    def get_task1Operating(self):
        return self.task1Operating
    
    def get_task2AllPriority(self):
        return self.task2AllPriority
    
    def get_task2Procedure(self):
        return self.task2Procedure
    
    def get_task2Frequency(self):
        return self.task2Frequency
    
    def get_task2Operating(self):
        return self.task2Operating
    
    def get_task3AllPriority(self):
        return self.task3AllPriority
    
    def get_task3Procedure(self):
        return self.task3Procedure
    
    def get_task3Frequency(self):
        return self.task3Frequency
    
    def get_task3Operating(self):
        return self.task3Operating
    
    def get_task4AllPriority(self):
        return self.task4AllPriority
    
    def get_task4Procedure(self):
        return self.task4Procedure
    
    def get_task4Frequency(self):
        return self.task4Frequency
    
    def get_task4Operating(self):
        return self.task4Operating
    
    def get_task5AllPriority(self):
        return self.task5AllPriority
    
    def get_task5Procedure(self):
        return self.task5Procedure
    
    def get_task5Frequency(self):
        return self.task5Frequency
    
    def get_task5Operating(self):
        return self.task5Operating
    
    def get_task6AllPriority(self):
        return self.task6AllPriority
    
    def get_task6Procedure(self):
        return self.task6Procedure
    
    def get_task6Frequency(self):
        return self.task6Frequency
    
    def get_task6Operating(self):
        return self.task6Operating

    def get_task7AllPriority(self):
        return self.task7AllPriority
    
    def get_task7Procedure(self):
        return self.task7Procedure
    
    def get_task7Frequency(self):
        return self.task7Frequency
    
    def get_task7Operating(self):
        return self.task7Operating
    
    def get_task8AllPriority(self):
        return self.task8AllPriority
    
    def get_task8Procedure(self):
        return self.task8Procedure
    
    def get_task8Frequency(self):
        return self.task8Frequency
    
    def get_task8Operating(self):
        return self.task8Operating
    
    def get_task1ChildPriority(self):
        return self.task1ChildPriority
    
    def get_task2ChildPriority(self):
        return self.task2ChildPriority
    
    def get_task3ChildPriority(self):
        return self.task3ChildPriority
    
    def get_task4ChildPriority(self):
        return self.task4ChildPriority
    
    def get_task5ChildPriority(self):
        return self.task5ChildPriority
    
    def get_task6ChildPriority(self):
        return self.task6ChildPriority
    
    def get_task7ChildPriority(self):
        return self.task7ChildPriority

    def get_task8ChildPriority(self):
        return self.task8ChildPriority
    
    def get_task1OutputCnt(self):
        return self.task1OutputCnt
    
    def get_task2OutputCnt(self):
        return self.task2OutputCnt
    
    def get_task3OutputCnt(self):
        return self.task3OutputCnt
    
    def get_task4OutputCnt(self):
        return self.task4OutputCnt
    
    def get_task5OutputCnt(self):
        return self.task5OutputCnt
    
    def get_task6OutputCnt(self):
        return self.task6OutputCnt
    
    def get_task7OutputCnt(self):
        return self.task7OutputCnt
    def get_task8OutputCnt(self):
        return self.task8OutputCnt
    
