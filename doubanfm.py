#!/usr/bin/python
# coding: utf-8

import httplib
import json
import os
import sys
import time
import select 
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')

class DoubanFM:
    def __init__(self):
        self.printHelp()

    def printHelp(self):
        helpInfo = u'''
Command List:
n Next Song
c Change Channel
e Exit
	'''
	print helpInfo

    def changeChannel(self):
        channelInfo = u'''
Channel List:
1 Chinese
2 English
61 New
	'''
	print channelInfo
	cID = raw_input('Please input channel ID:')
        self.channelID = cID

    def getSongList(self):
        httpConnection = httplib.HTTPConnection('douban.fm')
        httpConnection.request('GET','/j/mine/playlist?type=n&channel=' + self.channelID)
	self.songList = json.loads(httpConnection.getresponse().read())['song']

    def control(self):
        rlist,_,_ = select.select([sys.stdin], [], [])
        if rlist:
           s = sys.stdin.readline()
           return s[0]

    def start(self):
        self.changeChannel()
	self.getSongList()
        hasChangedChannel = False
        for song in self.songList:
            songURL = song['url']
            songTitle = song['title']
            songArtist = song['artist']
            songAlbum = song['albumtitle']
	    songLength = song['length']
            print 'Now playing: ' + songTitle + ' (' + songArtist + ')'
            self.player = subprocess.Popen(['mpg123',songURL],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	    starttime = time.time()
	    while True:
                ctl = self.control()
                endtime = time.time()
                elapsetime = endtime - starttime
                if ctl == 'n' or elapsetime > songLength:
		   self.player.kill()
                   break
		elif ctl == 'c':
		   hasChangedChannel = True
                   self.player.kill()
		   break
	        elif ctl == 'e':
		   self.player.kill()
                   sys.exit()
		else:
		   print 'Invalid command'
		   self.printHelp()
	    if hasChangedChannel:
               break
	self.start()

fm = DoubanFM()
fm.start()





