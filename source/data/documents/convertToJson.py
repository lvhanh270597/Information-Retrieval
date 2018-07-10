
from os import listdir
import json

for fname in listdir('raw'):
    f = open('raw/' + fname)
    lines = f.readlines()
    title, link = lines[:2]
    content = '\n'.join(lines[2:])

    doc = {'title' : title, 'link' : link, 'content' : content}
    with open('json/' + fname + '.json', 'w') as outfile:
        json.dump(doc, outfile, ensure_ascii=False)
