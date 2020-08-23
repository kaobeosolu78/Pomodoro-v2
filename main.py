import time
import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QGridLayout, QAction, QPushButton, QLabel
from PyQt5.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal

class Pom_GUI_Main(QMainWindow):

    pause_timer = pyqtSignal(bool)

    def __init__(self):
        super(Pom_GUI_Main, self).__init__()
        window = QWidget(self)
        self.setCentralWidget(window)
        grid = QGridLayout()

        # thread
        self.threadpool = QThreadPool()

        # label
        self.title = QLabel("test")
        grid.addWidget(self.title, 0, 0)

        # menu
        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")

        new = QAction("Settings", self)
        new.triggered.connect(lambda: self.settings())
        filemenu.addAction(new)

        # buttons
        start = QPushButton("Start")
        start.clicked.connect(lambda: self.start_timer(grid))
        grid.addWidget(start, 3, 0)

        close = QPushButton("Close")
        close.clicked.connect(lambda: self.close())
        grid.addWidget(close, 3, 2)

        self.pom_main = Pomodoro(self)

        self.finish(grid, window)

    def get_settings(self):
        jlk
        pass

    def mod_timer_label(self, k):
        self.title.setText(str(k))

    def start_timer(self, grid):
        self.p_r_bool = True
        self.pause_resume_button = QPushButton("Pause")
        self.pause_resume_button.clicked.connect(lambda: self.pause_resume_timer())
        grid.addWidget(self.pause_resume_button, 3, 1)

        self.worker = Worker(self.pom_main.advance, self.pause_timer)
        self.threadpool.start(self.worker)
        self.worker.signals.time_increment.connect(self.mod_timer_label)

    def pause_resume_timer(self):
        if self.p_r_bool == True:
            self.pause_resume_button.setText("Resume")
            self.pause_timer.emit(True)
            self.p_r_bool = False
        else:
            self.pause_resume_button.setText("Pause")
            self.pause_timer.emit(True)
            self.p_r_bool = True

    def settings(self):
        pass

    def finish(self, grid, window):
        window.setLayout(grid)
        self.setGeometry(300,300,250,150)
        self.setWindowTitle("Pomodoro Timer")
        self.show()


class WorkerSignals(QObject):
    time_increment = pyqtSignal(int)


class Worker(QRunnable):
    def __init__(self, fn, pause_sig):
        super(Worker, self).__init__()
        self.pause_sig = pause_sig
        self.signals = WorkerSignals()
        self.function = fn

    def run(self):
        self.function(self.signals.time_increment, self.pause_sig)


class Timer:
    def __init__(self, total_time, current_action="work"):
        self.total_time = total_time
        self.current_time = 0
        self.current_action = current_action

    def __iter__(self):
        for k in range(self.total_time):
            time.sleep(1)
            self.current_time += 1
            yield k

    def flip_mode(self, work_time, break_time):
        temp = {"work":["break",break_time], "break":["work",work_time]}
        self.current_action,  self.total_time, self.current_time = temp[self.current_action][0], temp[self.current_action][1], 0


class Pomodoro:
    def __init__(self, gui):
        self.gui = gui
        self.current_iteration = 0
        try:
            self.config = self.gui.get_settings()
        except:
            self.config = {"work": 25, "break": 5, "iterations": 4}
        self.time = Timer(self.config["work"])

    def advance(self, time_inc_sig, pause_time_sig):
        it = iter(self.time)
        while self.time.current_time != self.config[self.time.current_action]:
            k = next(it)
            time_inc_sig.emit(k)
            pause_time_sig.connect(self.pause)

        self.extend()
        self.time.flip_mode(self.config["work"], self.config["break"])
        self.advance(time_inc_sig, pause_time_sig)

    def extend(self):
        self.current_iteration += 1
        if self.current_iteration == 10:
            sys.exit("Complete!")
        # print(f"current iteration: {self.current_iteration}")
        if self.current_iteration == self.config["iterations"]:
            self.config["break"] += 5

    def pause(self, boo):
        print('jklsjfkl')
        while boo:
            time.sleep(0.5)

def main():
    app = QApplication(sys.argv)
    a = Pom_GUI_Main()
    sys.exit(app.exec_())

main()