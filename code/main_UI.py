import os
import KMP
import File
import file_UI
from PyQt5 import QtWidgets, QtGui
from Original_Model import main_GUI
from create_file_UI import *
from item_UI import *
from freq_UI import *
from about_UI import *
from progressbar_UI import *


class UI(QtWidgets.QMainWindow, main_GUI.Ui_MainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.init()
        self.search_status = None
        self.freqs = None
        self.words = []
        self.logic_status = []
        self.original = []

    def init(self):
        self.statusBar().showMessage("欢迎~~~")
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.logic_search)
        self.pushButton_3.clicked.connect(self.create_file)
        self.pushButton_4.clicked.connect(self.cal_words_freq)
        self.pushButton_5.clicked.connect(self.packaging)
        self.action.triggered.connect(self.add_files)
        self.action_2.triggered.connect(self.about)
        self.action_3.triggered.connect(self.clear_list)
        self.tableWidget.cellDoubleClicked.connect(self.itemClicked)

    def add_files(self):
        self.freqs = None
        ui_file = file_UI.Ui_FileDialog()
        files = ui_file.openFileNamesDialog()
        if files:
            self.creat_tableWidget(files)

    def about(self):
        about_ui = about_UI()
        about_ui.show()
        about_ui.exec_()

    def create_file(self):
        self.freqs = None
        dialog = create_file_UI()
        file_pos = ""
        if dialog.exec_():
            file_pos = (QtGui.QStandardItem(dialog.file_pos())).text()
            # dialog.destroy()
        if file_pos and "\\" not in file_pos:
            import os
            if os.path.isabs(file_pos):
                pass
            else:
                file_pos = os.getcwd() + "\\" + file_pos + ".txt"
            file = open(file_pos, "w")
            file.close()
            self.creat_tableWidget([file_pos])

    def cal_words_freq(self):
        import Cal_Words_Freq
        files=[]
        self.freqs = []
        files = self.get_files_from_table()
        proBar_ui = progressbar_UI()
        proBar_ui.show()
        for file in files:
            self.freqs.append((file, File.cal_words_positions(files=[file])))
            proBar_ui.setText(file)
            proBar_ui.setValue((files.index(file) + 1) * 100 / len(files))
            QtWidgets.QApplication.processEvents()
        proBar_ui.close()
        tmp1=Cal_Words_Freq.Cal_Words_Freq(files)
        tmp=tmp1.getInv()
        ans=[]
        for key in tmp.keys():
            ans.append({"word": key, "num": tmp[key]})
        def num(temp):
            return temp["num"]
        ans.sort(key=num,reverse=True)
        freq_ui = freq_UI(ans)
        freq_ui.show()
        freq_ui.exec_()

    def logic_search(self):
        self.logic_status.clear()
        self.words.clear()
        files = self.get_files_from_table()
        self.search_status = self.get_research_content()
        self.statusBar().showMessage(self.get_research_content() + " 的检索结果")
        data=str(self.search_status)
        data=data.replace("!","~")
        buf=""
        flag=0
        for j in range(len(data)):
            if data[j] not in '()&|~':
                buf+=data[j].lower()
            elif data[j]==")":
                self.words.append(buf)
                buf=""
        for file in files:
            temp = {'file': file, 'result': ""}
            tmp=data
            with open(file) as f:
                content = f.read()
                for word in self.words:
                    if len(KMP.positions(content.lower(),word))>0:
                        tmp=tmp.replace(word,"1")
                    else:
                        tmp=tmp.replace(word,"0")
                tmp=tmp.replace("~1","0")
                tmp=tmp.replace("~0","1")
                sum=eval(tmp)
                if sum==0:
                    temp['result']="False"
                else:
                    temp['result']="True"
                self.logic_status.append(temp)
        self.tableWidget.clear()
        files = []
        ans = []
        for i in self.logic_status:
            files.append(i['file'])
            ans.append(i['result'])
        self.creat_tableWidget1(files, ans)
        self.words.clear()
        self.original.clear()
        for j in range(len(data)):
            if data[j]=="~":
                flag=1
            if data[j] not in '()&|~':
                buf+=data[j].lower()
            elif data[j]==")":
                if flag==0:
                    self.words.append(buf)
                buf=""
                flag=0
        for word in self.words:
            self.original.append(word)

    def packaging(self):
        import Inverted_Index
        dialog = create_file_UI()
        file_pos = ""
        if dialog.exec_():
            file_pos = (QtGui.QStandardItem(dialog.file_pos())).text()
            # dialog.destroy()
        if file_pos and "\\" not in file_pos:
            import os
            if os.path.isabs(file_pos):
                pass
            else:
                file_pos = os.getcwd() + "\\" + file_pos + ".txt"
            file = open(file_pos, "w")
            files = self.get_files_from_table()
            tmp=Inverted_Index.Inverted_Index(files)
            ans=str(tmp.getInv())
            for key in ans.split('),',ans.count('),')):
                file.write(key)
                file.write(')\n')
            file.close()
            self.creat_tableWidget([file_pos])

    def clear_list(self):
        self.freqs = None
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['文件', "词频"])
        self.tableWidget.setRowCount(0)

    def get_research_content(self):
        return self.lineEdit.text()

    def get_files_from_table(self):
        files = []
        row = self.tableWidget.rowCount()
        for i in range(row):
            files.append(self.tableWidget.item(i, 0).text())
        return files

    def creat_tableWidget(self, files, nums=[], poss=[]):
        self.tableWidget.clear()
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(len(files))
        self.tableWidget.setColumnWidth(0, 640)
        self.tableWidget.setColumnWidth(1, 80)
        self.tableWidget.setHorizontalHeaderLabels(['文件', "词频", "位置"])
        if files:
            row = 0
            for file in files:
                newItem = QtWidgets.QTableWidgetItem(file)
                self.tableWidget.setItem(row, 0, newItem)
                row += 1
        if nums:
            row = 0
            for num in nums:
                newItem = QtWidgets.QTableWidgetItem(str(num))
                self.tableWidget.setItem(row, 1, newItem)
                row += 1
        if poss:
            row = 0
            for pos in poss:
                newItem = QtWidgets.QTableWidgetItem(str(pos)[1:-1])
                self.tableWidget.setItem(row, 2, newItem)
                row += 1
    
    def creat_tableWidget1(self, files, nums=[]):
        self.tableWidget.clear()
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(files))
        self.tableWidget.setColumnWidth(0, 640)
        self.tableWidget.setColumnWidth(1, 80)
        self.tableWidget.setHorizontalHeaderLabels(['文件', "状态"])
        if files:
            row = 0
            for file in files:
                newItem = QtWidgets.QTableWidgetItem(file)
                self.tableWidget.setItem(row, 0, newItem)
                row += 1
        if nums:
            row = 0
            for num in nums:
                newItem = QtWidgets.QTableWidgetItem(str(num))
                self.tableWidget.setItem(row, 1, newItem)
                row += 1

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message', "确认退出？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def search(self):
        def word_result(freqs, word):
            result = []
            for word_tuple in freqs:
                temp = {"file": word_tuple[0], "num": 0, "pos": []}
                if " " not in word:
                    for word_and_freq_dict in word_tuple[1]:
                        if word_and_freq_dict["word"] == word:
                            temp["num"] = len(word_and_freq_dict["pos"])
                            temp["pos"] = word_and_freq_dict["pos"]
                else:
                    pos = KMP.positions(File.File(word_tuple[0]).get_content(), word)
                    temp["num"] = len(pos)
                    temp["pos"] = pos
                result.append(temp)

            def num(result):
                return result["num"]

            result.sort(key=num, reverse=True)
            return result

        self.search_status = self.get_research_content()
        self.statusBar().showMessage(self.get_research_content() + " 的检索结果")
        files = self.get_files_from_table()
        if not self.freqs:
            self.freqs = [(file, File.cal_words_positions(files=[file])) for file in files]
        temp_result = []
        result = []
        for word in self.search_status.split(";"):
            temp_result.append(word_result(self.freqs, word))
        for file in files:
            temp = {"file": file, "num": "", "pos": []}
            for i in temp_result:
                for j in i:
                    if j["file"] == file:
                        temp["num"] += str(j["num"]) + "+"
                        temp["pos"].append(j["pos"])
            result.append(temp)

        def num(result):
            return eval(result["num"][:-1])

        result.sort(key=num, reverse=True)
        self.tableWidget.clear()
        files = []
        nums = []
        poss = []
        for i in result:
            files.append(i["file"])
            nums.append(i["num"][:-1])
            poss.append(i["pos"])
        self.creat_tableWidget(files, nums, poss)

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(str(sender) + ' was pressed')

    def itemClicked(self, row, col):
        file = self.tableWidget.item(row, 0).text()
        for i in self.logic_status:
            if i['file']==file and i['result']=="False":
                self.words.clear()
            if i['file']==file and i['result']=="True":
                for word in self.original:
                    self.words.append(word)
        self.statusBar().showMessage(file)
        item_ui = item_UI(file, self.search_status, self.words)
        item_ui.show()
        item_ui.exec_()
