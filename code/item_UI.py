import File
from PyQt5 import QtWidgets, QtGui, QtCore
from Original_Model import item_GUI
from huffman_UI import *
from search_UI import *


class item_UI(QtWidgets.QDialog, item_GUI.Ui_Dialog):
    def __init__(self, file_pos, keyword=None, keyword1=None):
        super(item_UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.file = File.File(file_pos)
        self.init(keyword, keyword1, file_pos.split("/")[-1])

    def init(self, keyword, keyword1, filename):
        self.pushButton.clicked.connect(self.encode)
        self.pushButton_2.clicked.connect(self.decode)
        self.pushButton_3.clicked.connect(self.huffman_codes)
        self.pushButton_4.clicked.connect(self.edit)
        self.toolButton.setShortcut('Ctrl+F')
        self.toolButton.clicked.connect(self.search_substitute)
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+T"), self)
        self.shortcut.activated.connect(self.translate)
        self.textEdit.setText(self.file.get_content())
        if keyword1:
            self.highlight1(keyword1)
        elif keyword:
            self.highlight(keyword)
        self.textEdit.setReadOnly(True)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", filename))
        self.label.setText(_translate("Dialog", "选中内容后，按Ctrl+T翻译"))
        self.current_selected_string = None

    def highlight(self, pattern, color="yellow"):
        if pattern==None:
            return
        for word in pattern.split(";"):
            if word:
                cursor = self.textEdit.textCursor()
                format = QtGui.QTextCharFormat()
                format.setBackground(QtGui.QBrush(QtGui.QColor(color)))
                regex = QtCore.QRegExp(word)
                pos = 0
                content=self.file.get_content().lower()
                content = content.replace('<br />'," ")
                index = regex.indexIn(content, pos)
                while index != -1:
                    cursor.setPosition(index)
                    for i in range(len(word)):
                        cursor.movePosition(QtGui.QTextCursor.Right, 1)
                    cursor.mergeCharFormat(format)
                    pos = index + regex.matchedLength()
                    index = regex.indexIn(content, pos)
    
    def highlight1(self, pattern, color="yellow"):
        if pattern==None:
            return
        for word in pattern:
            if word:
                cursor = self.textEdit.textCursor()
                format = QtGui.QTextCharFormat()
                format.setBackground(QtGui.QBrush(QtGui.QColor(color)))
                regex = QtCore.QRegExp(word)
                pos = 0
                content=self.file.get_content().lower()
                content = content.replace('<br />'," ")
                index = regex.indexIn(content, pos)
                while index != -1:
                    cursor.setPosition(index)
                    for i in range(len(word)):
                        cursor.movePosition(QtGui.QTextCursor.Right, 1)
                    cursor.mergeCharFormat(format)
                    pos = index + regex.matchedLength()
                    index = regex.indexIn(content, pos)

    def highlight_specific(self, pos=(0, 0), color="grey"):
        cursor = self.textEdit.textCursor()
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor(color)))
        cursor.setPosition(pos[0])
        for i in range(pos[1] - pos[0]):
            cursor.movePosition(QtGui.QTextCursor.Right, 1)
        cursor.mergeCharFormat(format)

    def encode(self):
        self.textEdit.setText(self.file.get_encodeStr())

    def decode(self):
        self.textEdit.setText(self.file.get_decodeStr(self.file.get_encodeStr()))

    def huffman_codes(self):
        huffman_codes = self.file.get_huffman_codes()
        form = []
        for item in huffman_codes:
            for tuple in self.file.chars_freqs:
                if item[0] == tuple[0]:
                    form.append((item[0], tuple[1], item[1]))
        huffman_ui = huffman_UI(form)
        huffman_ui.show()
        huffman_ui.exec_()

    def edit(self):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_4.setText(_translate("Dialog", "保存"))
        self.pushButton_4.clicked.connect(self.save)
        self.textEdit.setReadOnly(False)

    def save(self):
        _translate = QtCore.QCoreApplication.translate
        self.file.set_content(self.textEdit.toPlainText())
        self.file.chars_freqs = None
        self.file.Huffman_codes = None
        self.textEdit.setReadOnly(True)
        self.pushButton_4.setText(_translate("Dialog", "编辑"))
        self.pushButton_4.clicked.connect(self.edit)

    def search_substitute(self):
        search_ui = search_UI(self)
        search_ui.show()
        search_ui.exec_()

    def translate(self):
        import requests
        def t(string):
            import bs4
            rooturl = 'http://www.youdao.com/w/'
            finurl = rooturl + string
            res = {}
            res['word'] = string
            try:
                response = requests.get(finurl)
                soup = bs4.BeautifulSoup(response.text, 'html.parser')
                tran = soup.select('.trans-container > ul > li')[0].get_text()
                res['翻译'] = tran
            except IndexError:
                res['翻译'] = "好像没找到这个词..."
            return res

        try:
            internet = requests.get("http://www.baidu.com").status_code
        except:
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("Dialog", "似乎没有联网..."))
            return True
        string = self.textEdit.textCursor().selectedText()
        if string:
            if " " in string:
                _translate = QtCore.QCoreApplication.translate
                self.label.setText(_translate("Dialog", "只能查单词哟~~"))
                return True
            result = t(string)
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("Dialog", result["翻译"]))
        else:
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("Dialog", "没有选中任何内容！"))
