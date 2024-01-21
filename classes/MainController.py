import heapq

class MainController:
    '''
    Contains all the functions required
    '''
    def __init__(self):
        file = open("station_time.txt", "r")
        self.station_times = eval(file.readline())
        file = open("exit_data.txt", "r")
        self.exits = eval(file.readline())
        file = open("transfer_data.txt", "r")
        self.transfers = eval(file.readline())

    def convert(self, start_station, end_station):
        if start_station.startswith("DT"):
            if int(start_station[2:]) > int(end_station[2:]):
                return "DT1"
            return "DT35"
        if start_station.startswith("NE"):
            if int(start_station[2:]) > int(end_station[2:]):
                return "NE1"
            return "NE17"
        if start_station.startswith("EW") and end_station.startswith("EW"):
            if int(start_station[2:]) > int(end_station[2:]):
                return "EW1"
            return "EW33"
        if start_station.startswith("CG") and end_station.startswith("CG"):
            if int(start_station[2:]) > int(end_station[2:]):
                return "EW33"
            return "CG2"
        if end_station.startswith("CG"):
            return "CG2"
        if start_station.startswith("CG"):
            return "EW33"
        if start_station.startswith("CC") and end_station.startswith("CC"):
            if int(start_station[2:]) > int(end_station[2:]):
                return "CC1"
            return "CC29"
        if start_station.startswith("CE") and end_station.startswith("CE"):
            if int(start_station[2:]) > int(end_station[2:]):
                return "CC29"
            return "CE2"
        if end_station.startswith("CE"):
            return "CE2"
        if start_station.startswith("CE"):
            return "CC29"
        if start_station.startswith("TE"):
            if int(start_station[2:]) > int(end_station[2:]):
                return "TE1"
            return "TE22"
        if start_station.startswith("NS"):
            if int(start_station[2:]) > int(end_station[2:]):
                return "NS1"
            return "NS28"        
        print(start_station, end_station)
        return "oops unhandled error"
    
    def is_same_line(self, station_1, station_2):
        first = station_1[:2]
        second = station_2[:2]
        if first.startswith("P") and second.startswith("P"):
            return True
        if first.startswith("S") and second.startswith("S"):
            return True
        if first == "CE":
            first = "CC"
        if second == "CE":
            second = "CC"
        return first == second

    def get_line(self, station):
        if station.startswith("DT"):
            return "DTL"
        if station.startswith("NE"):
            return "NEL"
        if station.startswith("EW"):
            return "EWL"
        if station.startswith("CG"):
            return "CGL"
        if station.startswith("NS"):
            return "NSL"
        if station.startswith("CC") or station.startswith("CE"):
            return "CCL"
        if station.startswith("TE"):
            return "TEL"
        return station
    
    def get_path(self, json):
        path = self.path_finding(json["start"], json["end"])
        print(path)
        if not self.is_same_line(path[1][-1],path[1][-2]):
            del path[1][-1]
        if not self.is_same_line(path[1][0],path[1][1]):
            del path[1][0]
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
            for next_station in self.station_times[cur]:
                temp_dir = dir
                temp_data = data[:]
                if next_station[2] == 2 and temp_dir == -1:
                    next_station = (next_station[0], 0, next_station[2])
                if next_station[2] == 2:
                    temp_data.append(cur)
                    temp_dir = -1
                elif temp_dir == -1:
                    temp_data.append(cur)
                    temp_dir = next_station[2]
                elif temp_dir != next_station[2]:
                    temp_dir = next_station[2]
                heapq.heappush(queue, [time + next_station[1], next_station[0], temp_dir, temp_data])
        
        print(visited)
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
                try:
                    if i + 2 == len(path):
                        details = list(self.exits[path[i+1]][dir][exit])
                    else:
                        temp_dir = self.convert(path[i+2], path[i+3])
                        details = list(self.transfers[path[i+1]][temp_dir])
                except Exception as e:
                    print(temp_dir)
                    print("oop")
                    print(e)
                    details = ["Any door","Any door","Any door"]

                try:
                    if dir not in self.exits[path[i]]:
                        if dir == "CE2":
                            dir = "CC1"
                        elif dir == "CG2":
                            dir = "EW1"
                    instructions["details"] = "Platform " + self.exits[path[i]][dir]["Platform"]
                    instructions["towards"] = dir
                except Exception as e:
                    print(e, "as)")
                    instructions["details"] = "Platform"
                    instructions["towards"] = path[i+1]

                instructions["door"] = details
                stations[-1]["instructions"].append(instructions)
            else:
                need_new = False
                station = {}
                if path[i] == "CG0":
                    path[i] = "EW4"
                station["name"] = path[i]
                station["instructions"] = []
                stations.append(station)
                stations[-1]["instructions"].append({"type":"transfer", "description":self.get_line(path[i+1])})
        stations.append({"name":path[-1], "instructions":[]})
        return {"stations": stations}


