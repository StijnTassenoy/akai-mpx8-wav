import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QListView, QAbstractItemView, QLabel, QWidget, \
    QVBoxLayout, QHBoxLayout

from models.sound_effect import SoundEffect


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.soundeffect_list = []

        self.setWindowTitle("AKAI MPX8 Manager")

        # Create the left pane for drag and drop
        self.left_pane = QLabel("Drag and drop files here")
        self.left_pane.setAcceptDrops(True)
        self.left_pane.setAlignment(Qt.AlignCenter)
        self.left_pane.setStyleSheet("QLabel { border: 2px dashed gray; }")
        self.left_pane.setMinimumSize(200, 300)
        self.left_pane.dragEnterEvent = self.dragEnterEvent
        self.left_pane.dropEvent = self.dropEvent

        # Create the right pane for displaying file list
        self.right_pane = QListView()
        self.right_pane.setSelectionMode(QAbstractItemView.SingleSelection)
        self.right_pane.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.right_pane.setStyleSheet(
            """
            QListView {
                font-size: 14px;
                background-color: white;
            }

            QListView::item {
                padding: 3px;
            }

            QListView::item:selected {
                padding: 3px;
                background-color: lightblue;
                border: none;
            }
            """
        )

        # Create a model for the right pane
        self.model = QStandardItemModel(self.right_pane)

        # Set the model for the right pane
        self.right_pane.setModel(self.model)

        # Create a layout for the panes
        pane_layout = QHBoxLayout()
        pane_layout.addWidget(self.left_pane)
        pane_layout.addWidget(self.right_pane)

        # Create a layout for the main window
        main_layout = QVBoxLayout()
        main_layout.addLayout(pane_layout)

        # Create a central widget and set the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Initialize the file list
        self.file_list = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path) and path.endswith(".wav"):
                if path not in self.file_list:
                    self.file_list.append(path)
                    item = QStandardItem(os.path.basename(path))
                    self.model.appendRow(item)
                    soundeffect = SoundEffect(source_path=path, output_path="", output_name="")
                    self.soundeffect_list.append(soundeffect)
        print(self.soundeffect_list)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
