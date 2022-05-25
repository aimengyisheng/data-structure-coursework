import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog


class Ui_FileDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.title = '选择需要导入的TXT文档'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "选择要导入的文件", "", "TXT Files (*.txt)", options=options)
        if files:
            return files

    def saveFileDialog(self):
        pass
