#!/usr/bin/python3
import os,json

result = {}
categories = os.listdir('Static/music')
for i in categories:
    result[i] = list(map(lambda i:i[:-4:],os.listdir('Static/music/' + i)))

with open('Static/allsongs.js','w') as f:
    f.truncate()
    f.write('var songs =' + json.dumps(result) + ';')
