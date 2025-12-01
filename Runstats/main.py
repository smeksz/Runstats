from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread, QMetaObject, Qt, Signal
from Layouts.window import Ui_Form
from Clipboard import ClipboardWorker
from Statistics import StatisticsWorker
from Latest_world_path import LatestWorldWorker
from pathlib import Path
import sys, math, os, json


class MainWindow(QMainWindow):
    update_statistics_world_path = Signal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        #self.ui.pushButton.clicked.connect(self.on_click)
        self.get_latest_world_path()


        self.start_threads()

    def get_latest_world_path(self):
        speedrunigt_path = os.path.join(Path.home(),"speedrunigt/latest_world.json")
        if not os.path.exists(speedrunigt_path):
            raise ValueError(f"Error: {speedrunigt_path} is not a valid path")
        with open(speedrunigt_path, 'r') as file:
            self.latest_world_data = json.load(file)
        self.latest_world_path = self.latest_world_data['world_path']
    
    def start_threads(self):
        # Latest world
        self.latest_world_thread = QThread()
        self.latest_world_worker = LatestWorldWorker()
        self.latest_world_worker.moveToThread(self.latest_world_thread)
        self.latest_world_thread.started.connect(self.latest_world_worker.run)
        self.latest_world_worker.data_ready.connect(self.latest_world_updated)
        self.latest_world_thread.start()

        #Clipboard
        self.clipboard_thread = QThread()
        self.clipboard_worker = ClipboardWorker()
        self.clipboard_worker.moveToThread(self.clipboard_thread)
        self.clipboard_thread.started.connect(self.clipboard_worker.run)
        self.clipboard_worker.data_ready.connect(lambda data: print("Clipboard Data:", data))
        self.clipboard_thread.start()

        #Statistics
        self.stats_thread = QThread()
        self.stats_worker = StatisticsWorker(self.latest_world_path)
        self.stats_worker.moveToThread(self.stats_thread)
        self.update_statistics_world_path.connect(self.stats_worker.latest_world_updated)
        self.stats_thread.started.connect(self.stats_worker.run)
        self.stats_worker.data_ready.connect(self.statistics_data_emitted)
        self.stats_thread.start()
    

    def statistics_data_emitted(self,data):
        print("Satistics Data:", data)
        # Save stats data to json file
        runstats_path = os.path.join(self.latest_world_path,"stats/runstats.json")
        if os.path.exists(runstats_path):
            with open(runstats_path,'r') as file:
                self.old_json = json.load(file)
        else:
            self.old_json = {"statistics":[]}
        self.old_json["statistics"].append(data)
        with open(runstats_path,'w') as file:
            json.dump(self.old_json,file,indent=4)



    def latest_world_updated(self,data):
        print("Latest world path updated to", data)
        self.latest_world_path = data
        self.update_statistics_world_path.emit(data)

        
    def stop_threads(self):
        QMetaObject.invokeMethod(
            self.latest_world_worker,
            "stop",
            Qt.BlockingQueuedConnection
        )
        QMetaObject.invokeMethod(
            self.clipboard_worker,
            "stop",
            Qt.BlockingQueuedConnection
        )

        QMetaObject.invokeMethod(
            self.stats_worker,
            "stop",
            Qt.BlockingQueuedConnection
        )
        self.latest_world_thread.quit()
        self.latest_world_thread.wait()
        self.stats_thread.quit()
        self.stats_thread.wait()
        self.clipboard_thread.quit()
        self.clipboard_thread.wait()

    def closeEvent(self,event):
        print("Closing window and stopping threads...")
        self.stop_threads()
        event.accept()

app = QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec())
