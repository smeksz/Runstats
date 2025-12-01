from PySide6.QtCore import QObject, Signal, Slot, QTimer
from pathlib import Path
import os, json

class LatestWorldWorker(QObject):
    data_ready = Signal(object)
    
    def __init__(self):
        super().__init__()
        self.running = True

    def get_latest_world_path(self):
        self.speedrunigt_path = os.path.join(Path.home(),"speedrunigt/latest_world.json")
        if not os.path.exists(self.speedrunigt_path):
            raise ValueError(f"Error: {self.speedrunigt_path} is not a valid path")
        with open(self.speedrunigt_path, 'r') as file:
            self.latest_world_data = json.load(file)
        self.latest_world_path = self.latest_world_data['world_path']
        self.data_ready.emit(self.latest_world_path)

    @Slot()
    def stop(self):
        print("Stopping latest world worker")
        self.running = False
        if hasattr(self,"timer"):
            self.timer.stop()
    
    @Slot()
    def run(self):
        self.get_latest_world_path()
        # Update latest world path
        self._last_mtime = os.path.getmtime(self.speedrunigt_path)
        self.timer = QTimer()
        self.timer.timeout.connect(self._poll_file)
        self.timer.start(500)

    def _poll_file(self):
        mtime = os.path.getmtime(self.speedrunigt_path)
        if mtime != self._last_mtime:
            self._last_mtime = mtime
            self.get_latest_world_path()
