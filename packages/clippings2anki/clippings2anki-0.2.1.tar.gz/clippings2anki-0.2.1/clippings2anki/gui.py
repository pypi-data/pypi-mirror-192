import sys
from PyQt6.QtCore import QObject, QThread, pyqtSignal, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QLineEdit, QMessageBox, QCheckBox, QFrame

import clippings2anki.clippings as clippings


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def __init__(self, input_file, language, output_file, save_json, anki_separator, parent=None):
        super().__init__(parent)
        
        self.input_file = input_file
        self.language = language
        self.output_file = output_file
        self.save_json = save_json
        self.anki_separator = anki_separator
        
    def process(self):
        print("Processing...")
        
        clippings.main_cli(self.input_file, self.language, self.output_file, save_json=self.save_json, anki_separator=self.anki_separator, qt_signal=self.progress)
        
        self.finished.emit()
        
    def finished_popup(self):
        print("Finished processing")
        
        popup = QMessageBox()
        popup.setWindowTitle("clippings2anki finished")
        popup.setText(f"Finished processing your Kindle clippings\nOutput file for anki import: {self.output_file}")
        _ = popup.exec()


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clippings2Anki")
        # self.resize(800, 600)
        # set minimum width
        self.setMinimumWidth(600)
        
        layout = QVBoxLayout()
        # set vertical alignment to center
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # chosen file label
        self.chosen_file_label = QLabel("No file chosen")
        layout.addWidget(self.chosen_file_label)

        # choose file button
        self.input_file = None
        choose_file_button = QPushButton("Choose Kindle clippings file")
        choose_file_button.clicked.connect(self.choose_file)
        layout.addWidget(choose_file_button)
        
        # language input
        language_label = QLabel("Language (e.g. \"english\", \"french\", \"german\")")
        self.language_input = QLineEdit("english")
        self.language_input.textChanged.connect(self.update_start_button)
        layout.addWidget(language_label)
        layout.addWidget(self.language_input)
        
        # more options button
        self.more_options_button = QPushButton("More options")
        self.more_options_button.clicked.connect(self.more_options)
        layout.addWidget(self.more_options_button)
        
        # more options layout
        self.more_options_frame = QFrame()
        self.more_options_layout = QVBoxLayout()
        # add border around layout
        self.more_options_layout.setContentsMargins(10,10,10,10)        
        
        # output file input
        output_file_label = QLabel("Output file")
        self.output_file_input = QLineEdit("Kindle flashcards.txt")
        self.more_options_layout.addWidget(output_file_label)
        self.more_options_layout.addWidget(self.output_file_input)
        
        # json checkbox
        self.json_checkbox = QCheckBox("Save json file")
        self.more_options_layout.addWidget(self.json_checkbox)
        
        # anki separator input
        anki_separator_label = QLabel("Word-definition separator in output (tab by default)")
        self.anki_separator_input = QLineEdit("\\t")
        self.more_options_layout.addWidget(anki_separator_label)
        self.more_options_layout.addWidget(self.anki_separator_input)
        
        # add more options layout to main layout
        self.more_options_frame.setLayout(self.more_options_layout)
        layout.addWidget(self.more_options_frame)
        self.more_options_frame.hide()
        
        # start layout
        start_layout = QVBoxLayout()
        start_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        start_layout.setContentsMargins(0,20,0,0)
        
        # start button
        self.start_button = QPushButton("Start")
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.start)
        start_layout.addWidget(self.start_button)
        
        # progress bar
        progress_bar_label = QLabel("Progress")
        start_layout.addWidget(progress_bar_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        start_layout.addWidget(self.progress_bar)
        
        layout.addLayout(start_layout)

        # show layout
        # layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        
    def choose_file(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '', 'Kindle Clippings file (*.txt)')
        if path != ('', ''):
            print("File path : "+ path[0])
            
            # update label
            self.chosen_file_label.setText("Chosen file: " + path[0])
            self.input_file = path[0]
            
            self.update_start_button()
            
    def more_options(self):
        # toggle more options frame
        self.more_options_frame.setVisible(not self.more_options_frame.isVisible())
                
    def update_start_button(self):
        if self.language_input.text() != "" and self.input_file:
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)
            
    def start(self):
        # disable start button
        self.start_button.setEnabled(False)
        
        self.progress_bar.setValue(0)
        
        # start processing
        self.worker_thread = QThread()
        
        self.worker = Worker(self.input_file, self.language_input.text(), self.output_file_input.text(), self.json_checkbox.isChecked(), self.anki_separator_input.text().encode().decode("unicode_escape"))
        
        self.worker.progress.connect(self.progress_bar.setValue)    
        self.worker.moveToThread(self.worker_thread)
        self.worker.finished.connect(self.worker.finished_popup)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.started.connect(self.worker.process)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.start()
        

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    app.exec()
    

if __name__ == "__main__":
    main()
