file = open("data.csv", "r")
total = ""
for line in file:
    total += line
rows = total.split("\n`,")
exits = {}
transfers = {}
for row in rows:
    name, dir, towards, doors, transfer = row.split(",")
    platform, end = towards.split("/")
    if name not in exits:
        exits[name] = {}
    # if end in exits[name]:
    #     print("oop")
    exits[name][end] = {"Platform":platform}
    doors = doors[1:-1].split("\n")
    for door in doors:
        exit_val, esc, lift, stairs = door.split("/")
        exits[name][end][exit_val] = (esc, lift, stairs)
    if transfer != "":
        if name not in transfers:
            transfers[name] = {}
        if "\n" in transfer:
            temp = transfer[1:-1].split("\n")
            for transfer in temp:
                transfer = transfer.split("/")
                if len(transfer) == 5:
                    line, a, b, c, out = transfer
                    if "?" in out:
                        dir1, dir2 = out.split("?")
                        transfers[name][dir1] = (a,b,c)
                        transfers[name][dir2] = (a,b,c)
                    else:
                        transfers[name][out] = (a,b,c)
                else:
                    line, a, b, c = transfer
                    if line.startswith("CC"):
                        dir1, dir2 = "CC1", "CC29"
                    elif line.startswith("DT"):
                        dir1, dir2 = "DT1", "DT35"
                    elif line.startswith("NS"):
                        dir1, dir2 = "NS1", "NS28"
                    elif line.startswith("EW"):
                        dir1, dir2 = "EW1", "EW33"
                    elif line.startswith("TE"):
                        dir1, dir2 = "TE1", "TE22"
                    elif line.startswith("NE"):
                        dir1, dir2 = "NE1", "NE17"
                    else:
                        dir1, dir2 = line, line
                    transfers[name][dir1] = (a,b,c)
                    transfers[name][dir2] = (a,b,c)

        else:
            transfer = transfer.split("/")
            if len(transfer) == 5:
                line, a, b, c, out = transfer
                if "?" in out:
                    dir1, dir2 = out.split("?")
                    transfers[name][dir1] = (a,b,c)
                    transfers[name][dir2] = (a,b,c)
                else:
                    transfers[name][out] = (a,b,c)
            else:
                line, a, b, c = transfer
                if line.startswith("CC"):
                    dir1, dir2 = "CC1", "CC29"
                elif line.startswith("DT"):
                    dir1, dir2 = "DT1", "DT35"
                elif line.startswith("NS"):
                    dir1, dir2 = "NS1", "NS28"
                elif line.startswith("EW"):
                    dir1, dir2 = "EW1", "EW33"
                elif line.startswith("TE"):
                    dir1, dir2 = "TE1", "TE22"
                elif line.startswith("NE"):
                    dir1, dir2 = "NE1", "NE17"
                else:
                    dir1, dir2 = line, line
                transfers[name][dir1] = (a,b,c)
                transfers[name][dir2] = (a,b,c)

file = open("exit_data.txt", "w")
file.write(str(exits))
file.close()
print(exits)