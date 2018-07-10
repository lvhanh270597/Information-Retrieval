
import pickle
import lib.vnTokenize.Dictionary as ws_dict
import lib.vnTagger.Dictionary as tag_dict
from lib.vnTokenize.Tokenizer import Tokenizer
from lib.vnTagger.TransformationBasedLearning import TransformationBasedLearning
from lib.environment.env import ENV

def parse(s):
    lower = s.lower()
    BOOL = {"false" : False, "true" : True}
    if lower in BOOL: return BOOL[lower]
    return s

def initEnvironment(pathEnv = "lib/environment/env.txt"):
    for line in open(pathEnv):
        key_val = line.split()
        if len(key_val) == 2:
            key, val = key_val
            ENV[key] = parse(val)
    ENV["ws_dict"] = ws_dict.Dictionary()
    ENV["tag_dict"] = tag_dict.Dictionary()
    ENV["tokenize"] = Tokenizer()

    ENV["tagger"] = TransformationBasedLearning()
    if not ENV["SAVED_MODEL_TAG"]:
        X = [line for line in open(ENV["TAG_DATA_PATH"])]
        ENV["tagger"].fit(X)
        ENV['SAVED_MODEL_TAG'] = True
        filename = ENV['TAG_MODEL_PATH']
        pickle.dump(ENV["tagger"], open(filename, 'wb'))

def saveEnvironment(pathEnv = "lib/environment/env.txt"):
    f = open(pathEnv, "w")
    for (key, value) in ENV.items():
        if key == key.upper():
            f.write(key + '\t' + str(value) + '\n')
    f.close()
    print("Saved environment successfully!")

