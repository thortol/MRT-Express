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

    def get_path(self, json):
        path = self.path_finding(json["start"], json["end"])
        print(path)
        return self.convert_path_to_format(path[1], json["exit"])
    
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
            if path[i][:2] == path[i+1][:2]:
                if need_new:
                    stations.append([])
                need_new = True
                dir = self.convert(path[i], path[i+1])
                station = {}
                station["name"] = path[i]
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
                stations[-1].append(instructions)
            else:
                need_new = False
                stations.append([])
                stations[-1].append({"type":"transfer", "description":"transfer to new line"})
        return {"stations": stations}


