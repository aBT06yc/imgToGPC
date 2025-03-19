import sys
import cv2
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
from imgFun import make_picture,make_gpc


class MainWindow(QMainWindow): 
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        uic.loadUi("app.ui", self)

        self.xBox.valueChanged.connect(self.doPrint)
        self.yBox.valueChanged.connect(self.doPrint)
        self.invertedColour.stateChanged.connect(self.doPrint)
        
        #self.optimization.stateChanged.connect(self.doPrint)
        #self.colourBox. activated.connect(self.doPrint)
        
        self.fileButton.clicked.connect(self.selectFile)
        self.clipboardButton.clicked.connect(self.load_image_from_clipboard)

        self.blackBorderMinSlider.valueChanged.connect(self.doPrint)
        self.blackBorderMaxSlider.valueChanged.connect(self.doPrint)
        self.makeGPCButton.clicked.connect(self.makeGPC)
        self.copyButton.clicked.connect(self.copyText)

        self.canny.stateChanged.connect(self.doPrint)
        self.tLower.valueChanged.connect(self.doPrint)
        self.tUpper.valueChanged.connect(self.doPrint)
        self.cannyTypeBox.currentIndexChanged.connect(self.doPrint)

    def load_image_from_clipboard(self):
        clipboard = QApplication.clipboard()
        pixmap = clipboard.pixmap()  # Получаем изображение из буфера
        if not pixmap.isNull():
            pixmap.save("clipboard.png")
            self.fileName = "./clipboard.png"
            self.doPrint()
            #print(pixmap)
        else:
            print("Not a image in clipboard")

    def selectFile(self):
        self.fileName = QFileDialog.getOpenFileName(self,"Choose image", "", "Image Files (*.jfif *.png *.jpg *.jpeg *.bmp *.tiff *.tif)")[0]
        self.doPrint()

    def doPrint(self):

        invColour = self.invertedColour.isChecked()
        canny = self.canny.isChecked() 
        file = "test.jpg"
        tLower = int(self.tLower.value())
        tUpper = int(self.tUpper.value())
        x = int(self.xBox.text())
        y = int(self.yBox.text())   
        black_border_max = int(self.blackBorderMaxSlider.value())
        black_border_min = int(self.blackBorderMinSlider.value())
        canny_type = self.cannyTypeBox.currentText()

        try:
            try:file = str(self.fileName)
            except: print("Select your img file!")

            black = make_picture(file,x,y,black_border_min,black_border_max,invColour,canny,tLower,tUpper,canny_type)

            self.blackLable.setText(f"{black:.2f} %") 
            self.recLable.setText(f"{"make with black" if black < 50 else "make with white"}") 

            pixmap =  QtGui.QPixmap('example.tiff')
            self.image.setPixmap(pixmap)  
        
        except Exception as _ex:
            print(f"Smth wrong -> {_ex}")
            
        
    def makeGPC(self):

        colour = self.colourBox.currentText()
        x = int(self.xBox.text())
        y = int(self.yBox.text()) 
        black_border_min = int(self.blackBorderMinSlider.value())
        black_border_max = int(self.blackBorderMaxSlider.value())
        optimization = self.optimization.isChecked()

        try:
            make_gpc(x,y,colour,black_border_min,black_border_max,optimization)
            with open("myScript.gpc", "r") as file:
                text = file.read()
            self.gpcText.setText(text)

        except Exception as _ex:
            print(f"Smth wrong -> {_ex}")
   
    def copyText(self):
        self.gpcText.selectAll()
        self.gpcText.copy()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
