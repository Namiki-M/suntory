from bs4 import BeautifulSoup

from tools import ManualParam as mp
from tools import AuditFileController as afc
import configparser
from _ast import Continue
import bs4
from bs4 import BeautifulSoup
from tools.ManualParam import ManualParam
from pickle import FALSE, NONE

#マニュアルファイルのパーサクラス。
class HtmlParser4Manual():
    
    manualPath:str = ""
    targetFile = ""
    secDiv5 = []
    secDiv4= ""
    whatHowToArchive = []
    stcWhatHowToAchieve = "What/How to achieve"
    stcProcedure:str = "Procedure"
    stcFrequencyOrTiming:str = "Frequency or timing"
    stcOperatingLimit:str = "Operating limit or standard condition"
    
    soup = ""
    manualFullPath = ""
    auditFileController = afc.AuditFileController()
    
    manualParam:'mp.ManualParam' = mp.ManualParam()
    
    fwSectionDiv3:str = "sectionDiv3_title"
    fwSectionDiv4:str = "sectionDiv4_title"
    fwSectionDiv5:str = "sectionDiv5_title"
    
    currentDataFile:str = ""
    
    # 対象のマニュアルと、当該マニュアルの出力対象sectionのID
    # Manual-2-0-1-0.html★NODEID-847260a77458b847a こんな形式で追加していく。
    targetManualFileAndId:'list[str]' = []
    
    subjectedDefectMode4xls:str = ""
    subjectedPackaging4xls:str = ""
    subjectedLine4xls:str = ""
    section3Xls:str = ""
    subsection4Xls:str = ""
    subsubsection4Xls:str = ""
    purpose4Xls:str = ""
    howToAchieve4Xlsx:'list[str]' = []
    howToAchievePriority4Xlsx:'list[str]' = []
    
    task1AllPriority4Xlsx:bool = False
    task1Procedure4Xlsx:'list[str]' = []
    task1Frequency4Xlsx:'list[str]' = []
    task1Operating4Xlsx:'list[str]' = []
    task2AllPriority4Xlsx:bool = False
    task2Procedure4Xlsx:'list[str]' = []
    task2Frequency4Xlsx:'list[str]' = []
    task2Operating4Xlsx:'list[str]' = []
    task3AllPriority4Xlsx:bool = False
    task3Procedure4Xlsx:'list[str]' = []
    task3Frequency4Xlsx:'list[str]' = []
    task3Operating4Xlsx:'list[str]' = []
    task4AllPriority4Xlsx:bool = False
    task4Procedure4Xlsx:'list[str]' = []
    task4Frequency4Xlsx:'list[str]' = []
    task4Operating4Xlsx:'list[str]' = []
    task5AllPriority4Xlsx:bool = False
    task5Procedure4Xlsx:'list[str]' = []
    task5Frequency4Xlsx:'list[str]' = []
    task5Operating4Xlsx:'list[str]' = []
    task6AllPriority4Xlsx:bool = False
    task6Procedure4Xlsx:'list[str]' = []
    task6Frequency4Xlsx:'list[str]' = []
    task6Operating4Xlsx:'list[str]' = []
    task7AllPriority4Xlsx:bool = False
    task7Procedure4Xlsx:'list[str]' = []
    task7Frequency4Xlsx:'list[str]' = []
    task7Operating4Xlsx:'list[str]' = []
    task8AllPriority4Xlsx:bool = False
    task8Procedure4Xlsx:'list[str]' = []
    task8Frequency4Xlsx:'list[str]' = []
    task8Operating4Xlsx:'list[str]' = []
    
    task1ChildPriority4Xlsx:'list[str]' = []
    task2ChildPriority4Xlsx:'list[str]' = []
    task3ChildPriority4Xlsx:'list[str]' = []
    task4ChildPriority4Xlsx:'list[str]' = []
    task5ChildPriority4Xlsx:'list[str]' = []
    task6ChildPriority4Xlsx:'list[str]' = []
    task7ChildPriority4Xlsx:'list[str]' = []
    task8ChildPriority4Xlsx:'list[str]' = []
    
    task1OutputCnt4Xlsx:int = 0
    task2OutputCnt4Xlsx:int = 0
    task3OutputCnt4Xlsx:int = 0
    task4OutputCnt4Xlsx:int = 0
    task5OutputCnt4Xlsx:int = 0
    task6OutputCnt4Xlsx:int = 0
    task7OutputCnt4Xlsx:int = 0
    task8OutputCnt4Xlsx:int = 0
    
    # コンストラクタ
    def __init__(self):
        print("init:HtmlParser4Manual")
        
        # マニュアルファイルの格納場所取得。
        # suntoryEnv = configparser.ConfigParser
        # suntoryEnv.read('suntoryEnv.ini', encoding='utf-8')
        # self.manualPath = suntoryEnv['MANUAL_FILE_PATH']['manualFilePath']
        soup = BeautifulSoup(self.manualFullPath, "html.parser")
    
    # マニュアルファイル解析。dataFile：対象ファイル(1件取得)、searchCondition：検索条件（配列で受け取る。）
    # 戻り値として、パラメータクラス(ManualParam)を返す。
    def parseManualData(self,dataFile,searchCondition,param,priorityVal):
        print("マニュアル解析処理　START")
        
        self.currentDataFile = dataFile
        
        manualParam:ManualParam = param
        
        paramPriority:str = priorityVal
        
        suntoryEnv = configparser.ConfigParser()
        suntoryEnv.read('suntoryEnv.ini', encoding='utf-8')
        manualPath = suntoryEnv['MANUAL_FILE_PATH']['manualFilePath']
        
        mp:str = manualPath + dataFile
        f = open(mp, 'r', encoding='UTF-8')
        # 対象マニュアルデータの読み込み。
        data:str = f.read()
        
        # 対象マニュアルの1つ上のレベルのマニュアルのdiv3(1.3.6　Contents transfer/Liquid treatment とか)を取得する
        self.section3Xls = self.findSectionDiv3();
        
        # 対象マニュアルのsectionDiv4(1.3.6.9　UV sterilizer for contents とか)を取得する
        self.subsection4Xls = self.findSectionDiv4();
        
        for sc in searchCondition :
            # 対象の検索文言が指定のマニュアルファイルに存在しない場合はループを抜ける
            if data.find(sc) is None :
                Continue
            else :
                targetPosition:int = data.find(sc)
                
                # 先頭から見つかったとこまでを切り取る
                posUntilFind = data[:targetPosition]
                # 見つかったテキスト内で、sectionDiv5を逆から検索する。（見つかったsectionを対象sectionとみなす）
                sectionDiv5Int:int = posUntilFind.rfind(self.fwSectionDiv5)
                
                data2:str = posUntilFind[sectionDiv5Int:]
                id4Section5:str = "id="
                id4Section5Index:int = data2.find(id4Section5)
                
                # "id="からの文字列を取得する。
                strFromSectionDiv5Id:str = data2[id4Section5Index:]
                
                targetSectionId:str = strFromSectionDiv5Id[4:28]
                print("targetSectionId -> " + targetSectionId)
                
                # 重複する出力を避けるため、メンバ変数(list)に格納している値を参照したうえ、
                #　書き込み対象かどうかの判定を行う。
                alreadyOutput:bool = False
                if len(self.targetManualFileAndId) > 0 :
                    for val in self.targetManualFileAndId :
                        if val == dataFile + "★" + targetSectionId :
                            print("すでに出力が完了しているSectionです")
                            alreadyOutput = True
                        else :
                            self.targetManualFileAndId.append(dataFile + "★" + targetSectionId)
                            print("これから出力するSectionです")
                            break
                else :
                    self.targetManualFileAndId.append(dataFile + "★" + targetSectionId)
                
                # すでに出力している(=クラス変数に存在する)場合、ループをスキップする。
                if alreadyOutput == True :
                    Continue
                
                soup:'bs4.BeautifulSoup' = bs4.BeautifulSoup(open(mp , encoding='UTF-8' ), 'html.parser')
                targetSectionElement:list[bs4.BeautifulSoup] = soup.select('#' + targetSectionId)
                subject:'list[str]' = []
                for var in targetSectionElement:
                    # ここでSection5(=出力対象Section)の中身を取得。
                    section5:str = var.find('span').string
                    self.subsubsection4Xls = section5
                    nextElem = var.find_next_sibling()
                    rows = nextElem.findAll("tr")
                    for row in rows:
                        cnt:int = 1
                        for td in row.find_all("td") :
                            if cnt == 2:
                                subject.append(td.string)
                            cnt = cnt + 1
                    print("ループ終わり")
                self.subjectedDefectMode4xls = subject[0]
                self.subjectedPackaging4xls = subject[1]
                self.subjectedLine4xls = subject[2]
        
                sibling_soup = soup.find(id=targetSectionId)
                cntSibl:int = 0
                divTag4PurposeContents:BeautifulSoup
                currentDiv:BeautifulSoup
                siblList:list[BeautifulSoup] = sibling_soup.find_next_siblings('div')
                
                for sl in siblList:
                    val:BeautifulSoup = sl
                    sl4Div:BeautifulSoup = val.find('div')
                    if sl4Div.find('strong') is not None :
                        bs4Strong:BeautifulSoup = sl4Div.find('strong')
                        purposeTitle:BeautifulSoup = bs4Strong.find('u')
                        if purposeTitle is not None:
                            print(purposeTitle.string)
                            if purposeTitle.string == "Purpose" :
                                # Purposeの文言をもつ、次のdivタグに実際のデータを持っているので、次カウンタを指定して取得する。
                                divTag4PurposeContents = siblList[cntSibl + 1]
                                # 子階層までたどるとコードが煩雑になるのでList形式で取得しているが、
                                # 実際のデータとしては1件しかもっていないので、0番目の要素を指定する。
                                purposeLst:list[BeautifulSoup] = divTag4PurposeContents.find_all('strong')
                                self.purpose4Xls = purposeLst[0].string
                                currentDiv = siblList[cntSibl + 2]
                                break
                            else :
                                cntSibl = cntSibl + 1
                                continue
                        else :
                            cntSibl = cntSibl + 1
                            continue
                    else :
                        cntSibl = cntSibl + 1
                        continue
                # purposeの次からのdivタグリストを取得する。
                siblList2:list[BeautifulSoup] = currentDiv.find_next_siblings('div')
                achieveContentTag:BeautifulSoup
                achieveCnt:int = 0
                how2AchieveLst:'list[str]' = []
                how2AchieveTmp:str = ""
                
                cntSibl = 0
                currentDiv = siblList2[cntSibl + 2]
                
                # HowToAchieveの各種値を抽出する。
                for how2Achieve in siblList2:
                    if how2Achieve.find('strong') is not None :
                        currentDiv = siblList2[achieveCnt + 3]
                        achieveContentTag = siblList2[achieveCnt + 1]
                        tableData:list[BeautifulSoup] = achieveContentTag.findAll("tr")
                        for row in tableData :
                            tdCount:list[BeautifulSoup] = row.find_all('td')
                            
                            if len(tdCount) == 2 :
                                if len(how2AchieveTmp) > 0 :
                                    how2AchieveLst.append(how2AchieveTmp)
                                how2AchieveTmp = ""
                                if paramPriority == 'ON' :
                                    if tdCount[1].find('img') is not None :
                                        ptag:BeautifulSoup = tdCount[0].find('p')
                                        how2AchieveTmp = ptag.string
                                        self.howToAchievePriority4Xlsx.append("ON")
                                    else :
                                        print("doNothing")
                                else :
                                    ptag:BeautifulSoup = tdCount[0].find('p')
                                    how2AchieveTmp = ptag.string
                                    if tdCount[1].find('img') is not None :
                                        self.howToAchievePriority4Xlsx.append("ON")
                                    else :
                                        self.howToAchievePriority4Xlsx.append("OFF")
                                    
                            elif len(tdCount) == 3 :
                                ptag:BeautifulSoup = tdCount[1].find('p')
                                if how2AchieveTmp != "" :
                                    how2AchieveTmp = how2AchieveTmp + "\n" + ptag.string
                                    
                        break
                if len(how2AchieveTmp) > 0 :
                    how2AchieveLst.append(how2AchieveTmp)
                    
                self.howToAchieve4Xlsx = how2AchieveLst
                
                siblList3:list[BeautifulSoup] = currentDiv.find_next_siblings('div')
                
                taskList:list[BeautifulSoup] = []
                for sl3 in siblList3 :
                    cn:'list[str]' = sl3['class']
                    if cn[0] == 'block_table' :
                        taskList.append(sl3)
                    else :
                        break
                currentTask:str = ""
                currentTaskDetail:str = ""
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
                
                task1AllPriority:bool = False
                task2AllPriority:bool = False
                task3AllPriority:bool = False
                task4AllPriority:bool = False
                task5AllPriority:bool = False
                task6AllPriority:bool = False
                task7AllPriority:bool = False
                task8AllPriority:bool = False
                
                task1OutputCnt:int = 0
                task2OutputCnt:int = 0
                task3OutputCnt:int = 0
                task4OutputCnt:int = 0
                task5OutputCnt:int = 0
                task6OutputCnt:int = 0
                task7OutputCnt:int = 0
                task8OutputCnt:int = 0
                
                
                # Tasksの各種値を抽出する。
                for tasks in taskList:
                    tableData:list[BeautifulSoup] = tasks.findAll("tr")
                    for row in tableData :
                        for td in row.find_all("td") :
                            if td.has_attr("colspan") :
                                currentTask = td.find('strong').get_text().strip()
                                colspanProp:str = td.get('colspan')
                                # colspan=2 の場合、Task全体をpriorityありと見なす。
                                if colspanProp == "2" :
                                    if currentTask == "Task 1" :
                                        task1AllPriority = True
                                    elif currentTask == "Task 2" :
                                        task2AllPriority = True
                                    elif currentTask == "Task 3" :
                                        task3AllPriority = True
                                    elif currentTask == "Task 4" :
                                        task4AllPriority = True
                                    elif currentTask == "Task 5" :
                                        task5AllPriority = True
                                    elif currentTask == "Task 6" :
                                        task6AllPriority = True
                                    elif currentTask == "Task 7" :
                                        task7AllPriority = True
                                    elif currentTask == "Task 8" :
                                        task8AllPriority = True
                                # colspan=3 の場合、Task全体をpriorityなしと見なす。
                                elif colspanProp == "3" :
                                    if currentTask == "Task 1" :
                                        task1AllPriority = False
                                    elif currentTask == "Task 2" :
                                        task2AllPriority = False
                                    elif currentTask == "Task 3" :
                                        task3AllPriority = False
                                    elif currentTask == "Task 4" :
                                        task4AllPriority = False
                                    elif currentTask == "Task 5" :
                                        task5AllPriority = False
                                    elif currentTask == "Task 6" :
                                        task6AllPriority = False
                                    elif currentTask == "Task 7" :
                                        task7AllPriority = False
                                    elif currentTask == "Task 8" :
                                        task8AllPriority = False
                            elif td.find("strong") is not None :
                                currentTaskDetail = td.string
                            else :
                                taskChildPriority:list[BeautifulSoup] = row.find_all('td')
                                if currentTask == "Task 1" :
                                    task1Str:str = td.string.strip()
                                    if currentTaskDetail == self.stcProcedure :
                                        if task1Str is not None and len(task1Str) > 1 :
                                            if paramPriority == "OFF" :
                                                task1Procedure.append(task1Str)
                                                task1OutputCnt = task1OutputCnt + 1
                                            elif paramPriority == "ON" and task1AllPriority == True :
                                                task1Procedure.append(task1Str)
                                                task1OutputCnt = task1OutputCnt + 1
                                            elif paramPriority == "ON" and task1AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task1Procedure.append(task1Str)
                                                    task1OutputCnt = task1OutputCnt + 1
                                        else :
                                            task1childImgTag:BeautifulSoup = td.find('img')
                                            if task1childImgTag is not None :
                                                if task1AllPriority == False :
                                                    task1ChildPriority.append("ON")
                                            else :
                                                if task1AllPriority == False :
                                                    task1ChildPriority.append("OFF")
                                        
                                    elif currentTaskDetail == self.stcFrequencyOrTiming :
                                        if task1Str != "" :
                                            if paramPriority == "OFF" :
                                                task1Frequency.append(task1Str)
                                                task1OutputCnt = task1OutputCnt + 1
                                            elif paramPriority == "ON" and task1AllPriority == True :
                                                task1Frequency.append(task1Str)
                                                task1OutputCnt = task1OutputCnt + 1
                                            elif paramPriority == "ON" and task1AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task1Frequency.append(task1Str)
                                                    task1OutputCnt = task1OutputCnt + 1
                                        else :
                                            if td.has_attr('img') :
                                                if task1AllPriority == False :
                                                    task1ChildPriority.append("ON")
                                            else :
                                                if task1AllPriority == False :
                                                    task1ChildPriority.append("OFF")
                                                    
                                    elif currentTaskDetail == self.stcOperatingLimit :
                                        if task1Str != "" :
                                            if paramPriority == "OFF" :
                                                task1Operating.append(task1Str)
                                                task1OutputCnt = task1OutputCnt + 1
                                            elif paramPriority == "ON" and task1AllPriority == True :
                                                task1Operating.append(task1Str)
                                                task1OutputCnt = task1OutputCnt + 1
                                            elif paramPriority == "ON" and task1AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task1Operating.append(task1Str)
                                                    task1OutputCnt = task1OutputCnt + 1
                                        else :
                                            if td.has_attr('img') :
                                                if task1AllPriority == False :
                                                    task1ChildPriority.append("ON")
                                            else :
                                                if task1AllPriority == False :
                                                    task1ChildPriority.append("OFF")
                                elif currentTask == "Task 2" :
                                    task2Str:str = td.string
                                    if currentTaskDetail == self.stcProcedure :
                                        if task2Str is not None and len(task2Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task2Procedure.append(task2Str)
                                                task2OutputCnt = task2OutputCnt + 1
                                            elif paramPriority == "ON" and task2AllPriority == True :
                                                task2Procedure.append(task2Str)
                                                task2OutputCnt = task2OutputCnt + 1
                                            elif paramPriority == "ON" and task2AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task2Procedure.append(task2Str)
                                                    task2OutputCnt = task2OutputCnt + 1
                                        else :
                                            task2childImgTag:BeautifulSoup = td.find('img')
                                            if task2childImgTag is not None :
                                                if task2AllPriority == False :
                                                    task2ChildPriority.append("ON")
                                            else :
                                                if task1AllPriority == False :
                                                    task2ChildPriority.append("OFF")
                                            
                                    elif currentTaskDetail == self.stcFrequencyOrTiming :
                                        if task2Str is not None and len(task2Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task2Frequency.append(task2Str)
                                                task2OutputCnt = task2OutputCnt + 1
                                            elif paramPriority == "ON" and task2AllPriority == True :
                                                task2Frequency.append(task2Str)
                                                task2OutputCnt = task2OutputCnt + 1
                                            elif paramPriority == "ON" and task2AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task2Frequency.append(task2Str)
                                                    task2OutputCnt = task2OutputCnt + 1
                                        else :
                                            if td.has_attr('img') :
                                                if task2AllPriority == False :
                                                    task2ChildPriority.append("ON")
                                            else :
                                                if task2AllPriority == False :
                                                    task2ChildPriority.append("OFF")
                                            
                                    elif currentTaskDetail == self.stcOperatingLimit :
                                        
                                        if task2Str is not None and len(task2Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task2Operating.append(task2Str)
                                                task2OutputCnt = task2OutputCnt + 1
                                            elif paramPriority == "ON" and task2AllPriority == True :
                                                task2Operating.append(task2Str)
                                                task2OutputCnt = task2OutputCnt + 1
                                            elif paramPriority == "ON" and task2AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task2Operating.append(task2Str)
                                                    task2OutputCnt = task2OutputCnt + 1
                                        else :
                                            if td.has_attr('img') :
                                                if task2AllPriority == False :
                                                    task2ChildPriority.append("ON")
                                            else :
                                                if task2AllPriority == False :
                                                    task2ChildPriority.append("OFF")
                                                
                                elif currentTask == "Task 3" :
                                    task3Str:str = td.string
                                    if currentTaskDetail == self.stcProcedure :
                                        if task3Str is not None and len(task3Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task3Procedure.append(task3Str)
                                                task3OutputCnt = task3OutputCnt + 1
                                            elif paramPriority == "ON" and task3AllPriority == True :
                                                task3Procedure.append(task3Str)
                                                task3OutputCnt = task3OutputCnt + 1
                                            elif paramPriority == "ON" and task3AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task3Procedure.append(task3Str)
                                                    task3OutputCnt = task3OutputCnt + 1
                                        else :
                                            task3childImgTag:BeautifulSoup = td.find('img')
                                            if task3childImgTag is not None :
                                                if task3AllPriority == False :
                                                    task3ChildPriority.append("ON")
                                            else :
                                                if task3AllPriority == False :
                                                    task3ChildPriority.append("OFF")
                                            
                                    elif currentTaskDetail == self.stcFrequencyOrTiming :
                                        if task3Str is not None and len(task3Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task3Frequency.append(task3Str)
                                                task3OutputCnt = task3OutputCnt + 1
                                            elif paramPriority == "ON" and task3AllPriority == True :
                                                task3Frequency.append(task3Str)
                                                task3OutputCnt = task3OutputCnt + 1
                                            elif paramPriority == "ON" and task3AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task3Frequency.append(task3Str)
                                                    task3OutputCnt = task3OutputCnt + 1
                                        else :
                                            if td.has_attr('img') :
                                                if task3AllPriority == False :
                                                    task3ChildPriority.append("ON")
                                            else :
                                                if task3AllPriority == False :
                                                    task3ChildPriority.append("OFF")
                                    elif currentTaskDetail == self.stcOperatingLimit :
                                        if task3Str is not None and len(task3Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task3Operating.append(task3Str)
                                                task3OutputCnt = task3OutputCnt + 1
                                            elif paramPriority == "ON" and task3AllPriority == True :
                                                task3Operating.append(task3Str)
                                                task3OutputCnt = task3OutputCnt + 1
                                            elif paramPriority == "ON" and task3AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task3Operating.append(task3Str)
                                                    task3OutputCnt = task3OutputCnt + 1
                                            
                                        else :
                                            if td.has_attr('img') :
                                                if task3AllPriority == False :
                                                    task3ChildPriority.append("ON")
                                            else :
                                                if task3AllPriority == False :
                                                    task3ChildPriority.append("OFF")
                                                
                                elif currentTask == "Task 4" :
                                    task4Str:str = td.string
                                    if currentTaskDetail == self.stcProcedure :
                                        if task4Str is not None and len(task4Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task4Procedure.append(task4Str)
                                                task4OutputCnt = task4OutputCnt + 1
                                            elif paramPriority == "ON" and task4AllPriority == True :
                                                task4Procedure.append(task4Str)
                                                task4OutputCnt = task4OutputCnt + 1
                                            elif paramPriority == "ON" and task4AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task4Procedure.append(task4Str)
                                                    task4OutputCnt = task4OutputCnt + 1
                                        else :
                                            task4childImgTag:BeautifulSoup = td.find('img')
                                            if task4childImgTag is not None :
                                                if task4AllPriority == False :
                                                    task4ChildPriority.append("ON")
                                            else :
                                                if task4AllPriority == False :
                                                    task4ChildPriority.append("OFF")
                                    elif currentTaskDetail == self.stcFrequencyOrTiming :
                                        if task4Str is not None and len(task4Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task4Frequency.append(task4Str)
                                                task4OutputCnt = task4OutputCnt + 1
                                            elif paramPriority == "ON" and task4AllPriority == True :
                                                task4Frequency.append(task4Str)
                                                task4OutputCnt = task4OutputCnt + 1
                                            elif paramPriority == "ON" and task4AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task4Frequency.append(task4Str)
                                                    task4OutputCnt = task4OutputCnt + 1
                                        else :
                                            if td.has_attr('img') :
                                                if task4AllPriority == False :
                                                    task4ChildPriority.append("ON")
                                            else :
                                                if task4AllPriority == False :
                                                    task4ChildPriority.append("OFF") 
                                    elif currentTaskDetail == self.stcOperatingLimit :
                                        if task4Str is not None and len(task4Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task4Operating.append(task4Str)
                                                task4OutputCnt = task4OutputCnt + 1
                                            elif paramPriority == "ON" and task4AllPriority == True :
                                                task4Operating.append(task4Str)
                                                task4OutputCnt = task4OutputCnt + 1
                                            elif paramPriority == "ON" and task4AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task4Operating.append(task4Str)
                                                    task4OutputCnt = task4OutputCnt + 1
                                        else :
                                            if td.has_attr('img') :
                                                if task4AllPriority == False :
                                                    task4ChildPriority.append("ON")
                                            else :
                                                if task4AllPriority == False :
                                                    task4ChildPriority.append("OFF")
                                elif currentTask == "Task 5" :
                                    task5Str:str = td.string
                                    if currentTaskDetail == self.stcProcedure :
                                        if task5Str is not None and len(task5Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task5Procedure.append(task5Str)
                                                task5OutputCnt = task5OutputCnt + 1
                                            elif paramPriority == "ON" and task5AllPriority == True :
                                                task5Procedure.append(task5Str)
                                                task5OutputCnt = task5OutputCnt + 1
                                            elif paramPriority == "ON" and task5AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task5Procedure.append(task5Str)
                                                    task5OutputCnt = task5OutputCnt + 1
                                        else :
                                            task5childImgTag:BeautifulSoup = td.find('img')
                                            if task5childImgTag is not None :
                                                if task5AllPriority == False :
                                                    task5ChildPriority.append("ON")
                                            else :
                                                if task5AllPriority == False :
                                                    task5ChildPriority.append("OFF")
                                    elif currentTaskDetail == self.stcFrequencyOrTiming :
                                        if task5Str is not None and len(task5Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task5Frequency.append(task5Str)
                                                task5OutputCnt = task5OutputCnt + 1
                                            elif paramPriority == "ON" and task5AllPriority == True :
                                                task5Frequency.append(task5Str)
                                                task5OutputCnt = task5OutputCnt + 1
                                            elif paramPriority == "ON" and task5AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task5Frequency.append(task5Str)
                                                    task5OutputCnt = task5OutputCnt + 1
                                        else :
                                            if td.has_attr('img') :
                                                if task5AllPriority == False :
                                                    task5ChildPriority.append("ON")
                                            else :
                                                if task5AllPriority == False :
                                                    task5ChildPriority.append("OFF")
                                            
                                    elif currentTaskDetail == self.stcOperatingLimit :
                                        if task5Str is not None and len(task5Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task5Operating.append(task5Str)
                                                task5OutputCnt = task5OutputCnt + 1
                                            elif paramPriority == "ON" and task5AllPriority == True :
                                                task5Operating.append(task5Str)
                                                task5OutputCnt = task5OutputCnt + 1
                                            elif paramPriority == "ON" and task5AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task5Operating.append(task5Str)
                                                    task5OutputCnt = task5OutputCnt + 1
                                            
                                        else :
                                            if td.has_attr('img') :
                                                if task5AllPriority == False :
                                                    task5ChildPriority.append("ON")
                                            else :
                                                if task5AllPriority == False :
                                                    task5ChildPriority.append("OFF")
                                                
                                elif currentTask == "Task 6" :
                                    task6Str:str = td.string
                                    if currentTaskDetail == self.stcProcedure :
                                        if task6Str is not None and len(task6Str) > 1 :
                                            if paramPriority == "OFF" :
                                                task6Procedure.append(task6Str)
                                                task6OutputCnt = task6OutputCnt + 1
                                            elif paramPriority == "ON" and task6AllPriority == True :
                                                task6Procedure.append(task6Str)
                                                task6OutputCnt = task6OutputCnt + 1
                                            elif paramPriority == "ON" and task6AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task6Procedure.append(task6Str)
                                                    task6OutputCnt = task6OutputCnt + 1
                                        else :
                                            task6childImgTag:BeautifulSoup = td.find('img')
                                            if task6childImgTag is not None :
                                                if task6AllPriority == False :
                                                    task6ChildPriority.append("ON")
                                            else :
                                                if task6AllPriority == False :
                                                    task6ChildPriority.append("OFF")   
                                    elif currentTaskDetail == self.stcFrequencyOrTiming :
                                        if task6Str is not None and len(task6Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task6Frequency.append(task6Str)
                                                task6OutputCnt = task6OutputCnt + 1
                                            elif paramPriority == "ON" and task6AllPriority == True :
                                                task6Frequency.append(task6Str)
                                                task6OutputCnt = task6OutputCnt + 1
                                            elif paramPriority == "ON" and task6AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task6Frequency.append(task6Str)
                                                    task6OutputCnt = task6OutputCnt + 1
                                        else :
                                            if td.has_attr('img') :
                                                if task6AllPriority == False :
                                                    task6ChildPriority.append("ON")
                                            else :
                                                if task6AllPriority == False :
                                                    task6ChildPriority.append("OFF")
                                            
                                    elif currentTaskDetail == self.stcOperatingLimit :
                                        if task6Str is not None and len(task6Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task6Operating.append(task6Str)
                                                task6OutputCnt = task6OutputCnt + 1
                                            elif paramPriority == "ON" and task6AllPriority == True :
                                                task6Operating.append(task6Str)
                                                task6OutputCnt = task6OutputCnt + 1
                                            elif paramPriority == "ON" and task6AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task6Operating.append(task6Str)
                                                    task6OutputCnt = task6OutputCnt + 1
                                        else :
                                            if td.has_attr('img') :
                                                if task6AllPriority == False :
                                                    task6ChildPriority.append("ON")
                                            else :
                                                if task6AllPriority == False :
                                                    task6ChildPriority.append("OFF")
                                                
                                elif currentTask == "Task 7" :
                                    task7Str:str = td.string
                                    if currentTaskDetail == self.stcProcedure :
                                        if task7Str is not None and len(task7Str) > 1 :
                                            if paramPriority == "OFF" :
                                                task7Procedure.append(task7Str)
                                                task7OutputCnt = task7OutputCnt + 1
                                            elif paramPriority == "ON" and task7AllPriority == True :
                                                task7Procedure.append(task7Str)
                                                task7OutputCnt = task7OutputCnt + 1
                                            elif paramPriority == "ON" and task7AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task7Procedure.append(task7Str)
                                                    task7OutputCnt = task7OutputCnt + 1
                                        else :
                                            task7childImgTag:BeautifulSoup = td.find('img')
                                            if task7childImgTag is not None :
                                                if task7AllPriority == False :
                                                    task7ChildPriority.append("ON")
                                            else :
                                                if task7AllPriority == False :
                                                    task7ChildPriority.append("OFF") 
                                    elif currentTaskDetail == self.stcFrequencyOrTiming :
                                        if task7Str is not None and len(task7Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task7Frequency.append(task7Str)
                                                task7OutputCnt = task7OutputCnt + 1
                                            elif paramPriority == "ON" and task7AllPriority == True :
                                                task7Frequency.append(task7Str)
                                                task7OutputCnt = task7OutputCnt + 1
                                            elif paramPriority == "ON" and task7AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task7Frequency.append(task7Str)
                                                    task7OutputCnt = task7OutputCnt + 1
                                        else :
                                            if td.has_attr('img') :
                                                if task7AllPriority == False :
                                                    task7ChildPriority.append("ON")
                                            else :
                                                if task7AllPriority == False :
                                                    task7ChildPriority.append("OFF")
                                            
                                    elif currentTaskDetail == self.stcOperatingLimit :
                                        if task7Str is not None and len(task7Str.split()) > 1 :
                                            if paramPriority == "OFF" :
                                                task7Operating.append(task7Str)
                                                task7OutputCnt = task7OutputCnt + 1
                                            elif paramPriority == "ON" and task7AllPriority == True :
                                                task7Operating.append(task7Str)
                                                task7OutputCnt = task7OutputCnt + 1
                                            elif paramPriority == "ON" and task7AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task7Operating.append(task7Str)
                                                    task7OutputCnt = task7OutputCnt + 1
                                        else :
                                            if td.has_attr('img') :
                                                if task7AllPriority == False :
                                                    task7ChildPriority.append("ON")
                                            else :
                                                if task7AllPriority == False :
                                                    task7ChildPriority.append("OFF")
                                elif currentTask == "Task 8" :
                                    task8Str:str = td.string
                                    if currentTaskDetail == self.stcProcedure :
                                        if task8Str is not None and len(task8Str) > 1 :
                                            if paramPriority == "OFF" :
                                                task8Procedure.append(task8Str)
                                                task8OutputCnt = task8OutputCnt + 1
                                            elif paramPriority == "ON" and task8AllPriority == True :
                                                task8Procedure.append(task8Str)
                                                task8OutputCnt = task8OutputCnt + 1
                                            elif paramPriority == "ON" and task8AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task8Procedure.append(task2Str)
                                                    task8OutputCnt = task8OutputCnt + 1
                                            
                                        else :
                                            task8childImgTag:BeautifulSoup = td.find('img')
                                            if task8childImgTag is not None :
                                                if task8AllPriority == False :
                                                    task8ChildPriority.append("ON")
                                            else :
                                                if task8AllPriority == False :
                                                    task8ChildPriority.append("OFF")
                                            
                                    elif currentTaskDetail == self.stcFrequencyOrTiming :
                                        if task8Str is not None and len(task8Str.split()) > 1 :
                                            task8Frequency.append(task8Str)
                                            if paramPriority == "OFF" :
                                                task8Frequency.append(task8Str)
                                                task8OutputCnt = task8OutputCnt + 1
                                            elif paramPriority == "ON" and task8AllPriority == True :
                                                task8Frequency.append(task8Str)
                                                task8OutputCnt = task8OutputCnt + 1
                                            elif paramPriority == "ON" and task8AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task8Frequency.append(task8Str)
                                                    task8OutputCnt = task8OutputCnt + 1
                                            
                                        else :
                                            if td.has_attr('img') :
                                                if task8AllPriority == False :
                                                    task8ChildPriority.append("ON")
                                            else :
                                                if task8AllPriority == False :
                                                    task8ChildPriority.append("OFF")
                                            
                                    elif currentTaskDetail == self.stcOperatingLimit :
                                        if task8Str is not None and len(task8Str.split()) > 1 :
                                            task8Operating.append(task8Str)
                                            
                                            if paramPriority == "OFF" :
                                                task8Operating.append(task8Str)
                                                task8OutputCnt = task8OutputCnt + 1
                                            elif paramPriority == "ON" and task8AllPriority == True :
                                                task8Operating.append(task8Str)
                                                task8OutputCnt = task8OutputCnt + 1
                                            elif paramPriority == "ON" and task8AllPriority == False :
                                                tmpTd:BeautifulSoup = taskChildPriority[2]
                                                if tmpTd.find('img') is not None :
                                                    task8Operating.append(task8Str)
                                                    task8OutputCnt = task8OutputCnt + 1
                                        else :
                                            if td.has_attr('img') :
                                                if task8AllPriority == False :
                                                    task8ChildPriority.append("ON")
                                            else :
                                                if task8AllPriority == False :
                                                    task8ChildPriority.append("OFF")
                
                self.task1AllPriority4Xlsx = task1AllPriority
                self.task2AllPriority4Xlsx = task2AllPriority
                self.task3AllPriority4Xlsx = task3AllPriority
                self.task4AllPriority4Xlsx = task4AllPriority
                self.task5AllPriority4Xlsx = task5AllPriority
                self.task6AllPriority4Xlsx = task6AllPriority
                self.task7AllPriority4Xlsx = task7AllPriority
                self.task8AllPriority4Xlsx = task8AllPriority
                
                self.task1ChildPriority4Xlsx = task1ChildPriority
                
                self.task1Procedure4Xlsx = task1Procedure
                self.task1Frequency4Xlsx = task1Frequency
                self.task1Operating4Xlsx = task1Operating
                self.task2Procedure4Xlsx = task2Procedure
                self.task2Frequency4Xlsx = task2Frequency
                self.task2Operating4Xlsx = task2Operating
                self.task3Procedure4Xlsx = task3Procedure
                self.task3Frequency4Xlsx = task3Frequency
                self.task3Operating4Xlsx = task3Operating
                self.task4Procedure4Xlsx = task4Procedure
                self.task4Frequency4Xlsx = task4Frequency
                self.task4Operating4Xlsx = task4Operating
                self.task5Procedure4Xlsx = task5Procedure
                self.task5Frequency4Xlsx = task5Frequency
                self.task5Operating4Xlsx = task5Operating
                self.task6Procedure4Xlsx = task6Procedure
                self.task6Frequency4Xlsx = task6Frequency
                self.task6Operating4Xlsx = task6Operating
                self.task7Procedure4Xlsx = task7Procedure
                self.task7Frequency4Xlsx = task7Frequency
                self.task7Operating4Xlsx = task7Operating
                self.task8Procedure4Xlsx = task8Procedure
                self.task8Frequency4Xlsx = task8Frequency
                self.task8Operating4Xlsx = task8Operating
                
                self.task1OutputCnt4Xlsx = task1OutputCnt
                self.task2OutputCnt4Xlsx = task2OutputCnt
                self.task3OutputCnt4Xlsx = task3OutputCnt
                self.task4OutputCnt4Xlsx = task4OutputCnt
                self.task5OutputCnt4Xlsx = task5OutputCnt
                self.task6OutputCnt4Xlsx = task6OutputCnt
                self.task7OutputCnt4Xlsx = task7OutputCnt
                self.task8OutputCnt4Xlsx = task8OutputCnt
                
                # パラメータクラスへのセット
                manualParam.set_section(self.section3Xls)
                manualParam.set_subSection(self.subsection4Xls)
                manualParam.set_subsubSection(self.subsubsection4Xls)
                manualParam.set_purpose(self.purpose4Xls)
                manualParam.set_subjectedDefectMode(self.subjectedDefectMode4xls)
                manualParam.set_subjectedPackaging(self.subjectedPackaging4xls)
                manualParam.set_subjectedLine(self.subjectedLine4xls)
                manualParam.set_task1AllPriority(self.task1AllPriority4Xlsx)
                manualParam.set_task2AllPriority(self.task2AllPriority4Xlsx)
                manualParam.set_task3AllPriority(self.task3AllPriority4Xlsx)
                manualParam.set_task4AllPriority(self.task4AllPriority4Xlsx)
                manualParam.set_task5AllPriority(self.task5AllPriority4Xlsx)
                manualParam.set_task6AllPriority(self.task6AllPriority4Xlsx)
                manualParam.set_task7AllPriority(self.task7AllPriority4Xlsx)
                manualParam.set_task8AllPriority(self.task8AllPriority4Xlsx)
                
                manualParam.set_task1ChildPriority(self.task1ChildPriority4Xlsx)
                
                # 複数件情報
                manualParam.set_howToAchieve(self.howToAchieve4Xlsx)
                manualParam.set_howToAchievePriority(self.howToAchievePriority4Xlsx)
                manualParam.set_task1Procedure(self.task1Procedure4Xlsx)
                manualParam.set_task1Frequency(self.task1Frequency4Xlsx)
                manualParam.set_task1Operating(self.task1Operating4Xlsx)
                manualParam.set_task2Procedure(self.task2Procedure4Xlsx)
                manualParam.set_task2Frequency(self.task2Frequency4Xlsx)
                manualParam.set_task2Operating(self.task2Operating4Xlsx)
                manualParam.set_task3Procedure(self.task3Procedure4Xlsx)
                manualParam.set_task3Frequency(self.task3Frequency4Xlsx)
                manualParam.set_task3Operating(self.task3Operating4Xlsx)
                manualParam.set_task4Procedure(self.task4Procedure4Xlsx)
                manualParam.set_task4Frequency(self.task4Frequency4Xlsx)
                manualParam.set_task4Operating(self.task4Operating4Xlsx)
                manualParam.set_task5Procedure(self.task5Procedure4Xlsx)
                manualParam.set_task5Frequency(self.task5Frequency4Xlsx)
                manualParam.set_task5Operating(self.task5Operating4Xlsx)
                manualParam.set_task6Procedure(self.task6Procedure4Xlsx)
                manualParam.set_task6Frequency(self.task6Frequency4Xlsx)
                manualParam.set_task6Operating(self.task6Operating4Xlsx)
                manualParam.set_task7Procedure(self.task7Procedure4Xlsx)
                manualParam.set_task7Frequency(self.task7Frequency4Xlsx)
                manualParam.set_task7Operating(self.task7Operating4Xlsx)
                manualParam.set_task8Procedure(self.task8Procedure4Xlsx)
                manualParam.set_task8Frequency(self.task8Frequency4Xlsx)
                manualParam.set_task8Operating(self.task8Operating4Xlsx)

                manualParam.set_task1OutputCnt(self.task1OutputCnt4Xlsx)
                manualParam.set_task2OutputCnt(self.task2OutputCnt4Xlsx)
                manualParam.set_task3OutputCnt(self.task3OutputCnt4Xlsx)
                manualParam.set_task4OutputCnt(self.task4OutputCnt4Xlsx)
                manualParam.set_task5OutputCnt(self.task5OutputCnt4Xlsx)
                manualParam.set_task6OutputCnt(self.task6OutputCnt4Xlsx)
                manualParam.set_task7OutputCnt(self.task7OutputCnt4Xlsx)
                manualParam.set_task8OutputCnt(self.task8OutputCnt4Xlsx)
                     
        return manualParam                               
    
    # Sectionデータの探索。
    # 末端のマニュアルファイルには存在しないデータなので、カレントのファイル名をsubstringして取得する。
    def findSectionDiv3(self):
        print("findSectionDiv3 START")
        suntoryEnv = configparser.ConfigParser()
        suntoryEnv.read('suntoryEnv.ini', encoding='utf-8')
        manualPath = suntoryEnv['MANUAL_FILE_PATH']['manualFilePath']
        
        tmp:str = self.currentDataFile
        tmp = tmp.replace("Manual-", "", 1)
        print("1回削った" + tmp)
        tmpList:'list[str]' = tmp.split('-')
        tmpCnt:int = 0
        parentManual:str = "Manual"
        while tmpCnt <= 2 :
            parentManual = parentManual + "-" + str(tmpList[tmpCnt])
            tmpCnt = tmpCnt + 1
        parentManual = parentManual + ".html"
        
        mp:str = manualPath + parentManual
        soup:'bs4.BeautifulSoup' = bs4.BeautifulSoup(open(mp , encoding='UTF-8' ), 'html.parser')
        div3Lst:list[BeautifulSoup] = soup.find_all(class_=self.fwSectionDiv3)
        secDiv3Title:str = ""
        for var in div3Lst :
            secDiv3Title = var.find_all("span")
            secDiv3Title = secDiv3Title[0].string
            break
        return secDiv3Title
        
        # 見つける処理。
        
        #self.manualParam.section = 見つけたデータをセット
        
    # class「sectionDiv4_title」を取得する。1件ヒットする想定。(マニュアルファイルの項番がヒットする。)
    # 最終的に監査資料ファイルのSubsection(F列)にセット。    
    def findSectionDiv4(self):
        print("findSectionDiv4 START")
        
        suntoryEnv = configparser.ConfigParser()
        suntoryEnv.read('suntoryEnv.ini', encoding='utf-8')
        manualPath = suntoryEnv['MANUAL_FILE_PATH']['manualFilePath']
        
        mp:str = manualPath + self.currentDataFile
        soup:'bs4.BeautifulSoup' = bs4.BeautifulSoup(open(mp , encoding='UTF-8' ), 'html.parser')
        div4Lst:list[BeautifulSoup] = soup.find_all(class_=self.fwSectionDiv4)
        secDiv4Title:str = ""
        for var in div4Lst :
            secDiv4Title = var.find_all("span")
            secDiv4Title = secDiv4Title[0].string
            break
        return secDiv4Title
        
    def findTargetSection(self):
        print("findTargetSection START")
        # 検索対象ファイルに対して、検索文言を先頭から検索する。（パースではなくテキストで検索する）
        
        
        # ヒットした文字位置までをメモリにtmp変数に格納。
        
        
        # tmp変数から、「sectionDiv5_title」を逆順に検索。rfindを使用する。
        
        
        # 最初に見つかったsectionDiv5_titleが対象なので、これのidを取得する。
        # 見つかったsectionDiv5_titleの位置から、次にid="が出てくる箇所を探し、
        # id="に続く24文字を取得する。

        
        # ↑で見つかったidをメンバ変数にセット。
        
        # 対象ファイルをHTMLとしてパース。
        #　見つかったIDを検索し、これをtargetSectionとする。
    