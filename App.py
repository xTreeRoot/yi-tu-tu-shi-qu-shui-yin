import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import cv2
from get_origin_picture import process_image
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = '去除亿图图示水印工具'
        self.fileName = None
        self.left = 0
        self.top = 100
        self.width = 1900
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 获取当前屏幕的大小
        screen_size = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen_size.width(), screen_size.height()

        # 计算窗口应该显示的位置，并设置窗口的位置和大小
        x = (screen_width - self.width) / 2
        y = (screen_height - self.height) / 2
        self.setGeometry(int(x), int(y), self.width, self.height)


        # 创建选择图片按钮
        self.button = QPushButton('选择图片', self)
        self.button.setToolTip('选择要处理的图片')
        self.button.move(20, 20)
        self.button.clicked.connect(self.selectImage)

        # 创建处理图片按钮
        self.processButton = QPushButton('处理图片', self)
        self.processButton.setToolTip('对选定的图片进行处理')
        self.processButton.move(20, 70)
        self.processButton.clicked.connect(self.processImage)

        # 显示原始图片
        self.imageLabel = QLabel(self)
        self.imageLabel.move(300, 50)
        self.imageLabel.resize(700, 500)

        # 显示处理结果图片
        self.resultLabel = QLabel(self)
        self.resultLabel.move(1100, 50)
        self.resultLabel.resize(700, 500)

        # 显示窗口
        self.show()

    def selectImage(self):
        # 选择要处理的图片
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Images (*.png *.xpm *.jpg *.jpeg)", options=options)
        if fileName:
            self.fileName = fileName
            pixmap = QPixmap(self.fileName)
            pixmap = pixmap.scaled(700, 500)
            self.imageLabel.setPixmap(pixmap)

    def processImage(self):
        result = process_image(self.fileName)
        resultPath = './public/result.png'
        cv2.imwrite(resultPath, result)

        pixmap = QPixmap(resultPath)
        pixmap = pixmap.scaled(700, 500)
        self.resultLabel.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())