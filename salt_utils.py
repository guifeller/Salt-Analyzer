# Various utilities and tools

import json

def openF(file):
    with open(file, "r") as jsonfile:
        data = jsonfile.read()
        jdata = json.loads(data)
        return jdata
    print("The command file cannot be localized")