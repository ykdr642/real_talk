#!python3.6
import subprocess as sps
import pyaudio
import wave
import numpy as np
from datetime import datetime
import speech_recognition as sr
import os
import time
import threading
import math
import cv2
import numpy as np
from PIL import ImageGrab
from PIL import Image
from PIL import Image, ImageDraw, ImageFont
import pygame
import random
import pyautogui
import keyboard
import csv
import discord
import asyncio
import pyDes
import sys
import wx
os.chdir("../")
pygame.init()
clock = pygame.time.Clock()

class lagTimer:

    def __init__(self,time):
        self.lag = int(time)
    
    def changeLag(self,time):
        self.lag = int(time)
    
    def getLagTime(self):
        lag = self.lag
        if int(datetime.today().strftime('%S')) >= lag:
            timedata = datetime.today().strftime("%m%d%H%M") + str(int(datetime.today().strftime('%S')) - lag).zfill(2)
        elif int(datetime.today().strftime('%M')) == 0:
            timedata = datetime.today().strftime("%m%d%H") + str(59) + str(int(datetime.today().strftime('%S')) + (60-lag)).zfill(2)
        elif int(datetime.today().strftime('%M')) > 0:
            timedata = datetime.today().strftime("%m%d%H") + str(int(datetime.today().strftime('%M')) - 1).zfill(2)  + str(int(datetime.today().strftime('%S')) + (60-lag)).zfill(2)
        elif int(datetime.today().strftime('%H')) == 0:
            timedata = datetime.today().strftime("%m%d") + str(23) + str(59) + str(int(datetime.today().strftime('%S')) + (60-lag)).zfill(2)
        elif int(datetime.today().strftime('%H')) > 0:
            timedata = datetime.today().strftime("%m%d") + str(int(datetime.today().strftime('%H')) - 1).zfill(2)  + str(int(datetime.today().strftime('%M')) - 1).zfill(2)  + str(int(datetime.today().strftime('%S')) + (60-lag)).zfill(2)
        else:
            timedata = datetime.today().strftime("%m") + str(int(datetime.today().strftime('%d')) - 1).zfill(2)  + str(int(datetime.today().strftime('%H')) - 1).zfill(2)  + str(int(datetime.today().strftime('%M')) - 1)  + str(int(datetime.today().strftime('%S')) + (60-lag)).zfill(2)
        return timedata + str(int(int(datetime.today().strftime("%f"))/100000))

class cmdmaker:
    
    shot = False
    cmdmaker_threading_OFF_flag = False
    
    def __init__(self,washa,washaName):
        self.cv = washa
        self.washaName = washaName
        self.tasklist = []
        self.speeknow = 0
        self.innerclock = pygame.time.Clock()
        self.cmd = 'seikasay.exe この音声が流れることはないよ'
        self.coment = 'デフォルトです'
        self.frame = 30
        self.mabataki = 4
        self.kutipaku = 4
        self.vanish = False
        self.faceconfig = 0
        self.Red = 0
        self.Green = 0
        self.Blue = 0
        self.text = ""
        self.changeText = False
        self.textTime = 0
        self.LagTimer = lagTimer(10)
        self.RunNow = False
        self.JimakuNow = False
        self.TachieNow = False
        self.stop_Talk = True
        self.short_ID = str(self.cv)[:2]
        self.chouseiConfig = []
        if os.path.isdir('./voiceConfig'):
            if os.path.exists("voiceConfig/" + self.washaName + ".csv"):
                self.chouseiConfig = getcsv("voiceConfig/" + self.washaName + ".csv")
                self.chouseiConfig.pop(0)

        
    def makecmd(self):
        chousei_is_success = False
        for chousei in self.chouseiConfig:
            if str(self.tasklist[0][2]) == chousei[0]:
                if len(chousei) == 4:
                    self.cmd = 'seikasay.exe -cid ' + self.cv + ' -speed ' + chousei[1] + ' -pitch ' + chousei[2] + ' -intonation ' + chousei[3] + " -t " + ' \"' +self.tasklist[0][1] + '\"'
                    chousei_is_success = True
                    break
                elif len(chousei) == 7:
                    self.cmd = 'seikasay.exe -cid ' + self.cv + ' -speed ' + chousei[1] + ' -pitch ' + chousei[2] + ' -intonation ' + chousei[3] + ' -happiness ' + chousei[4] + ' -hatred ' + chousei[5] + ' -sadness ' + chousei[6] + " -t " + ' \"' + self.tasklist[0][1]+ '\"'
                    chousei_is_success = True
                    break                    
        if not chousei_is_success:
            self.cmd = 'seikasay.exe -cid ' + self.cv + " -t " + ' \"' + self.tasklist[0][1] + '\"'
        
        
    def changeLagTime(self,time):
        self.LagTimer.changeLag(time)
    
    def getTaskList(self,tlist):
        time = 0
        face = 0
        time,face = tlist[0].split("-")
        tlist[0] = time
        tlist.append(int(face))
        self.tasklist.append(tlist)
        
    
    def runVoiceRoid(self):
        if len(self.tasklist) > 0:
            times = int(self.LagTimer.getLagTime().lstrip('0'))
            if int(self.tasklist[0][0].lstrip('0')) < times:
                self.makecmd()
                self.textTime = 0
                self.text = self.tasklist[0][1]
                self.changeText = True
                self.faceconfig = self.tasklist[0][2]
                self.tasklist.pop(0)
                if not self.stop_Talk:
                    for hoge in manager.get_store_list:
                        if hoge[0] == self.short_ID:
                            hoge[1].append(self.washaName)
                        while True:
                            if self.stop_Talk:
                                break
                            time.sleep(1)
                for vlist in manager.VoiceRoidList:
                    if vlist.short_ID == self.short_ID:
                        vlist.stop_Talk = False
            
                if cmdmaker.shot and not self.cv == "NoVoice" and dis.discord_run_now:
                    sendname = self.washaName
                    if len(manager.changeNameList) > 0:
                        for cname in manager.changeNameList:
                            if cname[1] == sendname:
                                sendname = cname[0]
                                break
                    dis.sendlist.append(["shot",datetime.today().strftime("%m%d%H%M%S") + str(int(int(datetime.today().strftime("%f"))/100000)) + "-" + str(sendname),"up"])
                self.speeknow +=1
                if self.cv == "NoVoice":
                    time.sleep(1)
                else:
                    sps.call(self.cmd,shell=True,timeout = 15)
                self.speeknow -=1
                if cmdmaker.shot and not self.cv == "NoVoice" and dis.discord_run_now:
                    sendname = self.washaName
                    if len(manager.changeNameList) > 0:
                        for cname in manager.changeNameList:
                            if cname[1] == sendname:
                                sendname = cname[0]
                                break
                    dis.sendlist.append(["shot", datetime.today().strftime("%m%d%H%M%S") + str(int(int(datetime.today().strftime("%f"))/100000)) + "-" + str(sendname),"down"]) 
                for huga in manager.get_store_list:
                    if str(huga[0]) == str(self.short_ID):
                        if len(huga[1]) > 0:
                            for vlist in manager.VoiceRoidList:
                                if vlist.washaName == huga[1][0]:
                                    vlist.stop_Talk = True
                                    huga[1].pop(0)
                                    break
                        else:
                            for vlist in manager.VoiceRoidList:
                                if vlist.short_ID == self.short_ID:
                                    vlist.stop_Talk = True
                            break
                self.textTime = 1
    
    def loopRun(self):
        while True:
            self.runVoiceRoid()
            self.innerclock.tick(6)
            if cmdmaker.cmdmaker_threading_OFF_flag:
                break
            
    def startRunRoidThreading(self):
        startRunRoid = threading.Thread(target = self.loopRun)
        startRunRoid.start()
        


    def DrawMyChar(self):
        cv2.namedWindow(self.washaName)
        body = []
        eye = []
        anime_wait = []
        anime_talk = []
        im = Image.new('RGB', (1980, 1080), (0, 255, 0))
        im = np.asarray(im)
        im = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
        haikei = im
        if os.path.isdir("./data"):
            datafiles = os.listdir("data/" + self.washaName + "/")
            faceMax = len(datafiles)
        
            for datafile in datafiles:
                bdls = []
                eyels = []
                anils_wait = []
                anils_talk = []
                if os.path.isdir("data/" + self.washaName + "/" + datafile + "/body"):
                    files = os.listdir("data/" + self.washaName + "/" + datafile + "/body/")
                    if len(files) > 0:
                        for file in files:
                            if ".png" in file:
                                mp = cv2.imread("data/" + self.washaName + "/" + datafile + "/body/" + file,-1)
                                mp = cv2.resize(mp,(int(mp.shape[1]*750/mp.shape[0]),750))
                                bdls.append(mp)
                        body.append(bdls)
                    else:
                        body.append([])
                    
                if os.path.isdir("data/" + self.washaName + "/" + datafile + "/eye"):
                    files = os.listdir("data/" + self.washaName + "/" + datafile + "/eye/")
                    if len(files) > 0:
                        for file in files:
                            if ".png" in file:
                                ep = cv2.imread("data/" + self.washaName + "/" + datafile + "/eye/" + file,-1)
                                ep = cv2.resize(ep,(int(ep.shape[1]*750/ep.shape[0]),750))
                                eyels.append(ep)
                        eye.append(eyels)
                    else:
                        eye.append([])
                    
                if os.path.isdir("data/" + self.washaName + "/" + datafile + "/animation_wait"):
                    files = os.listdir("data/" + self.washaName + "/" + datafile + "/animation_wait/")
                    if len(files) > 0:
                        for file in files:
                            if ".png" in file:
                                ap = cv2.imread("data/" + self.washaName + "/" + datafile + "/animation_wait/" + file,-1)
                                ap = cv2.resize(ap,(int(ap.shape[1]*750/ap.shape[0]),750))
                                anils_wait.append(ap)
                        anime_wait.append(anils_wait)
                    else:
                        anime_wait.append([])

                if os.path.isdir("data/" + self.washaName + "/" + datafile + "/animation_talk"):
                    files = os.listdir("data/" + self.washaName + "/" + datafile + "/animation_talk/")
                    if len(files) > 0:
                        for file in files:
                            if ".png" in file:
                                ap = cv2.imread("data/" + self.washaName + "/" + datafile + "/animation_talk/" + file,-1)
                                ap = cv2.resize(ap,(int(ap.shape[1]*750/ap.shape[0]),750))
                                anils_talk.append(ap)
                        anime_talk.append(anils_talk)                
                    else:
                        anime_talk.append([])
                
            animeclock = pygame.time.Clock()
            timer = 0
            eyetime = 0
            eyestart = False
            eyescene = 0
            speekNow = True
            vanishtimer = 0
            face = 0
            bodynum = 0
            eyenum = 0
            animationNumber = 0
            face_Memory = 0
            bodynum_Memory = 0
            eyenum_Memory = 0
            animationNumber_Memory = 0

        #初期化
            drawmatrix = haikei.copy()
            if len(eye[face]) > 0:
                maskE = eye[face][0][:,:,3].copy()
                ret,maskE = cv2.threshold(maskE, 1, 1, cv2.THRESH_BINARY)
                maskE = cv2.cvtColor(maskE, cv2.COLOR_GRAY2BGR)
            if len(body[face]) > 0:
                maskB = body[face][0][:,:,3].copy()
                ret,maskB = cv2.threshold(maskB, 1, 1, cv2.THRESH_BINARY)
                maskB = cv2.cvtColor(maskB, cv2.COLOR_GRAY2BGR)
            if len(anime_wait[face]) > 0:
                maskA = anime_wait[face][0][:,:,3].copy()
                ret,maskA = cv2.threshold(maskA, 1, 1, cv2.THRESH_BINARY)
                maskA = cv2.cvtColor(maskA, cv2.COLOR_GRAY2BGR)
        
        
            while True:
                needchange = False
                        
                if speekNow and self.speeknow == 0:#話終わり
                    vanishtimer = 1
                    bodynum = 0
                    speekNow = False
            
                if not speekNow and self.speeknow > 0: #話はじめ
                    vanishtimer = 0
                    animationNumber = 0
                    speekNow = True
                    if self.faceconfig < faceMax:
                        face = self.faceconfig
                    else:
                        face = 0
                    eyenum = 0
                    bodynum = 0

                    
                    
                if face is not self.faceconfig:               
                    face = self.faceconfig                    
                    
                    
                    

        
                if speekNow:
                    vanishtimer = 0
                    if len(body[face]) > 0:        #bodyがあれば
                        if timer % self.kutipaku == 0:
                            needchange = True
                            if len(body[face]) > 2:
                                bodynum += random.randrange(len(body[face])-2)+ 1
                                if bodynum >= len(body[face]):
                                    bodynum -= len(body[face])-1
                            elif len(body[face]) == 2:
                                bodynum = 1
                            else:
                                bodynum = 0

                
                    if len(anime_talk[face]) > 0:
                        animationNumber += 1
                        if animationNumber >= len(anime_talk[face]):
                            animationNumber = 0


        
                elif vanishtimer < 150:
            
                    if len(anime_wait[face]) > 0:
                        animationNumber += 1
                        if animationNumber >= len(anime_wait[face]):
                            animationNumber = 0                 



            
                    if self.vanish and vanishtimer > 0 and vanishtimer < 150:
                        vanishtimer += 1
        
        
                
        
        
                if len(eye[face]) > 0:   #eyeがあればここは、speeknowと非同期
                    eyetime += 1
                    if eyetime > self.mabataki * self.frame and random.randrange(3) == 0:
                        eyetime = 0
                        if len(eye[face]) > 1:
                            eyestart = True
                    if eyestart:
                        needchange = True
                        eyescene += 1
                        eyenum = len(eye[face]) - 1 - abs(len(eye[face]) - 1 - eyescene)
                        if int(eyenum) == -1:
                            eyenum = 0
                            eyescene = 0
                            eyestart = False
                        
                    if len(eye[face]) - 1 < eyenum:
                        eyenum = 0
                        eyescene = 0
                        eyestart = False






                if not bodynum == bodynum_Memory:
                    needchange = True
                    bodynum_Memory = bodynum



                if not eyenum == eyenum_Memory:
                    needchange = True
                    eyenum_Memory = eyenum


                if not face == face_Memory:
                    needchange = True
                    face_Memory = face


                if not animationNumber == animationNumber_Memory:
                    needchange = True
                    animationNumber_Memory = animationNumber





                if needchange and vanishtimer < 150:
                    drawmatrix = haikei.copy()


                    if len(eye[face]) > 0:
                        maskE = eye[face][eyenum][:,:,3].copy()
                        ret,maskE = cv2.threshold(maskE, 1, 1, cv2.THRESH_BINARY)
                        maskE = cv2.cvtColor(maskE, cv2.COLOR_GRAY2BGR)
                        
                    if len(body[face]) > 0:
                        maskB = body[face][bodynum][:,:,3].copy()
                        ret,maskB = cv2.threshold(maskB, 1, 1, cv2.THRESH_BINARY)
                        maskB = cv2.cvtColor(maskB, cv2.COLOR_GRAY2BGR)
                
                    if len(anime_talk[face]) > 0 and speekNow:
                        maskA = body[face][bodynum][:,:,3].copy()
                        ret,maskA = cv2.threshold(maskA, 1, 1, cv2.THRESH_BINARY)
                        maskA = cv2.cvtColor(maskA, cv2.COLOR_GRAY2BGR)

                    if len(anime_wait[face]) > 0 and not speekNow:
                        maskA = body[face][bodynum][:,:,3].copy()
                        ret,maskA = cv2.threshold(maskA, 1, 1, cv2.THRESH_BINARY)
                        maskA = cv2.cvtColor(maskB, cv2.COLOR_GRAY2BGR)


                    if len(body[face]) > 0:
                        drawmatrix = cv2.resize(drawmatrix,(body[face][bodynum].shape[1],body[face][bodynum].shape[0]))
                        drawmatrix *= 1 - maskB
                        drawmatrix += body[face][bodynum][:,:,:3] * maskB


                    if len(eye[face]) > 0:
                        drawmatrix = cv2.resize(drawmatrix,(eye[face][eyenum].shape[1],eye[face][eyenum].shape[0]))
                        drawmatrix *= 1 - maskE
                        drawmatrix += eye[face][eyenum][:,:,:3] * maskE

                    if len(anime_talk[face]) > 0 and speekNow:
                        drawmatrix = cv2.resize(drawmatrix,(anime_talk[face][animationNumber].shape[1],anime_talk[face][animationNumber].shape[0]))
                        drawmatrix *= 1 - maskA
                        drawmatrix += anime_talk[face][animationNumber][:,:,:3] * maskA


                    if len(anime_wait[face]) > 0 and not speekNow:
                        drawmatrix = cv2.resize(drawmatrix,(anime_wait[face][animationNumber].shape[1],anime_wait[face][animationNumber].shape[0]))
                        drawmatrix *= 1 - maskA
                        drawmatrix += anime_wait[face][animationNumber][:,:,:3] * maskA

                    if len(body[face]) == 0 and len(eye[face]) == 0 and len(anime_talk[face]) == 0 and len(anime_wait[face]) == 0:
                        drawmatrix = cv2.resize(drawmatrix,(450,750))

                    
            
                if vanishtimer == 150:
                    drawmatrix = haikei.copy()
                    drawmatrix = cv2.resize(drawmatrix,(450,750))
                    vanishtimer = 151
            
            
                cv2.imshow(self.washaName,drawmatrix)
                cv2.waitKey(1)  
                
                
                timer += 1
                if timer == 60:
                    timer = 0
                if cmdmaker.cmdmaker_threading_OFF_flag:
                    break
                animeclock.tick(self.frame)
            
            
    def startChar(self):
        self.TachieEnd = False
        if os.path.isdir("./data"):
            if os.path.isdir("data/" + self.washaName):
                Tachie = threading.Thread(target = self.DrawMyChar)
                Tachie.start()
                self.TachieNow = True
        
        
        
    def WriteJimaku(self):
        cv2.namedWindow(self.washaName + "Jimaku")
        im = Image.new('RGB', (1980, 100), (0, 255, 0))
        textbox = im.copy()
        textbox = np.asarray(textbox)
        textbox = cv2.cvtColor(textbox,cv2.COLOR_BGR2RGB)
        Jimakuclock = pygame.time.Clock()
        while True:
            if self.changeText:
                self.changeText = False
                textbox = im.copy()
                draw = ImageDraw.Draw(textbox)
                font_size = 48
                while True:
                    draw.font = ImageFont.truetype("C:\Windows\Fonts\HGRPP1.ttc",font_size)
                    img_size = np.array(textbox.size)
                    txt_size = np.array(draw.font.getsize(self.text))
                    if img_size[0] > txt_size[0]:
                        break
                    font_size -= 2
        
                pos = (img_size - txt_size) / 2
                draw.text(pos, self.text, fill=(self.Red, self.Green, self.Blue))
                textbox = np.asarray(textbox)
                textbox = cv2.cvtColor(textbox,cv2.COLOR_BGR2RGB)
                
                
            if self.textTime == 300:
                self.textTime = 0
                textbox = im.copy()
                textbox = np.asarray(textbox)
                textbox = cv2.cvtColor(textbox,cv2.COLOR_BGR2RGB)
                
            if self.textTime > 0:
                self.textTime += 1
            cv2.imshow(self.washaName + "Jimaku",textbox)
            cv2.waitKey(1)
            if cmdmaker.cmdmaker_threading_OFF_flag:
                break
            Jimakuclock.tick(self.frame)
            
    def startJimaku(self):
        t1 = threading.Thread(target = self.WriteJimaku)
        t1.start()
        self.JimakuNow = True

class voiceRoidManager():
    
    voiceRoidManager_threading_OFF_flag = False
    
    def __init__(self):
        self.VoiceRoidList = []
        os.makedirs('OutputWav', exist_ok=True)
        self.checkdir = 'OutputWav/'
        self.tasklist = []
        self.changeNameList = []
        self.changeName = True
        self.changeWord = True
        self.replaceList = []
        self.rewriteList = []
        self.JimakuList = []
        self.R = 255
        self.G = 255
        self.B = 255
        self.changeColor = False
        self.times = 10
        self.get_store_list = []

        
    def getTaskList(self):
        while True:
            try:
                files = os.listdir(self.checkdir)
                for file in files:
                    r = sr.Recognizer()
                    with sr.AudioFile(self.checkdir+file) as source:
                        audio = r.record(source)
                    os.remove(self.checkdir+file)
                    try:
                        self.tasklist.append(["talk",file.replace('.wav',''),r.recognize_google(audio, language='ja-JP')])
                        if dis.discord_run_now:
                            dis.sendlist.append(["talk",file.replace('.wav',''),r.recognize_google(audio, language='ja-JP')]) 
                    except:
                        pass
            except:
                pass
            if voiceRoidManager.voiceRoidManager_threading_OFF_flag:
                break
            time.sleep(1)
    
    
    def appendVoiceRoid(self,cvID,washaName):
        self.VoiceRoidList.append(cmdmaker(cvID,washaName))
        save_ID = str(cvID)[:2]
        check_ID = True
        for lst in self.get_store_list:
            if str(save_ID) == str(lst[0]):
                check_ID = False
                break
        if check_ID:
            self.get_store_list.append([str(cvID)[:2],[]])
        self.VoiceRoidList[-1].LagTimer.changeLag(self.times)
        
    def changeRGB2(self,washaName,R,G,B):
        for vList in self.VoiceRoidList:
            if vList.washaName == washaName:
                vList.Red = R
                vList.Green = G
                vList.Blue = B
                
    def changeRGB2(self,num,R,G,B):
        self.VoiceRoidList[num].Red = R
        self.VoiceRoidList[num].Green = G
        self.VoiceRoidList[num].Blue = B

    def appendNameList(self,henkouMae,HenkuGo):
        self.changeNameList.append([henkouMae,HenkuGo])
        
    def up_Namelist(self,num):
        self.changeNameList[num],self.changeNameList[num-1] = self.changeNameList[num-1],self.changeNameList[num]
        

    def removeNameList(self,Num):
        if len(self.changeNameList) > int(Num) and len(self.changeNameList) > 0:
            self.changeNameList.pop(Num)
            
    def appendRelaceList(self,washaName,henkouMae,HenkuGo):
        self.replaceList.append([henkouMae,HenkuGo,washaName])
        
    def get_rewrite_list_for_csv(self):
        if os.path.isdir('./dic'):
            while True:
                if len(self.rewriteList) > 0:
                    self.rewriteList.pop(0)
                else:
                    break
            self.rewriteList = getcsv('./dic/rewritedic.csv')
        return self.rewriteList
        
    def get_replace_list_for_csv(self):
        if os.path.isdir('./dic'):
            while True:
                if len(self.replaceList) > 0:
                    self.replaceList.pop(0)
                else:
                    break
            self.replaceList = getcsv('./dic/replacedic.csv')
        return self.replaceList
        
    def save_replace_list_to_csv(self):
        if os.path.isdir('./dic'):
            savecsv('./dic/replacedic.csv',self.replaceList)
        
    def save_rewrite_list_to_csv(self):
        if os.path.isdir('./dic'):
            savecsv('./dic/rewritedic.csv',self.rewriteList)
        
        
    def removeReplaceList(self,Num):
        if len(self.replaceList) > int(Num) and len(self.replaceList) > 0:
            self.replaceList.pop(Num)        
            
    def appendReWriteList(self,washaName,henkouMae,HenkuGo):
        self.rewriteList.append([henkouMae,HenkuGo,washaName])

        
    def removeReWriteList(self,Num):
        if len(self.rewriteList) > int(Num) and len(self.rewriteList) > 0:
            self.rewriteList.pop(Num) 
    
                    
    def vanish_change(self,num):
        if len(self.VoiceRoidList) > num:
            if self.VoiceRoidList[num].vanish:
                self.VoiceRoidList[num].vanish = False
            else:
                self.VoiceRoidList[num].vanish = True
    
    def change_Name(self,name):
        if self.changeName and len(self.changeNameList) > 0:
            for Namelist in self.changeNameList:
                    if Namelist[0] in str(name):
                        cname = name.replace(Namelist[0],Namelist[1])
                        return cname
        return name
    def sortingList(self):
        sortClock = pygame.time.Clock()
        while True:
            if dis.discord_run_now:
                while len(dis.getlist) > 0:
                    self.tasklist.append(dis.getlist[0][:])
                    dis.getlist.pop(0)
            
            if len(self.tasklist) > 0:
                if self.tasklist[0][0] == "talk":
                    self.tasklist[0].pop(0)
                    self.tasklist[0][0] = self.tasklist[0][0].replace('.wav','')
                    

                    self.tasklist[0][0] = self.change_Name(self.tasklist[0][0])
                    
                    if self.changeWord:
                        noReWite = True
                        if len(self.rewriteList) > 0:
                            for wWordlist in self.rewriteList:
                                if wWordlist[0] in self.tasklist[0][1] and wWordlist[2] in self.tasklist[0][0]:
                                    self.tasklist[0][1] = str(wWordlist[1])
                                    noReWite = False
                                    break
                            
                        if len(self.replaceList) > 0 and noReWite:
                            for pWordlist in self.replaceList:
                                if pWordlist[0] in self.tasklist[0][1] and pWordlist[2] in self.tasklist[0][0]:
                                    self.tasklist[0][1] = self.tasklist[0][1].replace(pWordlist[0],pWordlist[1])
                                    
                                    
                    if len(self.JimakuList) == 5:
                        self.JimakuList.pop(0)

                    self.JimakuList.append(self.tasklist[0][:])
                        
                    if len(self.VoiceRoidList) > 0:
                        for vList in self.VoiceRoidList:
                            if vList.washaName in self.tasklist[0][0]:                                    
                                self.tasklist[0][0] = self.tasklist[0][0].replace(vList.washaName,'')
                                vList.getTaskList(self.tasklist[0])
                                break
                self.tasklist.pop(0)
            if voiceRoidManager.voiceRoidManager_threading_OFF_flag:
                break
            sortClock.tick(30)
            
            
    def showChat(self):
        cv2.namedWindow("RealTime")
        im = Image.new('RGB', (960, 500), (self.R, self.G, self.B))
        textbox = im.copy()
        textbox = np.asarray(textbox)
        textbox = cv2.cvtColor(textbox,cv2.COLOR_BGR2RGB)        
        chatClock = pygame.time.Clock()
        while True:
            if self.changeColor:
                im = Image.new('RGB', (960, 500), (self.R, self.G, self.B))
            textbox = im.copy()
            draw = ImageDraw.Draw(textbox)
            i = 0
            for Jimaku in self.JimakuList:
                strnum = len(Jimaku[0])
                strnum -= len(Jimaku[0].rsplit("-")[1]) + 12
                text = str(Jimaku[0][:strnum]) + ":" + str(Jimaku[1])
                font_size = 48
                while True:
                    draw.font = ImageFont.truetype("C:\Windows\Fonts\HGRPP1.ttc",font_size)
                    img_size = np.array(textbox.size)
                    txt_size = np.array(draw.font.getsize(text))
                    if img_size[0] > txt_size[0]:
                        break
                    font_size -= 2            
                pos = 0 / 2,25 + i * 100
                draw.text(pos,text, fill=(0,0,0))
                i += 1
                
            textbox = np.asarray(textbox)
            textbox = cv2.cvtColor(textbox,cv2.COLOR_BGR2RGB)
                
                
            cv2.imshow("RealTime",textbox)
            cv2.waitKey(1)
            if voiceRoidManager.voiceRoidManager_threading_OFF_flag:
                break
            chatClock.tick(10)            
            
    def changeGreen(self):
        self.R = 0
        self.G = 255
        self.B = 0
        self.changeColor = True
        
    def changeWhite(self):
        self.R = 255
        self.G = 255
        self.B = 255
        self.changeColor = True
            
    def startChat(self):
        chat = threading.Thread(target = self.showChat)
        chat.start()
    
    def startManegment(self):
        observer = threading.Thread(target = self.getTaskList)
        Sorting = threading.Thread(target = self.sortingList)
        observer.start()
        Sorting.start()
        

                    
    def startAllVoiceRoid(self):
        if len(self.VoiceRoidList) > 0:
            for vList in self.VoiceRoidList:
                if not vList.RunNow:
                    vList.startRunRoidThreading()
                    vList.RunNow = True
                    
    def startTachie(self,washaName):
        time.sleep(1)
        if len(self.VoiceRoidList) > 0:
            for vList in self.VoiceRoidList:
                if vList.washaName == washaName and not vList.TachieNow:
                    vList.startChar()

                    
                    
    def startJimaku(self,washaName):
        time.sleep(1)
        if len(self.VoiceRoidList) > 0:
            for vList in self.VoiceRoidList:
                if vList.washaName == washaName and not vList.JimakuNow:
                    vList.startJimaku()
                    
    def changeLagTime(self,times):
        self.times = times
        if len(self.VoiceRoidList) > 0:
            for vList in self.VoiceRoidList:
                vList.LagTimer.changeLag(self.times)
                
                


class discord_manager:
    
    def __init__(self):
        self.token = ''
        self.password = "password"
        self.subjank = "sdfija"
        self.sendlist = []
        self.getlist = []
        self.username = "----"
        self.userid = "----"
        self.discord_run_now =False
        self.sample_message = ""
        self.send_msg_now = False
        self.client = discord.Client()
        self.descrypyzKey = self.password.encode()
        self.k = pyDes.des(self.descrypyzKey, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
        self.safetime = lagTimer(20)

        
        
    def set_discord(self,token,pw):
        self.token = token
        self.password = str(pw)
        self.descrypyzKey = self.password.encode()
        self.k = pyDes.des(self.descrypyzKey, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

    def jankpass(self,talklist):
        t = str(talklist[0]) + "/zlso/" + str(talklist[1])
        t += self.subjank
        btl = bytearray(t.encode())
        ans = ""
        for b in btl:
            ans += str(b)
            ans += "/"
        ans = ans.rstrip("/")
        while len(ans) % 16 != 0:
            ans += "-"
        send_message = self.k.encrypt(ans)
        btlt = bytearray(send_message)
        msg = ""
        for b2 in btlt:
            msg += str(b2)
            msg += "/"
        return "!-" + str(msg).rstrip("/") + "/end/" + str(talklist[2])
    
    def remakepass(self,breakword):
        try:
            if "!-" in str(breakword):
                bw = breakword.split("/end/")
                btlt = bytearray()
                numls = str(bw[0]).lstrip("!-").split("/")
                for n in numls:
                    btlt.append(int(n))
                nums = self.k.decrypt(bytes(btlt))
                numlist = str(nums).rstrip("'").rstrip("-").rstrip("'").lstrip("b'").split("/")
                btls = bytearray()
                for num in numlist:
                    btls.append(int(num))
                word = btls.decode('utf-8')
                if self.subjank in word:
                    word = word.replace(self.subjank,"")
                    wls = word.split("/zlso/")
                    wls.append(bw[1])
                    checktime = wls[1].split("-")
                    checktime2 = str(checktime[0][-11:])
                    times = int(self.safetime.getLagTime().lstrip('0'))
                    time2 = int(checktime2.lstrip('0'))
                    if times < time2:
                        if wls[0] == "shot":
                            wls[1] = checktime[1]
                        return wls
                return None
        except:
            return None
    
                        
    def start_discord(self): 
        self.client.run(self.token)
        
    def start_threading_discord(self):
        if not self.discord_run_now:
            disc = threading.Thread(target = self.start_discord)
            disc.start()
            self.discord_run_now = True

class userClass():

    userClass_threading_OFF_flag = False
        
    def __init__(self):
        self.userName = "NoName"
        os.makedirs('OutputWav', exist_ok=True)
        self.outputfile = 'OutputWav/'
        self.threshold = 0.025
        self.thresholdmin = 0.01
        self.changePosition = []
        self.inputNow = False
        self.mute = False

        
        
    def recwav(self):
        chunk = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        blank = 0.3
        p = pyaudio.PyAudio()

        stream = p.open(format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            frames_per_buffer = chunk
            )

        cnt = 0
        all=[]
        while True:
            data = stream.read(chunk)
            x = np.frombuffer(data, dtype="int16") / 32768.0
            if userClass.userClass_threading_OFF_flag:
                break
            count = 0
            if x.max() > self.threshold and not self.mute:
                rec = 0
                filename = str(self.outputfile) + str(self.userName) + datetime.today().strftime("%m%d%H%M%S") + str(int(int(datetime.today().strftime("%f"))/100000)) + "-" + "ALTERNATEWORD" + ".wav"
                all=[]
                all.append(data)
                while rec < int(blank * RATE / chunk) and count < int(25 * RATE / chunk):
                    data = stream.read(chunk)
            
                    all.append(data)
                    x = np.frombuffer(data, dtype="int16") / 32768.0
                    if x.max() < self.thresholdmin:
                        rec += 1
                    else:
                        rec = 0
                    count += 1

                t = threading.Thread(target = self.recwav)
                t.start()
                filename = filename.replace("ALTERNATEWORD",str(self.coordinate2P()))
                data = b''.join(all)
                out = wave.open(filename,'w')
                out.setnchannels(CHANNELS)
                out.setsampwidth(2)
                out.setframerate(RATE)
                out.writeframes(data)
                out.close()
                break


            predata = data

        stream.close()
        p.terminate()
        
    def changeUserName(self,username):
        self.userName = username
        
    def getPosition(self,listnum,xp,yp,R):
        self.changePosition.append([0,listnum,xp,yp,R])
        
    def getBotton(self,listnum,R):
        if not self.inputNow:
            time.sleep(3)
            x,y = pyautogui.position()
            self.changePosition.append([0,listnum,x,y,R])
            return [x,y]
        return None
        
    def getKey(self,listNum):
        if not self.inputNow:
            self.inputNow = True
            time.sleep(3)
            key = keyboard.read_key()
            self.changePosition.append([1,listNum,key])
            self.inputNow = False
            return key
        return None
    
    def coordinate2P(self):
        x,y = pyautogui.position()        
        if len(self.changePosition) > 0:
            for plist in self.changePosition:
                if int(plist[0]) == 0 and abs(x - int(plist[2])) < int(plist[4]) and abs(y - int(plist[3])) < int(plist[4]):
                    return plist[1]
                if int(plist[0]) == 1 and keyboard.is_pressed(plist[2]):
                    return plist[1]
        return 0
    
        
    def removeCommandList(self,num):
        if len(self.changePosition) > int(num):
            self.changePosition.pop(int(num))
        
    def startRec(self):
        rec = threading.Thread(target = self.recwav)
        rec.start()
        
    def get_command_list_for_csv(self):
        if os.path.isdir('./dic'):
            while True:
                if len(self.changePosition) > 0:
                    self.changePosition.pop(0)
                else:
                    break
            self.changePosition = getcsv('./dic/cmdic.csv')
            return self.changePosition

    def save_command_list_to_csv(self):
        if os.path.isdir('./dic'):
            savecsv('./dic/cmdic.csv',self.changePosition)
        
    def changeMaxV(self,num):
        self.threshold = float(num/1000)
            
    def changeMiniV(self,num):
        fnum = float(num/1000)
        if fnum < self.threshold:
            self.thresholdmin = fnum
        else:
            self.thresholdmin = self.threshold

def savecsv(path,csvlist):
    with open(path,'w') as f:
        i = 0
        for ls1 in csvlist:
            j = 0
            for ls2 in ls1:
                f.write(str(ls2))
                if j < len(ls1) - 1:
                    f.write(",")
                j += 1
            if i < len(csvlist) - 1:
                f.write("\n")    
            i += 1
            
            
def getcsv(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            reader = list(csv.reader(f))
        return reader
    return []






dis = discord_manager()
manager = voiceRoidManager()
user = userClass()
user.startRec()
manager.startManegment()
manager.startChat()


@dis.client.event
async def on_ready():
    dis.username = dis.client.user.name
    dis.userid = dis.client.user.id
    ex.inputIDandNAMEindis(dis.username,dis.userid)
    dis.client.loop.create_task(background_loop())

        
        
@dis.client.event
async def on_message(message):
    if message.content.startswith("!setup"):
        if dis.client.user != message.author:
            dis.sendlist = []
            await dis.client.send_message(message.channel, "get channel!")
            dis.sample_message = message
            dis.send_msg_now = True

    if message.content.startswith("!-"):
        if dis.client.user != message.author:
            get_msg = dis.remakepass(message.content)
            if str(get_msg[0]) == "shot":
                if str(get_msg[2]) == "up" and len(manager.VoiceRoidList) > 0:
                    name = manager.change_Name(get_msg[1])
                    for vList in manager.VoiceRoidList:
                        if str(vList.washaName) == str(name) and vList.cv == "NoVoice": 
                            vList.speeknow += 1
                            break
                if str(get_msg[2]) == "down" and len(manager.VoiceRoidList) > 0:
                    name = manager.change_Name(get_msg[1])
                    for vList in manager.VoiceRoidList:
                        if str(vList.washaName) == str(name) and vList.cv == "NoVoice": 
                            vList.speeknow -= 1
                            break               
            else:
                dis.getlist.append(get_msg)

async def background_loop():
    await dis.client.wait_until_ready()
    while not dis.client.is_closed:
        if dis.send_msg_now and len(dis.sendlist) > 0 and dis.discord_run_now:
            while dis.send_msg_now and len(dis.sendlist) > 0 and dis.discord_run_now:
                send_message = dis.jankpass(dis.sendlist[0])
                dis.sendlist.pop(0)
                await dis.client.send_message(dis.sample_message.channel, send_message)
        await asyncio.sleep(1)

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(
            self, 
            parent, 
            title=title, 
            size=(720,720))
        notebook = wx.Notebook(self, wx.ID_ANY,style=wx.NB_TOP)
        panel1 = wx.Panel(notebook, wx.ID_ANY)
        panel1.SetBackgroundColour(wx.WHITE)
 
        panel2 = wx.Panel(notebook, wx.ID_ANY)
        panel2.SetBackgroundColour(wx.WHITE) 
        
        panel3 = wx.Panel(notebook, wx.ID_ANY)
        panel3.SetBackgroundColour(wx.WHITE) 
        
        panel4 = wx.Panel(notebook, wx.ID_ANY)
        panel4.SetBackgroundColour(wx.WHITE)
 
        panel5 = wx.Panel(notebook, wx.ID_ANY)
        panel5.SetBackgroundColour(wx.WHITE) 
        
        panel6 = wx.Panel(notebook, wx.ID_ANY)
        panel6.SetBackgroundColour(wx.WHITE)
        
        
        notebook.InsertPage(0, panel1, "名前の設定")
        notebook.InsertPage(1, panel2, "ボイスロイド")
        notebook.InsertPage(2, panel3, "変換設定")
        notebook.InsertPage(3, panel4, "表情の設定")
        notebook.InsertPage(4, panel5, "discord")
        notebook.InsertPage(5, panel6, "マイク")
        
        #tab1
        
        panel1_1 = wx.Panel(panel1, wx.ID_ANY, size=(720, 60))
        panel1_2 = wx.Panel(panel1, wx.ID_ANY, size=(720, 50))
        panel1_3 = wx.Panel(panel1, wx.ID_ANY, size=(720, 50))
        panel1_4 = wx.Panel(panel1, wx.ID_ANY, size=(720, 50))
        panel1_5 = wx.Panel(panel1, wx.ID_ANY, size=(720, 50))
        panel1_6 = wx.Panel(panel1, wx.ID_ANY, size=(720, 50))
        panel1_7 = wx.Panel(panel1, wx.ID_ANY, size=(720, 50))
        panel1_8 = wx.Panel(panel1, wx.ID_ANY, size=(720, 160))
        panel1_9 = wx.Panel(panel1, wx.ID_ANY, size=(720, 40))
        panel1_10 = wx.Panel(panel1, wx.ID_ANY, size=(720, 40))
        panel1_11 = wx.Panel(panel1, wx.ID_ANY, size=(720, 40))
  
        
        

        
        
        
        layout1_1 = wx.BoxSizer(wx.HORIZONTAL)
        label1_1 = wx.StaticText(panel1_1, wx.ID_ANY, 'ユーザーネーム設定', style=wx.TE_CENTER, size=(720, 60))
        font = wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        label1_1.SetFont(font)
        layout1_1.Add(label1_1,flag = wx.GROW | wx.ALL, border=10)
        panel1_1.SetSizer(layout1_1)

        layout1_2 = wx.BoxSizer(wx.HORIZONTAL)
        label1_2 = wx.StaticText(panel1_2, wx.ID_ANY, '新しいユーザー名',style=wx.TE_CENTER, size=(240, 50))
        font = wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        label1_2.SetFont(font)
        self.textbox1_1 = wx.TextCtrl(panel1_2,wx.ID_ANY, size=(240, 50))
        self.textbox1_1.SetFont(font)
        self.button1_1 = wx.Button(panel1_2, wx.ID_ANY, '登録', size=(240, 50))
        layout1_2.Add(label1_2,flag = wx.GROW | wx.ALL, border=5)
        layout1_2.Add(self.textbox1_1,flag = wx.GROW | wx.ALL, border=5)
        layout1_2.Add(self.button1_1,flag = wx.GROW | wx.ALL, border=5)
        panel1_2.SetSizer(layout1_2)        
        
        layout1_3 = wx.BoxSizer(wx.HORIZONTAL)
        label1_3 = wx.StaticText(panel1_3, wx.ID_ANY, '現在のユーザー名：',style=wx.TE_RIGHT, size=(360, 50))
        font = wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        label1_3.SetFont(font)
        self.label1_3_2 = wx.StaticText(panel1_3, wx.ID_ANY, 'NoName',style=wx.TE_LEFT, size=(360, 50))
        self.label1_3_2.SetFont(font)
        layout1_3.Add(label1_3,flag = wx.GROW | wx.ALL, border=5)
        layout1_3.Add(self.label1_3_2,flag = wx.GROW | wx.ALL, border=5)
        panel1_3.SetSizer(layout1_3)
        
        layout1_4 = wx.BoxSizer(wx.HORIZONTAL)
        label1_4 = wx.StaticText(panel1_4, wx.ID_ANY, '名前の変更設定', style=wx.TE_CENTER, size=(720, 50))
        font = wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        label1_4.SetFont(font)
        layout1_4.Add(label1_4,flag = wx.GROW | wx.ALL, border=5)
        panel1_4.SetSizer(layout1_4)
        
        layout1_5 = wx.BoxSizer(wx.HORIZONTAL)
        label1_5 = wx.StaticText(panel1_5, wx.ID_ANY, '名前変更前',style=wx.TE_RIGHT, size=(240, 50))
        label1_5.SetFont(font)
        self.textbox1_5 = wx.TextCtrl(panel1_5,wx.ID_ANY, size=(240, 50))
        self.textbox1_5.SetFont(font)
        layout1_5.Add(label1_5,flag = wx.GROW | wx.ALL, border=5)
        layout1_5.Add(self.textbox1_5,flag = wx.GROW | wx.ALL, border=5)
        panel1_5.SetSizer(layout1_5)          
        
        
        layout1_6 = wx.BoxSizer(wx.HORIZONTAL)
        label1_6 = wx.StaticText(panel1_6, wx.ID_ANY, '名前変更後',style=wx.TE_RIGHT, size=(240, 50))
        label1_6.SetFont(font)
        self.textbox1_6 = wx.TextCtrl(panel1_6,wx.ID_ANY, size=(240, 50))
        self.textbox1_6.SetFont(font)
        layout1_6.Add(label1_6,flag = wx.GROW | wx.ALL, border=5)
        layout1_6.Add(self.textbox1_6,flag = wx.GROW | wx.ALL, border=5)
        panel1_6.SetSizer(layout1_6)
        
        
        layout1_7 = wx.BoxSizer(wx.HORIZONTAL)
        self.button1_7_1 = wx.Button(panel1_7, wx.ID_ANY, '登録', size=(240, 40))
        self.button1_7_2 = wx.Button(panel1_7, wx.ID_ANY, '並び替え', size=(240, 40))
        layout1_7.Add(self.button1_7_1,flag = wx.GROW | wx.LEFT, border=118)
        layout1_7.Add(self.button1_7_2,flag = wx.GROW | wx.RIGHT, border=118)
        panel1_7.SetSizer(layout1_7)
        
        layout1_8 = wx.BoxSizer(wx.HORIZONTAL)
        self.listbox1_8 = wx.ListCtrl(panel1_8, wx.ID_ANY, style=wx.LC_REPORT, size=(360, 160))
        self.listbox1_8.InsertColumn(0, "変換前", wx.LIST_FORMAT_LEFT, 170)
        self.listbox1_8.InsertColumn(1, "変換後", wx.LIST_FORMAT_LEFT, 170)
        layout1_8.Add(self.listbox1_8,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=180)
        panel1_8.SetSizer(layout1_8)
        
        
        layout1_9 = wx.BoxSizer(wx.HORIZONTAL)
        label1_9 = wx.StaticText(panel1_9, wx.ID_ANY, '名前変換フィルターの削除', style=wx.TE_RIGHT, size=(360, 40))
        label1_9.SetFont(font)
        self.button1_9 = wx.Button(panel1_9, wx.ID_ANY, '削除', size=(160, 40))
        layout1_9.Add(label1_9,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=10)
        layout1_9.Add(self.button1_9,flag = wx.GROW | wx.RIGHT, border=10)
        panel1_9.SetSizer(layout1_9)
        
        
        layout1_10 = wx.BoxSizer(wx.HORIZONTAL)
        label1_10 = wx.StaticText(panel1_10, wx.ID_ANY, '名前変換フィルター', style=wx.TE_RIGHT, size=(360, 40))
        label1_10.SetFont(font)
        self.button1_10 = wx.Button(panel1_10, wx.ID_ANY, 'ON', size=(160, 40))
        layout1_10.Add(label1_10,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=10)
        layout1_10.Add(self.button1_10,flag = wx.GROW | wx.RIGHT, border=10)
        panel1_10.SetSizer(layout1_10)        
        

        layout1_11 = wx.BoxSizer(wx.HORIZONTAL)
        label1_11 = wx.StaticText(panel1_11, wx.ID_ANY, '背景色の変更', style=wx.TE_RIGHT, size=(360, 40))
        label1_11.SetFont(font)
        self.button1_11 = wx.Button(panel1_11, wx.ID_ANY, '背景白', size=(160, 40))
        layout1_11.Add(label1_11,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=10)
        layout1_11.Add(self.button1_11,flag = wx.GROW | wx.RIGHT, border=10)
        panel1_11.SetSizer(layout1_11)        
        
        
        
        
        layout1 = wx.BoxSizer(wx.VERTICAL)
        layout1.Add(panel1_1, 0, wx.GROW | wx.ALL, border=5)
        layout1.Add(panel1_2, 0, wx.GROW | wx.ALL)
        layout1.Add(panel1_3, 0, wx.GROW | wx.ALL)
        layout1.Add(panel1_4, 0, wx.GROW | wx.ALL)
        layout1.Add(panel1_5, 0, wx.GROW | wx.ALL)
        layout1.Add(panel1_6, 0, wx.GROW | wx.ALL)
        layout1.Add(panel1_7, 0, wx.GROW | wx.ALL)
        layout1.Add(panel1_8, 0, wx.GROW | wx.ALL)
        layout1.Add(panel1_9, 0, wx.GROW | wx.ALL)
        layout1.Add(panel1_10, 0, wx.GROW | wx.ALL)
        layout1.Add(panel1_11, 0, wx.GROW | wx.ALL)
        
        panel1.SetSizer(layout1)


        #tab2
        panel2_1 = wx.Panel(panel2, wx.ID_ANY, size=(720, 60))
        panel2_2 = wx.Panel(panel2, wx.ID_ANY, size=(720, 40))
        panel2_3 = wx.Panel(panel2, wx.ID_ANY, size=(720, 40))       
        panel2_4 = wx.Panel(panel2, wx.ID_ANY, size=(720, 40))
        panel2_5 = wx.Panel(panel2, wx.ID_ANY, size=(720, 180))
        panel2_6 = wx.Panel(panel2, wx.ID_ANY, size=(720, 40))
        panel2_7 = wx.Panel(panel2, wx.ID_ANY, size=(720, 80))
        panel2_8 = wx.Panel(panel2, wx.ID_ANY, size=(720, 40))
        panel2_9 = wx.Panel(panel2, wx.ID_ANY, size=(720, 40))
        panel2_10 = wx.Panel(panel2, wx.ID_ANY, size=(720, 40))
        panel2_11 = wx.Panel(panel2, wx.ID_ANY, size=(720, 40))
      

        
        
        
        layout2_1 = wx.BoxSizer(wx.HORIZONTAL)
        label2_1 = wx.StaticText(panel2_1, wx.ID_ANY, 'ボイスロイド設定', style=wx.TE_CENTER, size=(720, 60))
        font = wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        label2_1.SetFont(font)
        layout2_1.Add(label2_1,flag = wx.GROW | wx.ALL, border=10)
        panel2_1.SetSizer(layout2_1)
        
        
        layout2_2 = wx.BoxSizer(wx.HORIZONTAL)
        label2_2 = wx.StaticText(panel2_2, wx.ID_ANY, 'ボイスロイドのID',style=wx.TE_RIGHT, size=(360, 50))
        label2_2.SetFont(font)
        self.textbox2_2 = wx.TextCtrl(panel2_2,wx.ID_ANY, size=(240, 40))
        self.textbox2_2.SetFont(font)
        layout2_2.Add(label2_2,flag = wx.GROW | wx.ALL, border=5)
        layout2_2.Add(self.textbox2_2,flag = wx.GROW | wx.ALL, border=5)
        panel2_2.SetSizer(layout2_2)
        
        layout2_3 = wx.BoxSizer(wx.HORIZONTAL)
        label2_3 = wx.StaticText(panel2_3, wx.ID_ANY, 'ボイスロイドの名前',style=wx.TE_RIGHT, size=(360, 50))
        label2_3.SetFont(font)
        self.textbox2_3 = wx.TextCtrl(panel2_3,wx.ID_ANY, size=(240, 40))
        self.textbox2_3.SetFont(font)
        layout2_3.Add(label2_3,flag = wx.GROW | wx.ALL, border=5)
        layout2_3.Add(self.textbox2_3,flag = wx.GROW | wx.ALL, border=5)
        panel2_3.SetSizer(layout2_3)
        
        
        
        layout2_4 = wx.BoxSizer(wx.HORIZONTAL)
        self.button2_4 = wx.Button(panel2_4, wx.ID_ANY, 'ボイスロイドの登録', size=(240, 40))
        layout2_4.Add(self.button2_4,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=240)
        panel2_4.SetSizer(layout2_4) 
        
        layout2_5 = wx.BoxSizer(wx.HORIZONTAL)
        self.listbox2_5 = wx.ListCtrl(panel2_5, wx.ID_ANY, style=wx.LC_REPORT, size=(480, 180))
        self.listbox2_5.InsertColumn(0, "ID", wx.LIST_FORMAT_LEFT, 80)
        self.listbox2_5.InsertColumn(1, "名前", wx.LIST_FORMAT_LEFT, 180)
        self.listbox2_5.InsertColumn(2, "字幕RGB", wx.LIST_FORMAT_LEFT, 100)
        self.listbox2_5.InsertColumn(3, "VANISH", wx.LIST_FORMAT_LEFT, 100)        
        layout2_5.Add(self.listbox2_5,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=120)
        panel2_5.SetSizer(layout2_5)
        
        layout2_6 = wx.BoxSizer(wx.HORIZONTAL)
        label2_6 = wx.StaticText(panel2_6, wx.ID_ANY, 'RGBの設定', style=wx.TE_CENTER, size=(720, 40))
        font = wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        label2_6.SetFont(font)
        layout2_6.Add(label2_6,flag = wx.GROW | wx.ALL,border = 5)
        panel2_6.SetSizer(layout2_6)        
        
        layout2_7 = wx.GridSizer(rows=2, cols=3, gap=(0, 0))
        label2_7_1 = wx.StaticText(panel2_7, wx.ID_ANY, 'RED', style=wx.TE_CENTER, size=(240, 40))
        label2_7_2 = wx.StaticText(panel2_7, wx.ID_ANY, 'GREEN', style=wx.TE_CENTER, size=(240, 40))
        label2_7_3 = wx.StaticText(panel2_7, wx.ID_ANY, 'BLUE', style=wx.TE_CENTER, size=(240, 40))
        self.textbox2_7_1 = wx.TextCtrl(panel2_7,wx.ID_ANY, size=(240, 40))
        self.textbox2_7_2 = wx.TextCtrl(panel2_7,wx.ID_ANY, size=(240, 40))
        self.textbox2_7_3 = wx.TextCtrl(panel2_7,wx.ID_ANY, size=(240, 40))
        label2_7_1.SetFont(font)
        label2_7_2.SetFont(font)
        label2_7_3.SetFont(font)
        self.textbox2_7_1.SetFont(font)
        self.textbox2_7_2.SetFont(font)
        self.textbox2_7_3.SetFont(font)
        layout2_7.Add(label2_7_1,flag=wx.GROW)
        layout2_7.Add(label2_7_2,flag=wx.GROW)
        layout2_7.Add(label2_7_3,flag=wx.GROW)
        layout2_7.Add(self.textbox2_7_1,flag=wx.GROW)
        layout2_7.Add(self.textbox2_7_2,flag=wx.GROW)
        layout2_7.Add(self.textbox2_7_3,flag=wx.GROW)
        panel2_7.SetSizer(layout2_7) 
        
        layout2_8 = wx.BoxSizer(wx.HORIZONTAL)
        self.button2_8 = wx.Button(panel2_8, wx.ID_ANY, 'RGBの登録', size=(240, 40))
        layout2_8.Add(self.button2_8,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=240)
        panel2_8.SetSizer(layout2_8) 
        
        
        layout2_9 = wx.BoxSizer(wx.HORIZONTAL)
        label2_9 = wx.StaticText(panel2_9, wx.ID_ANY, '立ち絵が消えるかの設定', style=wx.TE_RIGHT, size=(360, 40))
        label2_9.SetFont(font)
        self.button2_9 = wx.Button(panel2_9, wx.ID_ANY, '切り替え', size=(160, 40))
        layout2_9.Add(label2_9,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=10)
        layout2_9.Add(self.button2_9,flag = wx.GROW | wx.RIGHT, border=10)
        panel2_9.SetSizer(layout2_9)            
        
        layout2_10 = wx.BoxSizer(wx.HORIZONTAL)
        label2_10 = wx.StaticText(panel2_10, wx.ID_ANY, 'ラグの時間変更', style=wx.TE_RIGHT, size=(360, 40))
        label2_10.SetFont(font)
        self.slider2_10 = wx.Slider(panel2_10,style=wx.SL_LABELS, size=(240, 40))
        self.slider2_10.SetValue(10)
        self.slider2_10.SetMin(0)
        self.slider2_10.SetMax(59)
        layout2_10.Add(label2_10,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=10)
        layout2_10.Add(self.slider2_10,flag = wx.GROW | wx.RIGHT, border=40)
        panel2_10.SetSizer(layout2_10)         
        
        layout2 = wx.BoxSizer(wx.VERTICAL)
        layout2.Add(panel2_1, 0, wx.GROW | wx.ALL, border=5)
        layout2.Add(panel2_2, 0, wx.GROW | wx.ALL)
        layout2.Add(panel2_3, 0, wx.GROW | wx.ALL)
        layout2.Add(panel2_4, 0, wx.GROW | wx.ALL)
        layout2.Add(panel2_5, 0, wx.GROW | wx.ALL)
        layout2.Add(panel2_6, 0, wx.GROW | wx.ALL, border=5)
        layout2.Add(panel2_7, 0, wx.GROW | wx.ALL)
        layout2.Add(panel2_8, 0, wx.GROW | wx.ALL, border=5)
        layout2.Add(panel2_9, 0, wx.GROW | wx.ALL)
        layout2.Add(panel2_10, 0, wx.GROW | wx.ALL)
        layout2.Add(panel2_11, 0, wx.GROW | wx.ALL)

        panel2.SetSizer(layout2)
        
        
        #tab3
        panel3_1 = wx.Panel(panel3, wx.ID_ANY, size=(720, 40))
        panel3_2 = wx.Panel(panel3, wx.ID_ANY, size=(720, 60))
        panel3_3 = wx.Panel(panel3, wx.ID_ANY, size=(720, 40))    
        panel3_4 = wx.Panel(panel3, wx.ID_ANY, size=(720, 180))
        panel3_5 = wx.Panel(panel3, wx.ID_ANY, size=(720, 40)) 
        panel3_6 = wx.Panel(panel3, wx.ID_ANY, size=(720, 60))
        panel3_7 = wx.Panel(panel3, wx.ID_ANY, size=(720, 40))
        panel3_8 = wx.Panel(panel3, wx.ID_ANY, size=(720, 180))
        
        
        layout3_1 = wx.BoxSizer(wx.HORIZONTAL)
        label3_1 = wx.StaticText(panel3_1, wx.ID_ANY, '書き換え設定', style=wx.TE_CENTER, size=(720, 60))
        font = wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        label3_1.SetFont(font)
        layout3_1.Add(label3_1,flag = wx.GROW | wx.ALL, border=5)
        panel3_1.SetSizer(layout3_1) 
        
        
        layout3_2 = wx.GridSizer(rows=2, cols=3, gap=(0, 0))
        label3_2_1 = wx.StaticText(panel3_2, wx.ID_ANY, '話者', style=wx.TE_CENTER, size=(240, 30))
        label3_2_2 = wx.StaticText(panel3_2, wx.ID_ANY, '変換前', style=wx.TE_CENTER, size=(240, 30))
        label3_2_3 = wx.StaticText(panel3_2, wx.ID_ANY, '変換後', style=wx.TE_CENTER, size=(240, 30))
        self.textbox3_2_1 = wx.TextCtrl(panel3_2,wx.ID_ANY, size=(240, 30))
        self.textbox3_2_2 = wx.TextCtrl(panel3_2,wx.ID_ANY, size=(240, 30))
        self.textbox3_2_3 = wx.TextCtrl(panel3_2,wx.ID_ANY, size=(240, 30))
        label3_2_1.SetFont(font)
        label3_2_2.SetFont(font)
        label3_2_3.SetFont(font)
        self.textbox3_2_1.SetFont(font)
        self.textbox3_2_2.SetFont(font)
        self.textbox3_2_3.SetFont(font)
        layout3_2.Add(label3_2_1,flag=wx.GROW)
        layout3_2.Add(label3_2_2,flag=wx.GROW)
        layout3_2.Add(label3_2_3,flag=wx.GROW)
        layout3_2.Add(self.textbox3_2_1,flag=wx.GROW)
        layout3_2.Add(self.textbox3_2_2,flag=wx.GROW)
        layout3_2.Add(self.textbox3_2_3,flag=wx.GROW)
        panel3_2.SetSizer(layout3_2)
        
        
        
        layout3_3 = wx.BoxSizer(wx.HORIZONTAL)
        self.button3_3_1 = wx.Button(panel3_3, wx.ID_ANY, '登録', size=(180, 40))
        self.button3_3_2 = wx.Button(panel3_3, wx.ID_ANY, '削除', size=(180, 40))
        self.button3_3_3 = wx.Button(panel3_3, wx.ID_ANY, 'セーブ', size=(180, 40))
        self.button3_3_4 = wx.Button(panel3_3, wx.ID_ANY, 'ロード', size=(180, 40))
        layout3_3.Add(self.button3_3_1,flag = wx.GROW)
        layout3_3.Add(self.button3_3_2,flag = wx.GROW)
        layout3_3.Add(self.button3_3_3,flag = wx.GROW)
        layout3_3.Add(self.button3_3_4,flag = wx.GROW)
        panel3_3.SetSizer(layout3_3) 
        
        
        layout3_4 = wx.BoxSizer(wx.HORIZONTAL)
        self.listbox3_4 = wx.ListCtrl(panel3_4, wx.ID_ANY, style=wx.LC_REPORT, size=(720, 180))
        self.listbox3_4.InsertColumn(0, "話者", wx.LIST_FORMAT_LEFT, 80)
        self.listbox3_4.InsertColumn(1, "変換前", wx.LIST_FORMAT_LEFT, 320)
        self.listbox3_4.InsertColumn(2, "変換後", wx.LIST_FORMAT_LEFT, 320)     
        layout3_4.Add(self.listbox3_4,flag = wx.GROW )
        panel3_4.SetSizer(layout3_4)
        
        
        layout3_5 = wx.BoxSizer(wx.HORIZONTAL)
        label3_5 = wx.StaticText(panel3_5, wx.ID_ANY, '置き換え設定', style=wx.TE_CENTER, size=(720, 60))
        font = wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        label3_5.SetFont(font)
        layout3_5.Add(label3_5,flag = wx.GROW | wx.ALL, border=5)
        panel3_1.SetSizer(layout3_5) 
        
        
        layout3_6 = wx.GridSizer(rows=2, cols=3, gap=(0, 0))
        label3_6_1 = wx.StaticText(panel3_6, wx.ID_ANY, '話者', style=wx.TE_CENTER, size=(240, 30))
        label3_6_2 = wx.StaticText(panel3_6, wx.ID_ANY, '変換前', style=wx.TE_CENTER, size=(240, 30))
        label3_6_3 = wx.StaticText(panel3_6, wx.ID_ANY, '変換後', style=wx.TE_CENTER, size=(240, 30))
        self.textbox3_6_1 = wx.TextCtrl(panel3_6,wx.ID_ANY, size=(240, 30))
        self.textbox3_6_2 = wx.TextCtrl(panel3_6,wx.ID_ANY, size=(240, 30))
        self.textbox3_6_3 = wx.TextCtrl(panel3_6,wx.ID_ANY, size=(240, 30))
        label3_6_1.SetFont(font)
        label3_6_2.SetFont(font)
        label3_6_3.SetFont(font)
        self.textbox3_6_1.SetFont(font)
        self.textbox3_6_2.SetFont(font)
        self.textbox3_6_3.SetFont(font)
        layout3_6.Add(label3_6_1,flag=wx.GROW)
        layout3_6.Add(label3_6_2,flag=wx.GROW)
        layout3_6.Add(label3_6_3,flag=wx.GROW)
        layout3_6.Add(self.textbox3_6_1,flag=wx.GROW)
        layout3_6.Add(self.textbox3_6_2,flag=wx.GROW)
        layout3_6.Add(self.textbox3_6_3,flag=wx.GROW)
        panel3_6.SetSizer(layout3_6)
        
        
        
        layout3_7 = wx.BoxSizer(wx.HORIZONTAL)
        self.button3_7_1 = wx.Button(panel3_7, wx.ID_ANY, '登録', size=(180, 40))
        self.button3_7_2 = wx.Button(panel3_7, wx.ID_ANY, '削除', size=(180, 40))
        self.button3_7_3 = wx.Button(panel3_7, wx.ID_ANY, 'セーブ', size=(180, 40))
        self.button3_7_4 = wx.Button(panel3_7, wx.ID_ANY, 'ロード', size=(180, 40))
        layout3_7.Add(self.button3_7_1,flag = wx.GROW)
        layout3_7.Add(self.button3_7_2,flag = wx.GROW)
        layout3_7.Add(self.button3_7_3,flag = wx.GROW)
        layout3_7.Add(self.button3_7_4,flag = wx.GROW)
        panel3_7.SetSizer(layout3_7) 
        
        
        layout3_8 = wx.BoxSizer(wx.HORIZONTAL)
        self.listbox3_8 = wx.ListCtrl(panel3_8, wx.ID_ANY, style=wx.LC_REPORT, size=(720, 180))
        self.listbox3_8.InsertColumn(0, "話者", wx.LIST_FORMAT_LEFT, 80)
        self.listbox3_8.InsertColumn(1, "変換前", wx.LIST_FORMAT_LEFT, 320)
        self.listbox3_8.InsertColumn(2, "変換後", wx.LIST_FORMAT_LEFT, 320)     
        layout3_8.Add(self.listbox3_8,flag = wx.GROW )
        panel3_8.SetSizer(layout3_8)
        
        
        
        
        layout3 = wx.BoxSizer(wx.VERTICAL)
        layout3.Add(panel3_1, 0, wx.GROW | wx.ALL)
        layout3.Add(panel3_2, 0, wx.GROW | wx.ALL)
        layout3.Add(panel3_3, 0, wx.GROW | wx.ALL)
        layout3.Add(panel3_4, 0, wx.GROW | wx.ALL)
        layout3.Add(panel3_5, 0, wx.GROW | wx.ALL)
        layout3.Add(panel3_6, 0, wx.GROW | wx.ALL)
        layout3.Add(panel3_7, 0, wx.GROW | wx.ALL)
        layout3.Add(panel3_8, 0, wx.GROW | wx.ALL)


        panel3.SetSizer(layout3)
        
        
        
        
        #tab4
        panel4_1 = wx.Panel(panel4, wx.ID_ANY, size=(720, 60))
        panel4_2 = wx.Panel(panel4, wx.ID_ANY, size=(720, 40))
        panel4_3 = wx.Panel(panel4, wx.ID_ANY, size=(720, 60))    
        panel4_4 = wx.Panel(panel4, wx.ID_ANY, size=(720, 40))
        panel4_5 = wx.Panel(panel4, wx.ID_ANY, size=(720, 40)) 
        panel4_6 = wx.Panel(panel4, wx.ID_ANY, size=(720, 60))
        panel4_6_2 = wx.Panel(panel4, wx.ID_ANY, size=(720, 40))
        panel4_7 = wx.Panel(panel4, wx.ID_ANY, size=(720, 240))
        panel4_8 = wx.Panel(panel4, wx.ID_ANY, size=(720, 40))
        
        
        layout4_1 = wx.BoxSizer(wx.HORIZONTAL)
        label4_1 = wx.StaticText(panel4_1, wx.ID_ANY, '表情変化アクションの設定', style=wx.TE_CENTER, size=(720, 60))
        label4_1.SetFont(font)
        layout4_1.Add(label4_1,flag = wx.GROW | wx.ALL, border=10)
        panel4_1.SetSizer(layout4_1)
        
        
        layout4_2 = wx.BoxSizer(wx.HORIZONTAL)
        label4_2 = wx.StaticText(panel4_2, wx.ID_ANY, '表情番号',style=wx.TE_RIGHT, size=(300, 50))
        label4_2.SetFont(font)
        self.textbox4_2 = wx.TextCtrl(panel4_2,wx.ID_ANY, size=(240, 40))
        self.textbox4_2.SetFont(font)
        layout4_2.Add(label4_2,flag = wx.GROW | wx.ALL, border=5)
        layout4_2.Add(self.textbox4_2,flag = wx.GROW | wx.ALL, border=5)
        panel4_2.SetSizer(layout4_2)
        
        layout4_3 = wx.BoxSizer(wx.HORIZONTAL)
        label4_3 = wx.StaticText(panel4_3, wx.ID_ANY, 'マウスアクションの設定', style=wx.TE_CENTER, size=(720, 60))
        label4_3.SetFont(font)
        layout4_3.Add(label4_3,flag = wx.GROW | wx.ALL, border=10)
        panel4_3.SetSizer(layout4_3)
        
        layout4_4 = wx.BoxSizer(wx.HORIZONTAL)
        label4_4 = wx.StaticText(panel4_4, wx.ID_ANY, 'マウスフィールドの大きさ',style=wx.TE_RIGHT, size=(300, 50))
        label4_4.SetFont(font)
        self.textbox4_4 = wx.TextCtrl(panel4_4,wx.ID_ANY, size=(240, 40))
        self.textbox4_4.SetFont(font)
        layout4_4.Add(label4_4,flag = wx.GROW | wx.ALL, border=5)
        layout4_4.Add(self.textbox4_4,flag = wx.GROW | wx.ALL, border=5)
        panel4_4.SetSizer(layout4_4)
        
        
        layout4_5 = wx.BoxSizer(wx.HORIZONTAL)
        self.button4_5 = wx.Button(panel4_5, wx.ID_ANY, 'マウス登録', size=(240, 40))
        layout4_5.Add(self.button4_5,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=240)
        panel4_5.SetSizer(layout4_5)
        
        
        layout4_6 = wx.BoxSizer(wx.HORIZONTAL)
        label4_6 = wx.StaticText(panel4_6, wx.ID_ANY, 'キーボードの設定', style=wx.TE_CENTER, size=(720, 60))
        label4_6.SetFont(font)
        layout4_6.Add(label4_6,flag = wx.GROW | wx.ALL, border=10)
        panel4_6.SetSizer(layout4_6)
        
        layout4_6_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.button4_6_2 = wx.Button(panel4_6_2, wx.ID_ANY, 'キー登録', size=(240, 40))
        layout4_6_2.Add(self.button4_6_2,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=240)
        panel4_6_2.SetSizer(layout4_6_2) 
        
        layout4_7 = wx.BoxSizer(wx.HORIZONTAL)
        self.listbox4_7 = wx.ListCtrl(panel4_7, wx.ID_ANY, style=wx.LC_REPORT, size=(720, 240))
        self.listbox4_7.InsertColumn(0, "タイプ", wx.LIST_FORMAT_LEFT, 80)
        self.listbox4_7.InsertColumn(1, "表情", wx.LIST_FORMAT_LEFT, 80)
        self.listbox4_7.InsertColumn(2, "コマンド", wx.LIST_FORMAT_LEFT, 200)     
        layout4_7.Add(self.listbox4_7,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=180)
        panel4_7.SetSizer(layout4_7)        
        
        layout4_8 = wx.BoxSizer(wx.HORIZONTAL)
        self.button4_8_1 = wx.Button(panel4_8, wx.ID_ANY, '削除', size=(180, 40))
        self.button4_8_2 = wx.Button(panel4_8, wx.ID_ANY, 'セーブ', size=(180, 40))
        self.button4_8_3 = wx.Button(panel4_8, wx.ID_ANY, 'ロード', size=(180, 40))
        layout4_8.Add(self.button4_8_1,flag = wx.GROW | wx.LEFT, border=90)
        layout4_8.Add(self.button4_8_2,flag = wx.GROW)
        layout4_8.Add(self.button4_8_3,flag = wx.GROW | wx.RIGHT, border=90)
        panel4_8.SetSizer(layout4_8)         
        
        
        layout4 = wx.BoxSizer(wx.VERTICAL)
        layout4.Add(panel4_1, 0, wx.GROW | wx.ALL)
        layout4.Add(panel4_2, 0, wx.GROW | wx.ALL)
        layout4.Add(panel4_3, 0, wx.GROW | wx.ALL)
        layout4.Add(panel4_4, 0, wx.GROW | wx.ALL)
        layout4.Add(panel4_5, 0, wx.GROW | wx.ALL)
        layout4.Add(panel4_6, 0, wx.GROW | wx.ALL)
        layout4.Add(panel4_6_2, 0, wx.GROW | wx.ALL)
        layout4.Add(panel4_7, 0, wx.GROW | wx.ALL)
        layout4.Add(panel4_8, 0, wx.GROW | wx.TOP, border=10)


        panel4.SetSizer(layout4)
        
        
        #tab5
        panel5_1 = wx.Panel(panel5, wx.ID_ANY, size=(720, 60))
        panel5_2 = wx.Panel(panel5, wx.ID_ANY, size=(720, 40))
        panel5_3 = wx.Panel(panel5, wx.ID_ANY, size=(720, 40))    
        panel5_4 = wx.Panel(panel5, wx.ID_ANY, size=(720, 40))
        panel5_5 = wx.Panel(panel5, wx.ID_ANY, size=(720, 60)) 
        panel5_6 = wx.Panel(panel5, wx.ID_ANY, size=(720, 60))
        panel5_7 = wx.Panel(panel5, wx.ID_ANY, size=(720, 60))
        panel5_8 = wx.Panel(panel5, wx.ID_ANY, size=(720, 40))
        
        
        layout5_1 = wx.BoxSizer(wx.HORIZONTAL)
        label5_1 = wx.StaticText(panel5_1, wx.ID_ANY, 'Discordの設定', style=wx.TE_CENTER, size=(720, 60))
        label5_1.SetFont(font)
        layout5_1.Add(label5_1,flag = wx.GROW | wx.ALL, border=10)
        panel5_1.SetSizer(layout5_1)        
        
        layout5_2 = wx.BoxSizer(wx.HORIZONTAL)
        label5_2 = wx.StaticText(panel5_2, wx.ID_ANY, 'token',style=wx.TE_RIGHT, size=(300, 50))
        label5_2.SetFont(font)
        self.textbox5_2 = wx.TextCtrl(panel5_2,wx.ID_ANY, size=(240, 40))
        self.textbox5_2.SetFont(font)
        layout5_2.Add(label5_2,flag = wx.GROW | wx.ALL, border=5)
        layout5_2.Add(self.textbox5_2,flag = wx.GROW | wx.ALL, border=5)
        panel5_2.SetSizer(layout5_2)
        
        layout5_3 = wx.BoxSizer(wx.HORIZONTAL)
        label5_3 = wx.StaticText(panel5_3, wx.ID_ANY, 'pass',style=wx.TE_RIGHT, size=(300, 50))
        label5_3.SetFont(font)
        self.textbox5_3 = wx.TextCtrl(panel5_3,wx.ID_ANY, size=(240, 40))
        self.textbox5_3.SetFont(font)
        layout5_3.Add(label5_3,flag = wx.GROW | wx.ALL, border=5)
        layout5_3.Add(self.textbox5_3,flag = wx.GROW | wx.ALL, border=5)
        panel5_3.SetSizer(layout5_3)
        
        
        layout5_4 = wx.BoxSizer(wx.HORIZONTAL)
        self.button5_4 = wx.Button(panel5_4, wx.ID_ANY, 'Start Bot', size=(240, 40))
        layout5_4.Add(self.button5_4,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=240)
        panel5_4.SetSizer(layout5_4)         
        
               
        
        layout5_5 = wx.BoxSizer(wx.HORIZONTAL)
        label5_5 = wx.StaticText(panel5_5, wx.ID_ANY, 'User Name：',style=wx.TE_RIGHT, size=(360, 50))
        label5_5.SetFont(font)
        self.label5_5_2 = wx.StaticText(panel5_5, wx.ID_ANY, '----',style=wx.TE_LEFT, size=(360, 50))
        self.label5_5_2.SetFont(font)
        layout5_5.Add(label5_5,flag = wx.GROW | wx.ALL, border=5)
        layout5_5.Add(self.label5_5_2,flag = wx.GROW | wx.ALL, border=5)
        panel5_5.SetSizer(layout5_5)   
        
        layout5_6 = wx.BoxSizer(wx.HORIZONTAL)
        label5_6 = wx.StaticText(panel5_6, wx.ID_ANY, 'User ID：',style=wx.TE_RIGHT, size=(360, 50))
        label5_6.SetFont(font)
        self.label5_6_2 = wx.StaticText(panel5_6, wx.ID_ANY, '----',style=wx.TE_LEFT, size=(360, 50))
        self.label5_6_2.SetFont(font)
        layout5_6.Add(label5_6,flag = wx.GROW | wx.ALL, border=5)
        layout5_6.Add(self.label5_6_2,flag = wx.GROW | wx.ALL, border=5)
        panel5_6.SetSizer(layout5_6)   
        
        
        
        layout5_7 = wx.BoxSizer(wx.HORIZONTAL)
        label5_7 = wx.StaticText(panel5_7, wx.ID_ANY, 'pass：',style=wx.TE_RIGHT, size=(360, 50))
        label5_7.SetFont(font)
        self.label5_7_2 = wx.StaticText(panel5_7, wx.ID_ANY, '----',style=wx.TE_LEFT, size=(360, 50))
        self.label5_7_2.SetFont(font)
        layout5_7.Add(label5_7,flag = wx.GROW | wx.ALL, border=5)
        layout5_7.Add(self.label5_7_2,flag = wx.GROW | wx.ALL, border=5)
        panel5_7.SetSizer(layout5_7)         
        
        
        
        
        
        layout5_8 = wx.BoxSizer(wx.HORIZONTAL)
        label5_8 = wx.StaticText(panel5_8, wx.ID_ANY, 'shot call', style=wx.TE_RIGHT, size=(360, 40))
        label5_8.SetFont(font)
        self.button5_8 = wx.Button(panel5_8, wx.ID_ANY, 'OFF', size=(160, 40))
        layout5_8.Add(label5_8,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=10)
        layout5_8.Add(self.button5_8,flag = wx.GROW | wx.RIGHT, border=10)
        panel5_8.SetSizer(layout5_8) 
        
        layout5 = wx.BoxSizer(wx.VERTICAL)
        layout5.Add(panel5_1, 0, wx.GROW | wx.ALL,border = 5)
        layout5.Add(panel5_2, 0, wx.GROW | wx.ALL)
        layout5.Add(panel5_3, 0, wx.GROW | wx.ALL)
        layout5.Add(panel5_4, 0, wx.GROW | wx.ALL)
        layout5.Add(panel5_5, 0, wx.GROW | wx.ALL)
        layout5.Add(panel5_6, 0, wx.GROW | wx.ALL)
        layout5.Add(panel5_7, 0, wx.GROW | wx.ALL)
        layout5.Add(panel5_8, 0, wx.GROW | wx.TOP)


        panel5.SetSizer(layout5)
        
        #tab6
        panel6_1 = wx.Panel(panel6, wx.ID_ANY, size=(720, 60))
        panel6_2 = wx.Panel(panel6, wx.ID_ANY, size=(720, 60))
        panel6_3 = wx.Panel(panel6, wx.ID_ANY, size=(720, 60))    
        panel6_4 = wx.Panel(panel6, wx.ID_ANY, size=(720, 40))       
        
        layout6_1 = wx.BoxSizer(wx.HORIZONTAL)
        label6_1 = wx.StaticText(panel6_1, wx.ID_ANY, 'マイクの設定', style=wx.TE_CENTER, size=(720, 60))
        label6_1.SetFont(font)
        layout6_1.Add(label6_1,flag = wx.GROW | wx.ALL, border=10)
        panel6_1.SetSizer(layout6_1)          
        
        
        layout6_2 = wx.BoxSizer(wx.HORIZONTAL)
        label6_2 = wx.StaticText(panel6_2, wx.ID_ANY, '録音開始の閾値', style=wx.TE_RIGHT, size=(360, 40))
        label6_2.SetFont(font)
        self.slider6_2 = wx.Slider(panel6_2,style=wx.SL_LABELS, size=(240, 40))
        self.slider6_2.SetValue(25)
        self.slider6_2.SetMin(0)
        self.slider6_2.SetMax(100)
        layout6_2.Add(label6_2,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=10)
        layout6_2.Add(self.slider6_2,flag = wx.GROW | wx.RIGHT, border=40)
        panel6_2.SetSizer(layout6_2)  
        
        layout6_3 = wx.BoxSizer(wx.HORIZONTAL)
        label6_3 = wx.StaticText(panel6_3, wx.ID_ANY, '録音終了の閾値', style=wx.TE_RIGHT, size=(360, 40))
        label6_3.SetFont(font)
        self.slider6_3 = wx.Slider(panel6_3,style=wx.SL_LABELS, size=(240, 40))
        self.slider6_3.SetValue(10)
        self.slider6_3.SetMin(0)
        self.slider6_3.SetMax(100)
        layout6_3.Add(label6_3,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=10)
        layout6_3.Add(self.slider6_3,flag = wx.GROW | wx.RIGHT, border=40)
        panel6_3.SetSizer(layout6_3)  
        
        layout6_4 = wx.BoxSizer(wx.HORIZONTAL)
        label6_4 = wx.StaticText(panel6_4, wx.ID_ANY, 'ミュート', style=wx.TE_RIGHT, size=(360, 40))
        label6_4.SetFont(font)
        self.button6_4 = wx.Button(panel6_4, wx.ID_ANY, 'OFF', size=(160, 40))
        layout6_4.Add(label6_4,flag = wx.GROW | wx.LEFT | wx.RIGHT, border=10)
        layout6_4.Add(self.button6_4,flag = wx.GROW | wx.RIGHT, border=10)
        panel6_4.SetSizer(layout6_4) 
        
        layout6 = wx.BoxSizer(wx.VERTICAL)
        layout6.Add(panel6_1, 0, wx.GROW | wx.ALL,border = 5)
        layout6.Add(panel6_2, 0, wx.GROW | wx.ALL)
        layout6.Add(panel6_3, 0, wx.GROW | wx.ALL)
        layout6.Add(panel6_4, 0, wx.GROW | wx.ALL)
        panel6.SetSizer(layout6)
        
        #コントロール構造bind
        
        self.button1_1.Bind(wx.EVT_BUTTON,self.buttonclick1_1)
        self.button1_7_1.Bind(wx.EVT_BUTTON,self.buttonclick1_2)
        self.button1_7_2.Bind(wx.EVT_BUTTON,self.buttonclick1_2_2)
        
        self.button1_9.Bind(wx.EVT_BUTTON,self.buttonclick1_3)
        self.button1_10.Bind(wx.EVT_BUTTON,self.buttonclick1_4)
        self.button1_11.Bind(wx.EVT_BUTTON,self.buttonclick1_5)
        self.button2_4.Bind(wx.EVT_BUTTON,self.buttonclick2_1)
        self.button2_8.Bind(wx.EVT_BUTTON,self.buttonclick2_2)
        self.button2_9.Bind(wx.EVT_BUTTON,self.buttonclick2_3)
        self.slider2_10.Bind(wx.EVT_SLIDER,self.slider_change2_1)
        self.button3_3_1.Bind(wx.EVT_BUTTON,self.buttonclick3_1_1)
        self.button3_3_2.Bind(wx.EVT_BUTTON,self.buttonclick3_1_2)
        self.button3_3_3.Bind(wx.EVT_BUTTON,self.buttonclick3_1_3)
        self.button3_3_4.Bind(wx.EVT_BUTTON,self.buttonclick3_1_4)
        self.button3_7_1.Bind(wx.EVT_BUTTON,self.buttonclick3_2_1)
        self.button3_7_2.Bind(wx.EVT_BUTTON,self.buttonclick3_2_2)
        self.button3_7_3.Bind(wx.EVT_BUTTON,self.buttonclick3_2_3)
        self.button3_7_4.Bind(wx.EVT_BUTTON,self.buttonclick3_2_4)
        
        self.button4_5.Bind(wx.EVT_BUTTON,self.buttonclick4_1)
        self.button4_6_2.Bind(wx.EVT_BUTTON,self.buttonclick4_2)
        self.button4_8_1.Bind(wx.EVT_BUTTON,self.buttonclick4_3_1)
        self.button4_8_2.Bind(wx.EVT_BUTTON,self.buttonclick4_3_2)
        self.button4_8_3.Bind(wx.EVT_BUTTON,self.buttonclick4_3_3)
        self.button5_4.Bind(wx.EVT_BUTTON,self.buttonclick5_1)
        self.button5_8.Bind(wx.EVT_BUTTON,self.buttonclick5_2)
        self.slider6_2.Bind(wx.EVT_SLIDER,self.slider_change6_1)
        self.slider6_3.Bind(wx.EVT_SLIDER,self.slider_change6_2)
        self.button6_4.Bind(wx.EVT_BUTTON,self.buttonclick6_1)
        
        
        
        
        
    def buttonclick1_1(self,event):
        if len(self.textbox1_1.GetValue()) < 11:
            name = self.textbox1_1.GetValue().replace('_','').replace('-','').replace('/','')
        else:
            name = self.textbox1_1.GetValue()[:10].replace('_','').replace('-','').replace('/','')
        user.changeUserName(name)
        self.label1_3_2.SetLabel(user.userName)
        
    def buttonclick1_2(self,event):
        if len(self.textbox1_5.GetValue()) < 11:
            before = self.textbox1_5.GetValue().replace('_','').replace('-','').replace('/','')

        else:
            before = self.textbox1_5.GetValue()[:10].replace('_','').replace('-','').replace('/','') 
        
        if len(self.textbox1_6.GetValue()) < 11:
            after = self.textbox1_6.GetValue().replace('_','').replace('-','').replace('/','')

        else:
            after = self.textbox1_6.GetValue()[:10].replace('_','').replace('-','').replace('/','')
        self.textbox1_5.Clear()
        self.textbox1_6.Clear()
        manager.appendNameList(before,after)
        self.listbox1_8.DeleteAllItems()
        num = 0
        for ls in manager.changeNameList:
            self.listbox1_8.InsertItem(num,str(ls[0]))
            self.listbox1_8.SetItem(num,1,str(ls[1]))
            num += 1

    def buttonclick1_2_2(self,event):
        try:
            if len(manager.changeNameList) > 1:
                if self.listbox1_8.GetFocusedItem() > 0:
                    index = self.listbox1_8.GetFocusedItem()
                    manager.up_Namelist(int(index))
                num = 0
                self.listbox1_8.DeleteAllItems()
                for ls in manager.changeNameList:
                    self.listbox1_8.InsertItem(num,str(ls[0]))
                    self.listbox1_8.SetItem(num,1,ls[1])
                    num += 1      
        except:
            pass
            
            
        
    def buttonclick1_3(self,event):
        try:
            if len(manager.changeNameList) > 0:
                if self.listbox1_8.GetFocusedItem() > -1:
                    index = self.listbox1_8.GetFocusedItem()
                    manager.removeNameList(int(index))
                num = 0
                self.listbox1_8.DeleteAllItems()
                for ls in manager.changeNameList:
                    self.listbox1_8.InsertItem(num,str(ls[0]))
                    self.listbox1_8.SetItem(num,1,ls[1])
                    num += 1
                    
        except:
            pass
                
    def buttonclick1_4(self,event):
        
        if not manager.changeName:
            manager.changeName = True
            self.button1_10.SetLabel('ON')
        elif manager.changeName:
            manager.changeName = False
            self.button1_10.SetLabel('OFF')
            
    def buttonclick1_5(self,event):
        if manager.R > 128:
            self.button1_11.SetLabel("背景緑")
            manager.changeGreen()
        else:
            self.button1_11.SetLabel("背景白")
            manager.changeWhite()        
        
    def buttonclick2_1(self,evemt):
        getid = False
        getname = False
        
        if len(self.textbox2_2.GetValue()) < 11 and len(self.textbox2_2.GetValue()) > 0:
            cid = str(self.textbox2_2.GetValue()).replace('_','').replace('-','').replace('/','')
            getid = True
        elif len(self.textbox2_2.GetValue()) > 0:
            cid = str(self.textbox2_2.GetValue())[:10].replace('_','').replace('-','').replace('/','')
            getid = True
            
        if len(self.textbox2_3.GetValue()) < 11 and len(self.textbox2_2.GetValue()) > 0:
            cvname = str(self.textbox2_3.GetValue()).replace('_','').replace('-','').replace('/','')
            getname = True
        elif len(self.textbox2_3.GetValue()) > 0:
            cvname = str(self.textbox2_3.GetValue())[:10].replace('_','').replace('-','').replace('/','')
            getname = True
            
        if getid and getname:
            manager.appendVoiceRoid(str(cid),str(cvname))
            manager.startAllVoiceRoid()
            manager.startTachie(str(cvname))
            manager.startJimaku(str(cvname))
            num = 0
            self.listbox2_5.DeleteAllItems()
            for vList in manager.VoiceRoidList:
                self.listbox2_5.InsertItem(num,vList.cv)
                self.listbox2_5.SetItem(num,1,vList.washaName)
                rgb16 = "#" + format(int(vList.Red),'02x') + format(int(vList.Green),'02x') + format(int(vList.Blue),'02x')
                self.listbox2_5.SetItem(num,2,rgb16)
                if vList.vanish:
                    bl = "True"
                else:
                    bl = "False"
                self.listbox2_5.SetItem(num,3,bl)
                num += 1
            
            self.textbox2_2.Clear()
            self.textbox2_3.Clear()
      
            
    def buttonclick2_2(self,event):
        if self.listbox2_5.GetFocusedItem() > -1 and str.isdecimal(self.textbox2_7_1.GetValue()) and str.isdecimal(self.textbox2_7_2.GetValue()) and str.isdecimal(self.textbox2_7_3.GetValue()):
            if int(self.textbox2_7_1.GetValue()) < 256 and int(self.textbox2_7_1.GetValue()) < 256 and int(self.textbox2_7_1.GetValue()) < 256:
                num = self.listbox2_5.GetFocusedItem()
                manager.changeRGB2(num,int(self.textbox2_7_1.GetValue()),int(self.textbox2_7_2.GetValue()),int(self.textbox2_7_3.GetValue()))
                num = 0
                self.listbox2_5.DeleteAllItems()
                for vList in manager.VoiceRoidList:
                    self.listbox2_5.InsertItem(num,vList.cv)
                    self.listbox2_5.SetItem(num,1,vList.washaName)
                    rgb16 = "#" + format(int(vList.Red),'02x') + format(int(vList.Green),'02x') + format(int(vList.Blue),'02x')
                    self.listbox2_5.SetItem(num,2,rgb16)
                    if vList.vanish:
                        bl = "True"
                    else:
                        bl = "False"
                    self.listbox2_5.SetItem(num,3,bl)
                    num += 1
                    
    def buttonclick2_3(self,event):
        index = self.listbox2_5.GetFocusedItem()
        if int(index) > -1:
            manager.vanish_change(index)
            num = 0
            self.listbox2_5.DeleteAllItems()
            for vList in manager.VoiceRoidList:
                self.listbox2_5.InsertItem(num,vList.cv)
                self.listbox2_5.SetItem(num,1,vList.washaName)
                rgb16 = "#" + format(int(vList.Red),'02x') + format(int(vList.Green),'02x') + format(int(vList.Blue),'02x')
                self.listbox2_5.SetItem(num,2,rgb16)
                if vList.vanish:
                    bl = "True"
                else:
                    bl = "False"
                self.listbox2_5.SetItem(num,3,bl)
                num += 1

    def slider_change2_1(self,event):
        obj = event.GetEventObject()
        manager.changeLagTime(int(obj.GetValue()))
        
    def buttonclick3_1_1(self,event):
        getwasha = False
        getmae = False
        getato = False
        
        if len(self.textbox3_2_1.GetValue().replace('/','').replace('_','').replace('-','')) < 11 and len(self.textbox3_2_1.GetValue().replace('/','').replace('_','').replace('-','')) > 0:
            washa = self.textbox3_2_1.GetValue().replace('/','').replace('_','').replace('-','')
            getwasha = True
            
        if len(self.textbox3_2_2.GetValue().replace('/','').replace('_','').replace('-','')) > 0:
            mae = self.textbox3_2_2.GetValue().replace('/','').replace('_','').replace('-','')
            getmae = True
            
        if len(self.textbox3_2_3.GetValue().replace('/','').replace('_','').replace('-','')) > 0:
            ato = self.textbox3_2_3.GetValue().replace('/','').replace('_','').replace('-','')
            getato = True
            
        if getwasha and getmae and getato:
            manager.appendReWriteList(washa,mae,ato)
            self.listbox3_4.DeleteAllItems()
            num = 0
            for ls in manager.rewriteList:
                self.listbox3_4.InsertItem(num,str(ls[2]))
                self.listbox3_4.SetItem(num,1,str(ls[0]))
                self.listbox3_4.SetItem(num,2,str(ls[1]))
                num += 1
            self.textbox3_2_1.Clear()
            self.textbox3_2_2.Clear()
            self.textbox3_2_3.Clear()
            
    def buttonclick3_1_2(self,event):
        if self.listbox3_4.GetFocusedItem() > -1:
            manager.removeReWriteList(int(self.listbox3_4.GetFirstSelected()))
            self.listbox3_4.DeleteAllItems()
            num = 0
            for ls in manager.rewriteList:
                self.listbox3_4.InsertItem(num,str(ls[2]))
                self.listbox3_4.SetItem(num,1,str(ls[0]))
                self.listbox3_4.SetItem(num,2,str(ls[1]))
                num += 1
                
    def buttonclick3_1_3(self,event):
        manager.save_rewrite_list_to_csv()
        
    def buttonclick3_1_4(self,event):
        manager.get_rewrite_list_for_csv()
        self.listbox3_4.DeleteAllItems()
        num = 0
        for ls in manager.rewriteList:
            self.listbox3_4.InsertItem(num,str(ls[2]))
            self.listbox3_4.SetItem(num,1,str(ls[0]))
            self.listbox3_4.SetItem(num,2,str(ls[1]))
            num += 1
            
    def buttonclick3_2_1(self,event):
        getwasha = False
        getmae = False
        getato = False
        
        if len(self.textbox3_6_1.GetValue().replace('/','').replace('_','').replace('-','')) < 11 and len(self.textbox3_6_1.GetValue().replace('/','').replace('_','').replace('-','')) > 0:
            washa = self.textbox3_2_1.GetValue().replace('/','').replace('_','').replace('-','')
            getwasha = True
            
        if len(self.textbox3_6_2.GetValue().replace('/','').replace('_','').replace('-','')) > 0:
            mae = self.textbox3_6_2.GetValue().replace('/','').replace('_','').replace('-','')
            getmae = True
            
        if len(self.textbox3_6_3.GetValue().replace('/','').replace('_','').replace('-','')) > 0:
            ato = self.textbox3_6_3.GetValue().replace('/','').replace('_','').replace('-','')
            getato = True
            
        if getwasha and getmae and getato:
            manager.appendRelaceList(washa,mae,ato)
            self.listbox3_8.DeleteAllItems()
            num = 0
            for ls in manager.replaceList:
                self.listbox3_8.InsertItem(num,str(ls[2]))
                self.listbox3_8.SetItem(num,1,str(ls[0]))
                self.listbox3_8.SetItem(num,2,str(ls[1]))
                num += 1
            self.textbox3_6_1.Clear()
            self.textbox3_6_2.Clear()
            self.textbox3_6_3.Clear()
            
    def buttonclick3_2_2(self,event):
        if self.listbox3_8.GetFocusedItem() > -1:
            manager.removeReplaceList(int(self.listbox3_8.GetFocusedItem()))
            self.listbox3_8.DeleteAllItems()
            num = 0
            for ls in manager.replaceList:
                self.listbox3_8.InsertItem(num,str(ls[2]))
                self.listbox3_8.SetItem(num,1,str(ls[0]))
                self.listbox3_8.SetItem(num,2,str(ls[1]))
                num += 1
                
    def buttonclick3_2_3(self,event):
        manager.save_replace_list_to_csv()
        
    def buttonclick3_2_4(self,event):
        manager.get_replace_list_for_csv()
        self.listbox3_8.DeleteAllItems()
        num = 0
        for ls in manager.replaceList:
            self.listbox3_8.InsertItem(num,str(ls[2]))
            self.listbox3_8.SetItem(num,1,str(ls[0]))
            self.listbox3_8.SetItem(num,2,str(ls[1]))
            num += 1
            
    def buttonclick4_1(self,event):
        if str.isdecimal(self.textbox4_2.GetValue()) and str.isdecimal(self.textbox4_4.GetValue()):
            num = self.textbox4_2.GetValue()
            r = self.textbox4_4.GetValue()
            getp = user.getBotton(int(num),int(r))
            self.listbox4_7.DeleteAllItems()
            num = 0
            for ls in user.changePosition:
                if int(ls[0]) == 0:
                    self.listbox4_7.InsertItem(num,"mouse")
                    self.listbox4_7.SetItem(num,1,str(ls[1]))
                    self.listbox4_7.SetItem(num,2,"x = " + str(ls[2]) + " y = " + str(ls[3]) + " R = " + str(ls[4]))
                elif int(ls[0]) == 1:
                    self.listbox4_7.InsertItem(num,"key")
                    self.listbox4_7.SetItem(num,1,str(ls[1]))
                    self.listbox4_7.SetItem(num,2,str(ls[2]))
                num += 1
                    
    def buttonclick4_2(self,event):
        if str.isdecimal(self.textbox4_2.GetValue()):
            num = self.textbox4_2.GetValue()
            get_key = user.getKey(int(num))
            self.listbox4_7.DeleteAllItems()
            num = 0
            for ls in user.changePosition:
                if int(ls[0]) == 0:
                    self.listbox4_7.InsertItem(num,"mouse")
                    self.listbox4_7.SetItem(num,1,str(ls[1]))
                    self.listbox4_7.SetItem(num,2,"x = " + str(ls[2]) + " y = " + str(ls[3]))
                elif int(ls[0]) == 1:
                    self.listbox4_7.InsertItem(num,"key")
                    self.listbox4_7.SetItem(num,1,str(ls[1]))
                    self.listbox4_7.SetItem(num,2,str(ls[2]))
                num += 1
                    
    def buttonclick4_3_1(self,event):
        index = self.listbox4_7.GetFocusedItem()
        if int(index) > -1:
            user.removeCommandList(index)
            num = 0
            self.listbox4_7.DeleteAllItems()
            for ls in user.changePosition:
                if int(ls[0]) == 0:
                    self.listbox4_7.InsertItem(num,"mouse")
                    self.listbox4_7.SetItem(num,1,str(ls[1]))
                    self.listbox4_7.SetItem(num,2,"x = " + str(ls[2]) + " y = " + str(ls[3]))
                elif int(ls[0]) == 1:
                    self.listbox4_7.InsertItem(num,"key")
                    self.listbox4_7.SetItem(num,1,str(ls[1]))
                    self.listbox4_7.SetItem(num,2,str(ls[2]))
                num += 1
                
    def buttonclick4_3_2(self,event):
        user.save_command_list_to_csv()
        
    def buttonclick4_3_3(self,event):
        user.get_command_list_for_csv()
        num = 0
        self.listbox4_7.DeleteAllItems()
        for ls in user.changePosition:
            if int(ls[0]) == 0:
                self.listbox4_7.InsertItem(num,"mouse")
                self.listbox4_7.SetItem(num,1,str(ls[1]))
                self.listbox4_7.SetItem(num,2,"x = " + str(ls[2]) + " y = " + str(ls[3]))
            elif int(ls[0]) == 1:
                self.listbox4_7.InsertItem(num,"key")
                self.listbox4_7.SetItem(num,1,str(ls[1]))
                self.listbox4_7.SetItem(num,2,str(ls[2]))
            num += 1
                
    def buttonclick5_1(self,event):
        if len(self.textbox5_2.GetValue()) > 10 and len(self.textbox5_3.GetValue()) == 8:
            try:
                dis.set_discord(self.textbox5_2.GetValue(),self.textbox5_3.GetValue())
                dis.start_threading_discord()
                self.label5_7_2.SetLabel(self.textbox5_3.GetValue())
                self.textbox5_2.Clear()
                self.textbox5_3.Clear()
            
            except:
                pass
    def buttonclick5_2(self,event):
        if cmdmaker.shot:
            cmdmaker.shot = False
        else:
            cmdmaker.shot = True
        if cmdmaker.shot:
            self.button5_8.SetLabel("ON")
        else:
            self.button5_8.SetLabel("OFF")
            
    def slider_change6_1(self,event):
        obj = event.GetEventObject()
        user.changeMaxV(int(obj.GetValue()))
        
    def slider_change6_2(self,event):
        obj = event.GetEventObject()
        user.changeMiniV(int(obj.GetValue()))
        
    def buttonclick6_1(self,event):
        if user.mute:
            user.mute = False
            self.button6_4.SetLabel("OFF")
        else:
            user.mute = True
            self.button6_4.SetLabel("ON")
            
    def inputIDandNAMEindis(self,uname,uid):
        self.label5_5_2.SetLabel(str(uname))
        self.label5_6_2.SetLabel(str(uid))


app = wx.App()
ex = MyFrame(None, title='ぼいろらいぶ(仮)')
ex.Show(True)

def main():
    app.MainLoop()

if __name__ == '__main__':
    main()
    userClass.userClass_threading_OFF_flag = True
    voiceRoidManager.voiceRoidManager_threading_OFF_flag = True
    cmdmaker.cmdmaker_threading_OFF_flag = True