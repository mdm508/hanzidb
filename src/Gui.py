###########################################################################################
#
#
# Header comments (Forbes Painter, 4/22/22, Animate Sprite A7)
#
###########################################################################################

import math
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

###########################################################################################
# Constants

from not_main import *

MENU_TEXT = "&File"
MENU_ITEM_UPDATE= "&UPDATE"

class HanziObject:
    def __init__(self, keyword, hanzi):
        self.keyword = keyword
        self.hanzi = hanzi

def subscribe(action: QAction, subscribers):
    """
    :param action: the action to be published.
    :param subscribers: a list of instance methods that should be invoked when action publishes
    Note* I just like the subscribe analogy better so I named the function subscribe
    """
    for s in subscribers:
        action.connect(s)


# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        """Long-running task."""
        with TinyDB('hanzi.json') as db:
            q = Query()
            for i, h in enumerate(db.all()):
                s = make_decomp_strs(h['decomposition'])
                self.progress.emit("{} of {}\t{}".format(i, len(db), s[0]))
                db.update({'decompstr': s}, q.hanzi == h['hanzi'])
        self.progress.emit("Updating Glossary")
        update_glossary()
        self.finished.emit()

###########################################################################################
#
# The SpritePreview class / widget.  Allows for displaying an animated sprite
# and switching between each frame.
#

class HanziPreview(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hanzi Preview")
        self.hanziInputBox = QLineEdit()
        self.keywordInputBox = QLineEdit()
        self.textInputs = [self.hanziInputBox,
                           self.keywordInputBox]
        self.submit = QPushButton()
        self.stepLabel = QLabel()
        # Instance Properties for UIComponents

        self.setupUI()

    def setupUI(self):
        # Setup Main window and Configure Layout
        frame = QFrame()
        main_layout = QVBoxLayout()

        for w in self.textInputs + [self.submit, self.stepLabel]:
            main_layout.addWidget(w)
        frame.setLayout(main_layout)
        self.setCentralWidget(frame)
        self.stepLabel.hide()
        self.hanziInputBox.setMaxLength(1)
        self.submit.setText("Submit")
        self.setTabOrder(self.keywordInputBox, self.submit)


        subscribe(self.submit.pressed, [self.submit_pressed])
        # Setup menu bar and configure menu actions
        menubar = self.window().menuBar()
        menubar.setNativeMenuBar(False)
        file_menu = menubar.addMenu(MENU_TEXT)
        ## Add a pause menu item
        # pause_action = QAction("&Pause", self.window())
        # subscribe(pause_action.triggered, [self.timer.stop, self.update_start_stop_button_text])
        # file_menu.addAction(pause_action)
        # Add an exit menu item
        update_action = QAction(MENU_ITEM_UPDATE, self.window())
        update_action.triggered.connect(self.runLongTask)
        file_menu.addAction(update_action)

    def reportProgress(self, progress_str):
        self.stepLabel.setText(progress_str)
    def runLongTask(self):
        self.stepLabel.show()

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.submit.setEnabled(False) #dibasle changes to db

        self.thread.finished.connect(
            lambda: self.submit.setEnabled(True)
        )
        self.thread.finished.connect(self.stepLabel.hide)

    def submit_pressed(self):
        if self.is_ready():
            update_hanzi(HanziObject(keyword=self.keywordInputBox.text(),
                              hanzi=self.hanziInputBox.text()))
            self.clear_fields()
        else:
            print("not ready")
    def clear_fields(self):
        self.hanziInputBox.clear()
        self.keywordInputBox.clear()
        self.hanziInputBox.focusWidget()

    def is_ready(self):
        return all([s.text != "" for s in self.textInputs])

def main():
    app = QApplication([])
    # Create our custom widget
    window = HanziPreview()
    menubar = window.menuBar()
    # And show it
    window.show()
    app.exec()


###########################################################################################

if __name__ == "__main__":
    main()
