#!/usr/bin/python3
from musicbox import *
import timer as t
import random
import threading
import tkinter as tk

class MusicPlayer(tk.Frame):
    
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.playlist = None
        self.categories = None
        self.play = True
        self.loop = False
        self.running = False
        self.initalizeUI()

    def initalizeUI(self):
        self.parent.title("Musicbox")
        
        self.info = tk.Label(self.parent,text="Playlist name:")
        self.info.place(x=0,y=0)
        
        self.doPlaylist = tk.Button(self.parent,text="Shuffle Playlist",command=self.initPlaylist)
        self.doPlaylist.place(x=0,y=20)
        
        self.playlistEntry = tk.Entry(self.parent,width=20)
        self.playlistEntry.place(x=100,y=0)
        
        self.doShuffle = tk.Button(self.parent,text="Shuffle All",command=self.initShuffle)
        self.doShuffle.place(x=125,y=20)

    def initShuffle(self):
        allFolders = [i for i in list(os.walk('.'))[0][1] if getAllMusic(i)]
        self.playlist,self.categories = musicDict(allFolders),allFolders
        self.initalizeMusicbox()

    def initPlaylist(self):
        self.playlist = readList(self.playlistEntry.get())
        self.categories = list(self.playlist.keys())
        self.initalizeMusicbox()

    def initalizeMusicbox(self):
        self.info.destroy()
        self.doPlaylist.destroy()
        self.playlistEntry.destroy()
        self.doShuffle.destroy()

        self.currentPlaying = tk.Label(self.parent,text="")
        self.currentPlaying.place(x=0,y=0)

        def skip():
            self.play = False
        self.skip = tk.Button(self.parent,text="Skip",command=skip)
        self.skip.place(x=50,y=20)
        def toggle_loop():
            self.loop = not self.loop
        self.loop = tk.Button(self.parent,text="Loop",command=toggle_loop)
        self.loop.place(x=200,y=20)
        
        self.running = True
        self.shuffler = threading.Thread(target=self.shuffle)
        self.shuffler.start()

    def shuffle(self):
        while(self.running):
            category = random.choice(self.categories)
            song = random.choice(self.playlist[category])
            self.currentPlaying.config(text="{} from {}".format(re.sub(r"^.+/","",song)[:-4:],category))
            wave = simpleaudio.WaveObject.from_wave_file(song)
            self.player = wave.play()
            timer = t.Timer()
            self.play = True
            while(self.play):
                if(not self.player.is_playing()):
                    self.play = timer.elapsed() > 180 and (not self.loop)
                    if(self.play):
                        self.player = wave.play()
            self.player.stop()

    def cleanup(self):
        if(self.running):
            self.running = False
            self.play = False
            self.shuffler.join()
        quit()
        
if(__name__ == '__main__'):
    os.chdir('/'.join(__file__.split('/')[:-1:]))
    root = tk.Tk()
    root.geometry("300x50+500+500")
    icon = tk.PhotoImage(file='disk.gif')
    root.tk.call('wm','iconphoto',root._w,icon)
    app = MusicPlayer(root)
    root.protocol("WM_DELETE_WINDOW", app.cleanup)
    root.mainloop()
    
