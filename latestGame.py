# https://github.com/bloxstraplabs/bloxstrap/blob/main/Bloxstrap/Integrations/ActivityWatcher.cs
#https://github.com/bloxstraplabs/bloxstrap/wiki/A-deep-dive-on-how-the-Roblox-bootstrapper-works#starting-roblox
import re
import os

GameJoiningEntry = "[FLog::Output] ! Joining game"
GameJoiningEntryPattern = r"! Joining game '([0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12})' place (\d+)"

if os.getuid() != 0:
    print("Root required")
    exit()

robloxLogs = "/data/data/com.roblox.client/files/appData/logs"
logsList = sorted([os.path.join(robloxLogs, i) for i in os.listdir(robloxLogs)], key = os.path.getmtime, reverse = True)

if len(logsList) == 0:
    print("No logs inside folder")
    exit()

with open(logsList[0], "r") as f:
    for lineEntry in f.readlines():
        if GameJoiningEntry in lineEntry:
            regexMatch = re.search(GameJoiningEntryPattern, lineEntry)
            placeId = regexMatch.group(2)
            jobId = regexMatch.group(1)

intentLink = f"roblox://experiences/start?placeId={placeId}&gameInstanceId={jobId}"
print(f"Latest Game:\nPlace ID: {placeId}\nJob ID: {jobId}\nIntent Link: {intentLink}")
os.system(f"/system/bin/am start -a android.intent.action.VIEW -d '{intentLink}'")
