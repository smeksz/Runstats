import math, time
from Clipboard_watcher import ClipboardWatcher
from PySide6.QtCore import QObject, Signal, Slot

class ClipboardWorker(QObject):
    data_ready = Signal(dict)

    def __init__(self):
        super().__init__()
        self.saved_coords = None
        self.running = True
        self.clipboard_watcher = ClipboardWatcher(self.on_clipboard_change)

    def angle_and_distance_between_coordinates(self,x1,z1,x2,z2):
        dx = x2 - x1
        dz = z2 - z1
        angle = -math.degrees(math.atan2(dx, dz))
        distance = math.sqrt(dx*dx + dz*dz)

        return [round(angle,2), round(distance,0)]

    def liststrings_to_float(self,list):
        new_list = []
        for x in list:
            new_list.append(float(x))
        return new_list

    def listfloats_to_int(self,list):
        # ALSO FLOORS
        new_list = []
        for x in list:
            new_list.append(int(math.floor(x)))
        return new_list

    def on_clipboard_change(self,new_clipboard):
        print("Copied:",new_clipboard)
        if new_clipboard.find("/execute") == -1:
            return
        # Getting initial position
        if self.saved_coords == None:
            self.saved_coords = new_clipboard.split("@s ")[1].split(" ")
            del self.saved_coords[-2:]
            self.saved_coords = self.liststrings_to_float(self.saved_coords)
            return

        # Getting angle and distance to intial position from current position

        # Get cur coords
        cur_coords = new_clipboard.split("@s ")[1].split(" ")
        del cur_coords[-2:]
        cur_coords = self.liststrings_to_float(cur_coords)
        # Get angle and distance
        angle_and_distance = self.angle_and_distance_between_coordinates(
            cur_coords[0],cur_coords[2],
            self.saved_coords[0],self.saved_coords[2]
            )
        self.data_ready.emit({
            "angle": angle_and_distance[0],
            "distance": int(math.floor(angle_and_distance[1])),
            "saved_coords": self.listfloats_to_int(self.saved_coords),
            "cur_coords": self.listfloats_to_int(cur_coords)
        })
                
    @Slot()
    def stop(self):
        print("Stopping clipboard worker")
        self.running = False

        if self.clipboard_watcher:
            self.clipboard_watcher.stop()

    def run(self):
        self.clipboard_watcher.start()
   # clipboard_watcher.stop()