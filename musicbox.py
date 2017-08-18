#!/usr/bin/env python3
import shutil
import os
import re
import sys
import simpleaudio
import subprocess
import random
import getcher
import timer

def replace(part,replacement,folder):
    os.chdir(folder)
    regex = re.compile(part)
    for file in os.listdir():
        if(regex.search(file)):
            newName = regex.sub(replacement,file)
            print('Moving {} to {}!'.format(file,newName))
            shutil.move(file,newName)
 
def playFile(path):
    wObj = simpleaudio.WaveObject.from_wave_file(path)
    cont = True
    forever = False
    waiter = timer.Timer()
    while(cont):
        pObj = wObj.play()
        while(pObj.is_playing()):
            if(KB.kbhit()):
                press = KB.getch()
                if(press == 'q'):
                    quit()
                if(press == 's'):
                    cont = False
                    break
                if(press == 'l'):
                    forever = not forever
        pObj.stop()
        if(180 < waiter.elapsed() and not forever):
            cont = False
            
def convertToWav(path):
    subprocess.run(['ffmpeg','-i',path,re.sub(r'\.\w+$',r'.wav',path)])
    
def convertAllWav():
    for folder,subfolders,files in os.walk('.'):
        for file in files:
            if(file.endswith('mp3') or file.endswith('mkv') or file.endswith('.webm') or file.endswith('.mp4')):
                print('Converting {} to a .wav file...')
                convertToWav(os.path.join(folder,file))
                os.unlink(os.path.join(folder,file))
                
def getAllMusic(folder):
    ret = []
    os.chdir(folder)
    for file in os.listdir():
        if(file.endswith('.wav')):
            ret.append(os.path.join(folder,file))
    os.chdir('..')
    return(ret)

def musicDict(folders):
    ret = {}
    for folder in folders:
        ret[folder] = getAllMusic(folder)
    return(ret)

def flush():
    print("\r" + ' '*shutil.get_terminal_size().columns,end='')
    
def shuffle(musicDict,categories):
    while(True):
        choice = random.choice(categories)
        song = random.choice(musicDict[choice])
        flush()
        print("\rNow Playing: {} from {}".format(re.sub(r"^.+/","",song)[:-4:],choice),end='')
        playFile(song)
        
def get(url,folder):
    if(not os.path.exists(folder)):
        os.mkdir(folder)
    os.chdir(folder)
    subprocess.run(['youtube-dl',url])
    os.chdir('..')
    convertAllWav()

def readList(file):
    with open(file,'r') as f:
        lines = f.read().split('\n')[:-1:]
    lines = [i.split(':') for i in lines]
    lineDict = {}
    for folder,song in lines:
        song = os.path.join(folder,song + '.wav')
        if(folder in lineDict):
            lineDict[folder].append(song)
        else:
            lineDict[folder] = [song]
    return lineDict

def parseArgs():
    if(len(sys.argv) == 0):
        print("Please provide command line arguments. See {} for more"
              .format('/'.join(__file__.split('/')[:-1:]) + '/README.md'))
        return
    choice = sys.argv[1]
    if(choice == 'replace'):
        replace(sys.argv[2],sys.argv[3],sys.argv[4])
    elif(choice == 'convert'):
        convertAllWav()
    elif(choice == 'shuffle'):
        if(len(sys.argv) == 2):
            allFolders = [i for i in list(os.walk('.'))[0][1] if getAllMusic(i)]
        else:
            allFolders = sys.argv[2::]
        music = musicDict(allFolders)
        shuffle(music,allFolders)
    elif(choice == 'get'):
        get(sys.argv[2],sys.argv[3])
    elif(choice == 'list'):
        lineDict = readList(sys.argv[2])
        shuffle(lineDict,list(lineDict.keys()))
    else:
        print("Mode \"{}\" is not recognized.".format(choice))

if(__name__=='__main__'):
    try:
        if("python" in sys.argv[0]):
            sys.argv = sys.argv[1::]
        os.chdir('/'.join(__file__.split('/')[:-1:]))
        KB = getcher.KBHit()
        parseArgs()
    finally:
        KB.set_normal_term()
