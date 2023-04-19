import sys, os
from pathlib import Path
from PyQt6 import QtWidgets, uic
from PatternCounter import PixelCounter

imagesPath = "./images/"
countedPath = "./counted/"

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(self.fetch_resource("counterUI.ui") , self)
        
        # put file names in combo box
        files = os.listdir(imagesPath)
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
            imgPath = imagesPath + self.fileBox.currentText()

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
        if not os.path.exists(countedPath):
            os.mkdir(countedPath)
        
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

    def fetch_resource(self, resource_path: Path) -> Path:
        try:  # running as *.exe; fetch resource from temp directory
            base_path = Path(sys._MEIPASS)
        except AttributeError:  # running as script; return unmodified path
            return resource_path
        else:  # return temp resource path
            return base_path.joinpath(resource_path)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()