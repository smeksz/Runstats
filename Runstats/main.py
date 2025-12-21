from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread, QMetaObject, Qt, Signal, QCoreApplication
from PySide6.QtGui import QPixmap
from Layouts.window import Ui_Runstats
from Clipboard import ClipboardWorker
from Statistics import StatisticsWorker
from Latest_world_path import LatestWorldWorker
from Qudrant_image_gen import QudrantGridWorker
from Layouts.GridWidget import GridWidget
from pathlib import Path
import sys, math, os, json, appdirs
import resources_rc


class MainWindow(QMainWindow):
    update_statistics_world_path = Signal(str)

    def __init__(self):
        print("--------------------------------------------------------------------------\n\t\t\tSTARTING RUNSTATS\t\t\t\n--------------------------------------------------------------------------")
        super().__init__()
        self.ui = Ui_Runstats()
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

        # Quadrant
        self.quadrant_thread = QThread()
        self.quadrant_worker = QudrantGridWorker()
        self.quadrant_worker.moveToThread(self.quadrant_thread)
        self.quadrant_thread.started.connect(self.quadrant_worker.run)
        self.quadrant_worker.data_ready.connect(self.quadrant_grid)
        self.quadrant_thread.start()

        #Clipboard
        self.clipboard_thread = QThread()
        self.clipboard_worker = ClipboardWorker()
        self.clipboard_worker.moveToThread(self.clipboard_thread)
        self.clipboard_thread.started.connect(self.clipboard_worker.run)
        self.clipboard_worker.data_ready.connect(self.clipboard_data_emitted)
        self.clipboard_thread.start()

        #Statistics
        self.stats_thread = QThread()
        self.stats_worker = StatisticsWorker()
        self.stats_worker.moveToThread(self.stats_thread)
        self.update_statistics_world_path.connect(self.stats_worker.latest_world_updated)
        self.stats_thread.started.connect(self.stats_worker.run)
        self.stats_worker.data_ready.connect(self.statistics_data_emitted)
        self.stats_thread.start()
    
    def quadrant_grid(self,data):
        print("Received quadrant grid:",data)
        self.ui.fort_quadrant.setPixmap(data.scaled(
        self.ui.fort_quadrant.size(),
        Qt.KeepAspectRatio,
        Qt.FastTransformation  # prevents blurring
    ))
        #self.ui.label.setText("PLEASE PLEASE PLEASE")
    
    def set_text(self,object,text):
        object.setText(QCoreApplication.translate("Runstats", text, None))

    def clipboard_data_emitted(self, data):
        print("Clipboard Data:", data)
        saved_coords = data.get("saved_coords")
        self.set_text(self.ui.hp_location,f"{saved_coords[0]}, {saved_coords[1]}, {saved_coords[2]}")
        self.set_text(self.ui.hp_distance, str(data.get("distance")))
        self.set_text(self.ui.hp_angle, str(data.get("angle")))


    def statistics_data_emitted(self,data):
        print("Satistics Data:", data)
        # Save stats data to json file
        #runstats_path = os.path.join(self.latest_world_path,"stats/runstats.json")
        runstats_folder_path = os.path.join(appdirs.user_data_dir(),"runstats")
        if not Path(runstats_folder_path).is_dir():
            os.makedirs(runstats_folder_path, exist_ok=True)

        runstats_path = os.path.join(appdirs.user_data_dir(),os.path.join("runstats",self.get_latest_world_name()))
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
        self.get_latest_world_name()

    def get_latest_world_name(self):
        return self.latest_world_path.split("/")[-1:][0]
        
    def stop_threads(self):
        QMetaObject.invokeMethod(
            self.latest_world_worker,
            "stop",
            Qt.BlockingQueuedConnection
        )
        QMetaObject.invokeMethod(
            self.quadrant_worker,
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
        self.quadrant_thread.quit()
        self.quadrant_thread.wait()
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
