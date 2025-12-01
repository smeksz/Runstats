import os, json, math
from PySide6.QtCore import QObject, Signal, QTimer, Slot


class StatisticsWorker(QObject):
    data_ready = Signal(object)

    def __init__(self, world_path):
        super().__init__()

        self.latest_world_path = world_path
        self.running = True
        self.states = None
        self.stats_file_path = None

    def get_statistics_file(self,directory_path):
        if not os.path.isdir(directory_path):
            print("Directory does not exist")
            return
        stats_folder_path = os.path.join(directory_path,"stats")
        stats_file_path = ""
        if not os.path.isdir(stats_folder_path):
            print("Directory does not exist")
            return
        for x in os.listdir(stats_folder_path):
            if x == "runstats.json":
                continue
            stats_file_path = os.path.join(stats_folder_path,x)
        return stats_file_path

    # Gets called when the stats file chages
    def stats_change(self):
        print("Stats file changed")
        with open(self.stats_file_path, 'r') as file:
            self.stats = json.load(file)['stats']

        data = self.get_important_item_counts()
        self.data_ready.emit(data)


    def get_important_item_counts(self):
        pearls = self.get_item_count_from_barters("ender_pearl")

        fireres = (
            self.get_item_count_from_barters("splash_potion") +
            self.get_item_count_from_barters("potion")
        )

        string_count = self.get_item_count_from_barters("string")
        wool = math.floor(string_count / 4) + self.get_item_count_from_barters("white_wool")

        colors = ["white","orange","magenta","light_blue","yellow","lime","pink","gray","light_gray","cyan","purple","blue","brown","green","red","black"]
        beds = 0
        for color in colors:
            beds += (
                self.get_item_crafted_amount(color+"_bed") +
                self.get_item_count_from_barters(color+"_bed")
            )

        glowstone = self.get_item_count_from_barters("glowstone_dust")

        tnt = self.get_item_count_from_barters("tnt")

        blaze_rods = self.get_item_count_from_barters("blaze_rod")

        blaze_killed = self.get_mob_killed_amount("blaze")

        eyes = (
            self.get_item_crafted_amount("ender_eye") +
            self.get_item_count_from_barters("ender_eye")
        )

        anchors = (
            self.get_item_crafted_amount("respawn_anchor") +
            self.get_item_count_from_barters("respawn_anchor")
        )
        bow = (
            self.get_item_crafted_amount("bow") +
            self.get_item_count_from_barters("bow")
        )

        deaths = self.get_death_amount()

        return {
            "items": {
                "pearls": pearls,
                "fireres": fireres,
                "string_e": string_count,
                "wool_e": wool,
                "beds": beds, # FORT: beds crafted/ tnt picked up - used - dropped|rates
                "glowstone_dust": glowstone,
                "tnt": tnt,
                "blaze_killed": blaze_killed,
                "blaze_rods": blaze_rods,
                "eyes": eyes,
                "anchors": anchors,
                "bow": bow
            },
            "deaths": deaths
            
        }


    def get_death_amount(self):
        if 'minecraft:custom' in self.stats:
            if "minecraft:deaths" in self.stats['minecraft:custom']:
                deaths = self.stats['minecraft:custom']["minecraft:deaths"]
            else:
                deaths = 0
        else:
            deaths = 0
        return deaths

    def get_mob_killed_amount(self,mob):
        if 'minecraft:killed' in self.stats:
            if "minecraft:"+mob in self.stats['minecraft:killed']:
                mob_killed = self.stats['minecraft:killed']["minecraft:"+mob]
            else:
                mob_killed = 0
        else:
            mob_killed = 0
        return mob_killed


    def get_item_crafted_amount(self,item):
        if 'minecraft:crafted' in self.stats:
            if "minecraft:"+item in self.stats['minecraft:crafted']:
                crafted = self.stats['minecraft:crafted']["minecraft:"+item]
            else:
                crafted = 0
        else:
            crafted = 0
        return crafted

    def get_item_picked_up_amount(self,item):
        if 'minecraft:picked_up' in self.stats:
            if "minecraft:"+item in self.stats['minecraft:picked_up']:
                picked_up = self.stats['minecraft:picked_up']["minecraft:"+item]
            else:
                picked_up = 0
        else:
            picked_up = 0 
        return picked_up

    # pearls, fireres, string, glowstone
    def get_item_count_from_barters(self,item):
        if 'minecraft:used' in self.stats:
            if "minecraft:"+item in self.stats['minecraft:used']:
                used = self.stats['minecraft:used']["minecraft:"+item]
            else:
                used = 0
        else:
            used = 0

        if 'minecraft:dropped' in self.stats:
            if "minecraft:"+item in self.stats['minecraft:dropped']:
                dropped = self.stats['minecraft:dropped']["minecraft:"+item]
            else:
                dropped = 0
        else:
            dropped = 0

        if 'minecraft:picked_up' in self.stats:
            if "minecraft:"+item in self.stats['minecraft:picked_up']:
                picked_up = self.stats['minecraft:picked_up']["minecraft:"+item]
            else:
                picked_up = 0
        else:
            picked_up = 0 
        total_amount = picked_up - dropped - used

        return total_amount

    @Slot()
    def stop(self):
        print("Stopping stats worker")
        #self.running = False
        if hasattr(self,"timer"):
            self.timer.stop()
    @Slot()
    def run(self):
        cur_world_path = self.latest_world_path

        self.stats_file_path = self.get_statistics_file(cur_world_path)

        self._last_mtime = os.path.getmtime(self.stats_file_path)

        self.timer = QTimer()
        self.timer.timeout.connect(self._poll_file)
        self.timer.start(100)
    
        print("Watching:",self.stats_file_path)

    def _poll_file(self):
        mtime = os.path.getmtime(self.stats_file_path)
        if mtime != self._last_mtime:
            self._last_mtime = mtime
            self.stats_change()

    @Slot(str)
    def latest_world_updated(self,new_world_path):
        print("Updated to new world path", new_world_path)
        self.latest_world_path = new_world_path
        cur_world_path = self.latest_world_path
        self.stats_file_path = self.get_statistics_file(cur_world_path)
        print("Watching:",self.stats_file_path)

