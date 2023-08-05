import sys
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QLineEdit, QMessageBox

import clippings2anki.clippings as clippings


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def __init__(self, input_file, language, parent=None):
        super().__init__(parent)
        
        self.input_file = input_file
        self.language = language
        
        self.output_file = "Kindle flashcards.txt"
        
    def process(self):
        print("Processing...")
        
        clippings.main_cli(self.input_file, self.language, self.output_file, save_json=False, anki_separator="\t", qt_signal=self.progress)
            
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

        # add label
        title = QLabel("Clippings2Anki")
        layout.addWidget(title)

        # chosen file label
        self.chosen_file_label = QLabel("No file chosen")
        layout.addWidget(self.chosen_file_label)

        # choose file button
        self.input_file = None
        choose_file_button = QPushButton("Choose file")
        choose_file_button.clicked.connect(self.choose_file)
        layout.addWidget(choose_file_button)
        
        # language input
        language_label = QLabel("Language (e.g. \"english\", \"french\", \"german\")")
        self.language_input = QLineEdit("english")
        self.language_input.textChanged.connect(self.update_start_button)
        layout.addWidget(language_label)
        layout.addWidget(self.language_input)
        
        # start button
        self.start_button = QPushButton("Start")
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.start)
        layout.addWidget(self.start_button)
        
        # progress bar
        progress_bar_label = QLabel("Progress")
        layout.addWidget(progress_bar_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

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
        self.worker = Worker(self.input_file, self.language_input.text())
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
