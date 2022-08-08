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
MENU_ITEM_REBUILD = "&REBUILD"

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
    id = None  # this is id to update
    def update_with_decomp(self):
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

    def update_decomp_v2(self):
        self.progress.emit("updating")
        updatedList = update_decompstrV2(self.id)
        self.progress.emit("updated " + str(len(updatedList)) + " " + ','.join(updatedList))
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
        self.submit = QPushButton()
        self.textInputs = [self.hanziInputBox,
                           self.keywordInputBox,
                           self.submit]
        self.stepLabel = QLabel()
        # Instance Properties for UIComponents

        self.setupUI()

    def setupUI(self):
        # Setup Main window and Configure Layout
        frame = QFrame()
        main_layout = QVBoxLayout()

        for w in self.textInputs + [self.submit, self.stepLabel, self.stepLabel]:
            main_layout.addWidget(w)
        frame.setLayout(main_layout)
        self.setCentralWidget(frame)
        self.hanziInputBox.setMaxLength(1)
        myFont = QFont()
        myFont.setPointSize(12)
        self.stepLabel.setFont(myFont)
        self.stepLabel.setLineWidth(100)
        self.stepLabel.setWordWrap(True)
        self.submit.setText("Submit")
        self.setTabOrder(self.keywordInputBox, self.submit)
        subscribe(self.submit.pressed, [self.submit_pressed])

        # Setup menu bar and configure menu actions
        # menubar = self.window().menuBar()
        # menubar.setNativeMenuBar(False)
        # file_menu = menubar.addMenu(MENU_TEXT)
        # update_action = QAction(MENU_ITEM_UPDATE, self.window())
        # update_action.triggered.connect(self.runLongTask(self.worker.update_with_decomp))
        # file_menu.addAction(update_action)

        # rebuild_action = QAction(MENU_ITEM_REBUILD, self.window())
        # rebuild_action.triggered.connect(update_glossary)

        # file_menu.addAction(rebuild_action)


    def reportProgress(self, progress_str):
        self.stepLabel.setText(progress_str)
    def runLongTask(self, longFunction):

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Make Worker
        #self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(longFunction)
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
        #self.thread.finished.connect(self.stepLabel.hide)

    def submit_pressed(self):
        if self.is_ready():
            """
            ok so we need to update worker id because runLongTask needs to take a worker function
            that it will invorke later. so worker functions cant take parameters
            so if your wondering why this code is trash thats why. i seriously need to refactor all this
            
            """
            Worker.id = update_hanzi(HanziObject(keyword=self.keywordInputBox.text(),
                              hanzi=self.hanziInputBox.text()))
            self.worker = Worker()
            self.runLongTask(self.worker.update_decomp_v2)
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
