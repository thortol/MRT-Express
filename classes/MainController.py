import heapq

class MainController:
    '''
    Contains all the functions required
    '''
    def __init__(self):
        file = open("station_time.txt", "r")
        self.station_times = eval(file.readline())
        self.exits = {
            "DT13" : {
                "DT35": {
                    "Platform": "A",
                    "A": ("8","5","10"),
                    "B": ("9","5","10")
                },
                "DT1": {
                    "Platform": "B",
                    "A": ("5","8","3"),
                    "B": ("6","8","3")
                }
            },
            "DT1" : {
                "DT35": {
                    "Platform": "A",
                    "A": ("8","5","10"),
                    "B": ("9","5","10")
                },
                "DT1": {
                    "Platform": "B",
                    "A": ("5","8","3"),
                    "B": ("6","8","3")
                }
            },
            "NE7": {
                "NE1": {
                    "Platform": "A",
                    "A": ("8","5","10"),
                    "B": ("8","5","10")
                },
                "NE17": {
                    "Platform": "B",
                    "A": ("5","8","3"),
                    "B": ("5","8","3")
                }
            }
        }
        self.transfers = {
            "CC10": {
                "DT1": ("1","1","1"),
                "DT35": ("12", "12", "12")
            },
            "NE7": {
                "DT1": ("1","1","1"),
                "DT35": ("12", "12", "12")
            }
        }
    
    def convert(self, start_station, end_station):
        if start_station.startswith("DT"):
            if int(start_station[2:]) > int(end_station[2:]):
                return "DT1"
            return "DT35"
        if start_station.startswith("NE"):
            if int(start_station[2:]) > int(end_station[2:]):
                return "NE1"
            return "NE17"
    
    def is_same_line(self, station_1, station_2):
        return station_1[:2] == station_2[:2]

    def get_line(self, station):
        if station.startswith("DT"):
            return "downtown line"
        if station.startswith("NE"):
            return "northeast line"
        return "A line"
    
    def get_path(self, json):
        path = self.path_finding(json["start"], json["end"])
        if not self.is_same_line(path[1][-1],path[1][-2]):
            del path[1][-1]
        json = self.convert_path_to_format(path[1], json["exit"])
        json["time"] = path[0]
        return json
    
    def path_finding(self, start, end):
        queue = [(0, start, -1, [])]
        visited = set()
        while queue != []:
            time, cur, dir, data = heapq.heappop(queue)
            if cur in visited:
                continue
            visited.add(cur)
            if cur == end:
                data.append(end)
                return time, data
            for next_station in self.station_times.get(cur, []):
                temp_dir = dir
                temp_data = data[:]
                if temp_dir == -1:
                    temp_data.append(cur)
                    temp_dir = next_station[2]
                elif next_station[2] == 2:
                    temp_data.append(cur)
                    temp_dir = -1
                elif temp_dir != next_station[2]:
                    continue
                heapq.heappush(queue, [time + next_station[1], next_station[0], temp_dir, temp_data])
        return "error no path found"

    def convert_path_to_format(self, path, exit):
        stations = []
        need_new = True
        for i in range(len(path)-1):
            if self.is_same_line(path[i],path[i+1]):
                dir = self.convert(path[i], path[i+1])
                station = {}
                station["name"] = path[i]
                station["instructions"] = []
                if need_new:
                    stations.append(station)
                need_new = True
                instructions = {}
                instructions["type"] = "board"
                instructions["station"] = path[i]
                if i + 2 == len(path):
                    details = str(self.exits[path[i+1]][dir][exit])
                else:
                    temp_dir = self.convert(path[i+2], path[i+3])
                    details = str(self.transfers[path[i+1]][temp_dir])
                instructions["details"] = "Platform " + self.exits[path[i+1]][dir]["Platform"] + ", Door " + details
                instructions["towards"] = dir
                stations[-1]["instructions"].append(instructions)
            else:
                need_new = False
                station = {}
                station["name"] = path[i]
                station["instructions"] = []
                stations.append(station)
                stations[-1]["instructions"].append({"type":"transfer", "description":"transfer to " + self.get_line(path[i+1])})
        stations.append({"name":path[-1], "instructions":[]})
        return {"stations": stations}


