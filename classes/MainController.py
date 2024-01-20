import heapq

class MainController:
    '''
    Contains all the functions required
    '''
    def __init__(self):
        file = open("station_time.txt", "r")
        self.station_times = eval(file.readline())
        self.exits = {
            "DT27" : {
                "DT35": {
                    "Platform": "A",
                    "A": (8,5,10),
                    "B": (8,5,10)
                },
                "DT1": {
                    "Platform": "B",
                    "A": (5,8,3),
                    "B": (5,8,3)
                }
            }
        }
    
    def convert(self, station, code):
        if station.startswith("DT"):
            return ["DT1", "DT35"][code]

    
    def get_path(self, json):
        path = self.path_finding(json["start"], json["end"])
    
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
                    print(cur)
                    temp_data.append(cur)
                    temp_dir = -1
                elif temp_dir != next_station[2]:
                    continue
                heapq.heappush(queue, [time + next_station[1], next_station[0], temp_dir, temp_data])
        return "error no path found"

    def convert_path_to_format(self, path):
        pass
