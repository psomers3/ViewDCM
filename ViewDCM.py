from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import sys
import argparse
import numpy as np
import pydicom


parser = argparse.ArgumentParser()
parser.add_argument("dir")
args = parser.parse_args()

directory = args.dir
if not os.path.isdir(directory):
    print("ERROR: A valid path was not provided.")
    sys.exit(1)


class Viewer(QWidget):
    def __init__(self):
        super().__init__()
        self.image = QGraphicsView()
        color = QColor("black")
        self.image.setBackgroundBrush(QBrush(color))
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.image)
        self.setFocusPolicy(Qt.NoFocus)

    def update_image(self, image):
        image = np.ndarray.astype(((image / np.max(image))*255), dtype=np.uint8)
        height, width, colors = image.shape[0], image.shape[1], 1
        image = QImage(image, width, height, QImage.Format_Indexed8)

        pixmap = QPixmap(image)
        scene = QGraphicsScene()
        scene.addPixmap(pixmap.scaled(self.image.width(), self.image.height(), Qt.KeepAspectRatio))
        self.image.setScene(scene)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.files = sorted([directory + "\\" + name for name in os.listdir(directory) if name[-3:] == "dcm"])
        self.num_files = len(self.files)
        if self.num_files < 1:
            print("No valid dcm files found.")
            sys.exit(1)
        self.index = 0

        self.viewer = Viewer()
        self.setCentralWidget(self.viewer)
        self.setFocusPolicy(Qt.ClickFocus)
        self.viewer.keyPressEvent = self.keyPressEvent
        self.viewer.keyReleaseEvent = self.keyReleaseEvent
        self.setFocus()

        self.show()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Right:
            if self.index < self.num_files - 2:
                self.index += 1
            else:
                return

        elif event.key() == Qt.Key_Left:
            if self.index > 0:
                self.index -= 1
            else:
                return
        else:
            return

        dataset = pydicom.dcmread(self.files[self.index])
        self.viewer.update_image(dataset.pixel_array)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()

    sys.exit(app.exec())