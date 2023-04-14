import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QListView, QAbstractItemView, QLabel, QWidget, \
    QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5 import QtGui

from helpers.ffmpeg_helpers import edit_audio
from helpers.helpers import validate_float_input, strip_empty_to_none
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
        self._setup_left_yt_input()
        self._setup_right_pane()

        # Create a start batch button
        self.start_batch_button = QPushButton("Start Batch")
        self.start_batch_button.setEnabled(False)  # Disable button by default
        self.start_batch_button.clicked.connect(self.start_batch)

        self._setup_pane_layout()

        self.current_edit_pane = None

        # Create a layout for the bottom part of the window
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        # Create a layout for the main window
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.pane_layout)
        self.main_layout.addLayout(bottom_layout)

        # Create a central widget and set the main layout
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def _setup_left_pane(self):
        self.left_pane = QLabel("Drag and drop files here")
        self.left_pane.setAcceptDrops(True)
        self.left_pane.setAlignment(Qt.AlignCenter)
        self.left_pane.setStyleSheet("QLabel { border: 2px dashed gray; }")
        self.left_pane.setMinimumSize(200, 280)
        self.left_pane.dragEnterEvent = self.dragEnterEvent
        self.left_pane.dropEvent = self.dropEvent

    def _setup_left_yt_input(self):
        self.yt_input = QLineEdit()
        self.yt_input.setObjectName("yt_input")
        self.yt_input.setPlaceholderText("Enter YouTube link")
        self.yt_add_button = QPushButton("Add Youtube Link")
        self.yt_add_button.clicked.connect(self.add_yt)

    def _setup_right_pane(self):
        self.right_pane = QListView()
        self.right_pane.setSelectionMode(QAbstractItemView.SingleSelection)
        self.right_pane.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.right_pane.setStyleSheet(right_pane_style)
        self.right_pane.clicked.connect(self.show_edit_pane)
        self.model = QStandardItemModel(self.right_pane)
        self.right_pane.setModel(self.model)

    def _setup_pane_layout(self):
        # Create vertical layout for left pane and input field
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.left_pane)
        left_layout.addWidget(self.yt_input)
        left_layout.addWidget(self.yt_add_button)

        # Create vertical layout for the start button
        button_layout = QVBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.start_batch_button)

        # Create a horizontal layout for the left pane and right pane
        pane_layout = QHBoxLayout()
        pane_layout.addLayout(left_layout)
        pane_layout.addWidget(self.right_pane)

        # Create a top-level layout for the panes and button
        top_layout = QVBoxLayout()
        top_layout.addLayout(pane_layout)
        top_layout.addLayout(button_layout)

        self.pane_layout = top_layout

    def save_sound(self):
        index = self.right_pane.currentIndex()

        # Get the corresponding soundeffect object
        soundeffect = self.soundeffect_list[index.row()]

        # Get the current values in the inputboxes
        output_name = self.current_edit_pane.findChild(QLineEdit, "output_name_input").text()
        start_time = self.current_edit_pane.findChild(QLineEdit, "start_time_input").text()
        end_time = self.current_edit_pane.findChild(QLineEdit, "end_time_input").text()

        # Update the soundeffect object with the current values in the inputboxes
        soundeffect.output_name = output_name
        start_time = strip_empty_to_none(start_time)
        end_time = strip_empty_to_none(end_time)

        if validate_float_input(start_time, "Start-time"):
            soundeffect.start_time = start_time
        if validate_float_input(end_time, "End-time"):
            soundeffect.end_time = end_time

        print(f"Saved: {soundeffect}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def _update_start_batch_button(self):
        # Enable the start batch button if there is at least one item in the list
        self.start_batch_button.setEnabled(len(self.soundeffect_list) > 0)

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            extension = path.rsplit(".", 1)[1]
            if os.path.isfile(path) and extension.lower() in ("wav", "mp3", "opus", "ogg"):
                if path not in self.file_list:
                    self.file_list.append(path)
                    item = QStandardItem(os.path.basename(path))
                    self.model.appendRow(item)
                    soundeffect = SoundEffect(source_path=path, output_path="", output_name="")
                    self.soundeffect_list.append(soundeffect)
                    self._update_start_batch_button()  # Call this method to update the button state

    def add_yt(self):
        if "youtube.com/watch?v=" in self.yt_input.text():
            name = self.yt_input.text().split("/watch?v=")[1]
            if "&" in name:
                name = name.split("&")[0]
            item = QStandardItem(name)
            self.model.appendRow(item)
            soundeffect = SoundEffect(source_path=self.yt_input.text(), output_path="./_output", output_name=name)
            self.soundeffect_list.append(soundeffect)
            self._update_start_batch_button()
        else:
            QMessageBox.warning(None, "Error", f"Not a valid YouTube URL.")

    def start_batch(self):
        # This method will be called when the Start Batch button is clicked
        print("Start Batch button clicked!")
        for se in self.soundeffect_list:
            edit_audio(se.start_time, se.end_time, se.source_path, se.generate_output_path())

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
                    if len(self.file_list) > 0:
                        self.start_batch_button.setEnabled(True)
        print(self.soundeffect_list)

    def show_edit_pane(self, index):
        # Hide the currently shown edit pane, if any
        soundeffect = self.soundeffect_list[index.row()]
        if self.current_edit_pane is not None:
            self.current_edit_pane.hide()
        self.current_edit_pane = QWidget()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_sound)
        edit_layout = QFormLayout()
        name = self.model.itemFromIndex(index).text()
        edit_layout.addRow("Name:", QLabel(name))
        output_name_input = QLineEdit()
        output_name_input.setObjectName("output_name_input")
        output_name_input.setText(str(soundeffect.output_name) if soundeffect.output_name else "")
        edit_layout.addRow("Output Name:", output_name_input)
        start_time_input = QLineEdit()
        start_time_input.setObjectName("start_time_input")
        start_time_input.setText(str(soundeffect.start_time) if soundeffect.start_time else "")
        edit_layout.addRow("Start Time:", start_time_input)
        end_time_input = QLineEdit()
        end_time_input.setObjectName("end_time_input")
        end_time_input.setText(str(soundeffect.end_time) if soundeffect.end_time else "")
        edit_layout.addRow("End Time:", end_time_input)
        edit_layout.addRow(save_button)

        # Set the layout for the edit pane
        self.current_edit_pane.setLayout(edit_layout)
        self.main_layout.addWidget(self.current_edit_pane)
        self.current_edit_pane.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
