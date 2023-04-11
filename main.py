import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QListView, QAbstractItemView, QLabel, QWidget, \
    QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit
from PyQt5 import QtGui

from helpers.stylesheets import right_pane_style
from models.sound_effect import SoundEffect


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.file_list = []
        self.soundeffect_list = []

        self.setWindowTitle("AKAI MPX8 Manager")
        self.setWindowIcon(QtGui.QIcon("images/logo.png"))
        self._setup_left_pane()
        self._setup_right_pane()

        self._setup_pane_layout()

        self.current_edit_pane = None
        self._setup_edit_pane()


        # Create a layout for the main window
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.pane_layout)
        self.main_layout.addWidget(self.edit_pane)

        # Create a central widget and set the main layout
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def _setup_left_pane(self):
        self.left_pane = QLabel("Drag and drop files here")
        self.left_pane.setAcceptDrops(True)
        self.left_pane.setAlignment(Qt.AlignCenter)
        self.left_pane.setStyleSheet("QLabel { border: 2px dashed gray; }")
        self.left_pane.setMinimumSize(200, 300)
        self.left_pane.dragEnterEvent = self.dragEnterEvent
        self.left_pane.dropEvent = self.dropEvent

    def _setup_right_pane(self):
        self.right_pane = QListView()
        self.right_pane.setSelectionMode(QAbstractItemView.SingleSelection)
        self.right_pane.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.right_pane.setStyleSheet(right_pane_style)
        self.right_pane.clicked.connect(self.show_edit_pane)
        # Create a model for the right pane
        self.model = QStandardItemModel(self.right_pane)
        # Set the model for the right pane
        self.right_pane.setModel(self.model)

    def _setup_edit_pane(self):
        # Create a layout for the edit pane
        edit_layout = QFormLayout()
        self.output_name_edit = QLineEdit()
        self.cut_from_edit = QLineEdit()
        self.cut_to_edit = QLineEdit()
        edit_layout.addRow(QLabel("Name:"), self.output_name_edit)
        edit_layout.addRow(QLabel("Cut from:"), self.cut_from_edit)
        edit_layout.addRow(QLabel("Cut to:"), self.cut_to_edit)
        self.edit_pane = QWidget()
        self.edit_pane.setLayout(edit_layout)
        self.edit_pane.hide()

    def _setup_pane_layout(self):
        self.pane_layout = QHBoxLayout()
        self.pane_layout.addWidget(self.left_pane)
        self.pane_layout.addWidget(self.right_pane)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            extension = path.rsplit(".", 1)[1]
            if os.path.isfile(path) and extension.lower() in ("wav", "mp3", "opus"):
                if path not in self.file_list:
                    self.file_list.append(path)
                    item = QStandardItem(os.path.basename(path))
                    self.model.appendRow(item)
                    soundeffect = SoundEffect(source_path=path, output_path="", output_name="")
                    self.soundeffect_list.append(soundeffect)
        print(self.soundeffect_list)

    def show_edit_pane(self, index):
        # Hide the currently shown edit pane, if any
        if self.current_edit_pane is not None:
            self.current_edit_pane.hide()

        # Create a new edit pane
        self.current_edit_pane = QWidget()
        edit_layout = QFormLayout()

        # Get the selected item's name
        name = self.model.itemFromIndex(index).text()

        # Create a label with the name
        label_name = QLabel(name)
        edit_layout.addRow("Name:", label_name)

        # Create an input box for the output name
        output_name_input = QLineEdit()
        edit_layout.addRow("Output Name:", output_name_input)

        # Create an input box for the starting time
        start_time_input = QLineEdit()
        edit_layout.addRow("Start Time:", start_time_input)

        # Create an input box for the ending time
        end_time_input = QLineEdit()
        edit_layout.addRow("End Time:", end_time_input)

        # Set the layout for the edit pane
        self.current_edit_pane.setLayout(edit_layout)

        # Add the edit pane to the main layout, to the right of the right pane
        self.main_layout.addWidget(self.current_edit_pane)

        # Show the edit pane
        self.current_edit_pane.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
