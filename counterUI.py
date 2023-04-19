import sys, os
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PatternCounter import PixelCounter
import time

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("counterUI.ui", self)
        
        # put file names in combo box
        files = os.listdir("./pattern_images")
        for file in files:
            self.fileBox.addItem(file)

        # connect button with clicked signal
        self.pushButton.clicked.connect(self.countSquares)

        self.fileBox.currentIndexChanged.connect(self.indexChanged)

    def countSquares(self):
        self.pushButton.setEnabled(False)

        if self.fileBox.currentIndex() == 0:
            imgPath = self.customPath.text()

            # handle invalid file input
            if imgPath == "" or not os.path.isfile(imgPath):
                self.warning("Invalid File Path", "Double check that your custom file path is valid")
                self.pushButton.setEnabled(True)
                return
        else:
            imgPath = "./pattern_images/" + self.fileBox.currentText()

        # check if width has data
        width = self.width.text()
        if self.lineEditHasNoData(width, "'Width'"):
            self.pushButton.setEnabled(True)
            return

        # check if length das data
        length = self.length.text()
        if self.lineEditHasNoData(length, "'Length'"):
            self.pushButton.setEnabled(True)
            return

        # check if threshold has data
        threshold = self.threshold.text()
        if self.lineEditHasNoData(threshold, "'Count Threshold'"):
            self.pushButton.setEnabled(True)
            return
        
        # try to create a counter object
        try:
            counter = PixelCounter(imgPath, int(width), int(length), int(threshold))
        except ValueError:
            self.warning("Invalid Value","Either the 'Width', 'Length', or 'Count Threshold' fields contain data that isn't a number")
            self.pushButton.setEnabled(True)
            return
        
        # count the sqaures and output file
        counter.count()

        self.pushButton.setEnabled(True)

    def lineEditHasNoData(self, str, widget):
        if str == "":
            self.warning("Missing Data", f"The {widget} field has no data in it.")
            return True
        return False

    def warning(self, title, message):
        QtWidgets.QMessageBox.warning(self, title, message)

    def indexChanged(self):
        if self.fileBox.currentIndex() == 0 and self.customPath.text() != "":
            self.customPath.setText("")

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()