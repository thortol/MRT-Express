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
        if end_station.startswith("CE"):
            return "CE2"
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
        if first == "CG":
            first = "EW"
        if second == "CG":
            second = "EW"
        if first == "CE":
            first = "CC"
        if second == "CE":
            second = "CC"
        return first == second

    def get_line(self, station):
        if station.startswith("DT"):
            return "downtown line"
        if station.startswith("NE"):
            return "northeast line"
        if station.startswith("EW") or station.startswith("CG"):
            return "eastwest line"
        if station.startswith("NS"):
            return "northsouth line"
        if station.startswith("CC") or station.startswith("CC"):
            return "circle line"
        if station.startswith("TE"):
            return "thomson east coast line"
        return "A line"
    
    def get_path(self, json):
        path = self.path_finding(json["start"], json["end"])
        if not self.is_same_line(path[1][-1],path[1][-2]):
            del path[1][-1]
        if not self.is_same_line(path[1][0],path[1][1]):
            del path[1][0]
        print(path)
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
                if next_station[2] == 2 and temp_dir == -1:
                    next_station = (next_station[0], 0, next_station[2])
                if next_station[2] == 2:
                    temp_data.append(cur)
                    temp_dir = -1
                elif temp_dir == -1:
                    temp_data.append(cur)
                    temp_dir = next_station[2]
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
                if dir not in self.exits[path[i]]:
                    if dir == "CE2":
                        dir = "CC1"
                    elif dir == "CG2":
                        dir = "EW1"
                instructions["details"] = "Platform " + self.exits[path[i]][dir]["Platform"] + ", Door " + details
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


