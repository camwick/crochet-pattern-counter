import sys, os
from pathlib import Path
from PyQt6 import QtWidgets, uic
from PatternCounter import PixelCounter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

imagesPath = "./images/"
countedPath = "./counted/"

# count the sqaures and output file
if not os.path.exists(countedPath):
    os.mkdir(countedPath)
if not os.path.exists(imagesPath):
    os.mkdir(imagesPath)

class MainWindow(QtWidgets.QMainWindow):
    class Event(FileSystemEventHandler):
        def __init__(self, fileBox):
            super().__init__()
            self.fileBox = fileBox

        def on_created(self, event):
            file = event.src_path.split("/")[-1]
            self.fileBox.addItem(file)
        
        def on_deleted(self, event):
            file = event.src_path.split("/")[-1]
            self.fileBox.removeItem(self.fileBox.findText(file))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(self.fetch_resource("counterUI.ui") , self)
        
        # put file names in combo box
        files = os.listdir(imagesPath)
        for file in files:
            self.fileBox.addItem(file)

        # connecting signals
        self.pushButton.clicked.connect(self.countSquares)
        self.fileBox.currentIndexChanged.connect(self.indexChanged)

        # initiating watchdog thread to update file combo box
        self.event_handler = MainWindow.Event(self.fileBox)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, imagesPath, recursive=False)
        self.observer.start()

    def countSquares(self):
        self.pushButton.setEnabled(False)

        # check if ignored number of rows/columns are numbers
        if not self.topRowsLineEdit.text().isdigit():
            self.topRowsLineEdit.setText("0")
        if not self.bottomRowsLineEdit.text().isdigit():
            self.bottomRowsLineEdit.setText("0")
        if not self.rightColumnsLineEdit.text().isdigit():
            self.rightColumnsLineEdit.setText("0")
        if not self.leftColumnsLineEdit.text().isdigit():
            self.leftColumnsLineEdit.setText("0") 

        # set current image file path
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
            counter = PixelCounter(imgPath, 
                                   countedPath,
                                   int(width), 
                                   int(length), 
                                   int(threshold), 
                                   (int(self.topRowsLineEdit.text()),
                                        int(self.bottomRowsLineEdit.text()),
                                        int(self.leftColumnsLineEdit.text()),
                                        int(self.rightColumnsLineEdit.text())))
        except ValueError:
            self.warning("Invalid Value","Either the 'Width', 'Length', or 'Count Threshold' fields contain data that isn't a number")
            self.pushButton.setEnabled(True)
            return
        
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
        
    def closeEvent(self, event) -> None:
        # closing observer thread
        self.observer.stop()
        self.observer.join()

        return super().closeEvent(event)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()