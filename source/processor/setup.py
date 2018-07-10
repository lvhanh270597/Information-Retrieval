
from environment.env import ENV

def parse(s):
    lower = s.lower()
    BOOL = {"false" : False, "true" : True}
    if lower in BOOL: return BOOL[lower]
    return s

def initEnvironment(pathEnv = "environment/env.txt"):
    for line in open(pathEnv):
        key_val = line.split()
        if len(key_val) == 2:
            key, val = key_val
            ENV[key] = parse(val)

def saveEnvironment(pathEnv = "environment/env.txt"):
    f = open(pathEnv, "w")
    for (key, value) in ENV.items():
        if key == key.upper():
            f.write(key + '\t' + str(value) + '\n')
    f.close()
    print("Saved environment successfully!")

