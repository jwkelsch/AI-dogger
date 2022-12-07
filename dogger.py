from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import time
import random
from playsound import playsound
import threading
#import vlc
#import multiprocessing
#from multiprocess import Process #pip install multiprocess   
#from multiprocessing import Process
from threading import Thread
from functools import partial

#mode 1 = AI mode
#mode 2 = base game mode
mode = 1

class Bot:
    def __init__(self, boneGot, safe, pos, carline, accel):
        self.boneGot = boneGot
        self.safe = safe   # [0,0,0,0,0]
        self.pos = pos
        self.carline = carline
        self.accel = accel
    def findBoneDistance(self, currPos, bonePos):
        posDiff = currPos - bonePos
        if posDiff != 0:
            return posDiff
    def findBoneLR(self, posDiff):
        if posDiff < 0:
            direction = "right"
        if posDiff > 0: 
            direction = "left"
        return direction
    def moveToBone(self, posDiff, direction):
        AIBot.pos = dogPlayer.getDogPos()
        amountMove = abs(posDiff)
        if direction == "right":
            AIBot.pos = dogPlayer.getDogPos()
            while amountMove > 0:
                #dogPlayer.forceRight()
                #dogPlayer.setDog(dogPlayer.getDogPos()+1)
                goRight()
                AIBot.pos = dogPlayer.getDogPos()
                updateDoglbl()
                time.sleep(.02)
                amountMove = amountMove - 1
            AIBot.boneGot = True
            print("got bone")
            AIBot.pos = dogPlayer.getDogPos()
        if direction == "left":
            AIBot.pos = dogPlayer.getDogPos()
            while amountMove > 0:
                #dogPlayer.forceLeft()
                #dogPlayer.setDog(dogPlayer.getDogPos()-1)
                goLeft()
                AIBot.pos = dogPlayer.getDogPos()
                updateDoglbl()
                time.sleep(.02)
                amountMove = amountMove - 1
            AIBot.boneGot = True
            print("got bone")
            AIBot.pos = dogPlayer.getDogPos()


    def moveToSafeSpot(self): 
        if AIBot.accel == "veryfast":
            time.sleep(.06)
        if AIBot.accel == "slow" or AIBot.accel == "med" or AIBot.accel == "fast":
            time.sleep(.1)
        #time.sleep(.1)
        AIBot.pos = dogPlayer.getDogPos()
        carLine = AIBot.carline
        if carLine[AIBot.pos] == 0:
            AIBot.safe = True # dont need to move
            print("safe - DONT NEED TO MOVE")
            return "safe"

        #goes to CLOSEST safe spot (mimics human)
        AIBot.pos = dogPlayer.getDogPos()
        safeSpotFound = False
        adjcounter = 1
        while safeSpotFound == False:
            #check if OOB 
            if AIBot.pos + adjcounter <= 4:  #not OOB for go right
                if carLine[AIBot.pos + adjcounter] == 0:
                    #go right
                    while adjcounter > 0:
                        goRight()
                        AIBot.pos = dogPlayer.getDogPos()
                        updateDoglbl()
                        adjcounter = adjcounter - 1
                        time.sleep(.02)
                    AIBot.safe = True
                    safeSpotFound = True
                    print("safe")
                    return "safe"
            if AIBot.pos - adjcounter >= 0: #not OOB for go left
                if carLine[AIBot.pos - adjcounter] == 0:
                    #go left
                    while adjcounter > 0:
                        goLeft()
                        AIBot.pos = dogPlayer.getDogPos()
                        updateDoglbl()
                        adjcounter = adjcounter - 1
                        time.sleep(.02)
                    AIBot.safe = True
                    safeSpotFound = True
                    print("safe")
                    return "safe"
            adjcounter = adjcounter + 1
            
            


def AIBotThread(): #communicate to main thread through AI bot class that main thread passes data to - class pseudo simple neural network - teach to process data accordingly
    time.sleep(.1)
    while dogPlayer.done == False:
        #print("test")
        #time.sleep(2)
        AIBot.pos = dogPlayer.getDogPos()
        currPos = AIBot.pos 
        while AIBot.boneGot == False:
            #find bone
            bonePos = dogPlayer.getBonePos()
            posDiff = AIBot.findBoneDistance(currPos, bonePos)
            direction = AIBot.findBoneLR(posDiff)
            AIBot.moveToBone(posDiff, direction)
        while AIBot.safe == False:
            #get to safe spot
            time.sleep(.5)
            AIBot.moveToSafeSpot()
            print("--thread flags done--")
            #reset to false when last iteration in main game/reset row on top, bonegot/safe
            

class Dog:
    def __init__(self, posi, done):
        self.pos = posi
        self.bonePos = 0
        self.done = False
    def setDog(self, val):
        self.pos = val
    def getDogPos(self):
        return self.pos
    def calcBonePos(self):
        possibleColumn = [0,1,2,3,4]
        bonePos = random.choice(possibleColumn)
        self.bonePos = bonePos
        return bonePos
    def getBonePos(self):
        return self.bonePos
    def neutralizeBonePos(self):
        self.bonePos = 20
    def setDone(self):
        self.done = True

#--------------------------------------------------------------
def virtualInputDisplayThread(): 
    while dogPlayer.done == False:
        while LRinputs.statusL == True:
            unhighlightLarrow()
        while LRinputs.statusR == True:
            unhighlightRarrow()

class adaptiveInputs:
    def __init__(self, statusR, statusL):
        self.statusR = statusR
        self.statusL = statusL
#--------------------------------------------------------------

def closeWindow(e):
    global window
    window.destroy()
    dogPlayer.setDone()

def updateDoglbl():
    lblDog.grid(row=5, column = AIBot.pos)

def goLeft():
    dPos = dogPlayer.getDogPos()
    #print('d = ',dPos)
    if dPos>0:
        dogPlayer.setDog(dPos-1)
        dPos = dPos-1
        lblDog.grid(row=5, column = dPos)
        Llabel.configure(image=LlabelGreen)
        LRinputs.statusL = True
        print('left')
        #print('current column: ', dPos) 

def goRight():
    dPos = dogPlayer.getDogPos()
    #print('d = ',dPos)
    if dPos<4:
        dogPlayer.setDog(dPos+1)
        dPos = dPos+1
        lblDog.grid(row=5, column = dPos)
        Rlabel.configure(image=RlabelGreen)
        LRinputs.statusR = True
        print('right')
        #print('current column: ', dPos)  

#bind left right arrow keys on keyboard
def any_keypress(event):
    currDog = dogPlayer.getDogPos()
    if event.keysym == 'Right':
        if currDog<4:
            dogPlayer.setDog(currDog+1)
            currDog = currDog+1
            lblDog.grid(row=5, column=currDog)
            Rlabel.configure(image=RlabelGreen)
            LRinputs.statusR = True
    if event.keysym == "Left":
        if currDog>0:
            dogPlayer.setDog(currDog-1)
            currDog = currDog-1
            lblDog.grid(row=5, column=currDog)
            Llabel.configure(image=LlabelGreen)
            LRinputs.statusL = True
    if event.keysym == "Escape":
        window.destroy()
        #AIThread.join()
        #vThread.join()
            
def unhighlightRarrow():
    #print("in unhighlight R")
    time.sleep(.05)
    Rlabel.configure(image=RlabelBlank)
    LRinputs.statusR = False

def unhighlightLarrow():
    #print("in unhighlight L")
    time.sleep(.05)
    Llabel.configure(image=LlabelBlank)
    LRinputs.statusL = False
#--------------------------------------------------------------
#object instantiations
LRinputs = adaptiveInputs(False, False)
dogPlayer = Dog(2, False) 
AIBot = Bot(False, False, 2, [0, 0, 0, 0, 0], "slow")
#--------------------------------------------------------------

#main game thread, game logic and function definitions
#create window
window = tk.Tk()
window.bind_all('<Key>', any_keypress) #bind keypresses to window and function defined above
window.attributes("-topmost", True)
# window.lift()
# window.focus_force()
# window.focus_set()
window.bind('<Escape>', lambda e: closeWindow(e))
window.geometry('1000x600')
window.title("Dogger: Not Frogger")
window.grid_columnconfigure(0, weight=1, uniform="key")
window.grid_columnconfigure(1, weight=1, uniform="key")
window.grid_columnconfigure(2, weight=1, uniform="key")
window.grid_columnconfigure(3, weight=1, uniform="key")
window.grid_columnconfigure(4, weight=1, uniform="key")
window.grid_rowconfigure(2, weight=1, uniform="key")
window.grid_rowconfigure(3, weight=1, uniform="key")
window.grid_rowconfigure(4, weight=1, uniform="key")
window.grid_rowconfigure(5, weight=1, uniform="key")
score = 0
lblInstrucs = tk.Label(window, text = "DOGE THE CARS!! (use buttons or Left/Right arrow keys to play")
lblLine0 = tk.Label(window, text = "*SCORE: "+ str(score) + "*")

#dog image manipulation
imgDog = Image.open('assets/dog.png')
newdog = imgDog.resize((100, 50))
imgDog2 = ImageTk.PhotoImage(newdog)
lblDog = tk.Label(window, image=imgDog2)

# append elements to grid
lblInstrucs.grid(row=0, column=0, columnspan=5)
lblLine0.grid(row=1, column=0, columnspan=5)
lblDog.grid(row=5, column = 2)


#make / append adaptive LR button labels
imgRlabel = Image.open('assets/RarrowBlank.png')
newRlabel = imgRlabel.resize((80, 50))
RlabelBlank = ImageTk.PhotoImage(newRlabel)
Rlabel = Label(window, image=RlabelBlank)
Rlabel.grid(row=7, column =3)

imgLlabel = Image.open('assets/LarrowBlank.png')
newLlabel = imgLlabel.resize((80, 50))
LlabelBlank = ImageTk.PhotoImage(newLlabel)
Llabel = Label(window, image=LlabelBlank)
Llabel.grid(row=7, column =1)

#prep highlight arrow images
imgRlabel = Image.open('assets/RarrowGreen.png')
newRlabel = imgRlabel.resize((80, 50))
RlabelGreen = ImageTk.PhotoImage(newRlabel)

imgLlabel = Image.open('assets/LarrowGreen.png')
newLlabel = imgLlabel.resize((80, 50))
LlabelGreen = ImageTk.PhotoImage(newLlabel)

#UI button clicks definitions - if not playing with arrow keys - add to grid
button1 = Button(window, text="<-", command=goLeft)
button1.grid(row=6, column=1)
button2 = Button(window, text="->", command=goRight)
button2.grid(row=6, column=3)
#rows 2-5       5 being where dog stays

#image creation and labeling
img1 = Image.open('assets/flintstones.png')
newcar = img1.resize((100,50))
img2 = ImageTk.PhotoImage(newcar)
lblCar = tk.Label(window, image=img2)

fzero = Image.open('assets/blueFalcon.jpg')
newFzero = fzero.resize((100,50))
fzero2 = ImageTk.PhotoImage(newFzero)
lblFzero = tk.Label(window, image=fzero2)

batMobile = Image.open('assets/batmobile.jpg')
newbatMobile = batMobile.resize((100,50))
batMobile2 = ImageTk.PhotoImage(newbatMobile)
lblbatMobile = tk.Label(window, image=batMobile2)

mysMachine = Image.open('assets/mysteryMachine.jpg')
newMysMachine = mysMachine.resize((100,50))
mysMachine2 = ImageTk.PhotoImage(newMysMachine)
lblMysMachine = tk.Label(window, image=mysMachine2)

explode = Image.open('assets/explodeImage.jpg')
newExplode = explode.resize((600,400))
explode2 = ImageTk.PhotoImage(newExplode)
lblExplode = tk.Label(window, image=explode2)

bone = Image.open('assets/bone.png')
newBone = bone.resize((100,50))
bone2 = ImageTk.PhotoImage(newBone)
lblBone = tk.Label(window, image=bone2)

plus5 = Image.open('assets/plus5.png')
newPlus5 = plus5.resize((100,50))
pls5 = ImageTk.PhotoImage(newPlus5)
lblPlus5 = tk.Label(window, image=pls5)
 #--------------------------------------------------------------  THREADS
#start AI thread if mode selected
if mode == 1:
    AIThread = Thread(target=partial(AIBotThread))
    AIThread.start()

#vThread = Thread(target=partial(virtualInputDisplayThread))
#vThread.start()
#--------------------------------------------------------------

#main game recursive time looping function
def Advance(carLine, iteration, fasterIteration, score):
    #check if ate bone
    dogPos = dogPlayer.getDogPos()
    bonePos = dogPlayer.getBonePos()
    lblPlus5.grid_forget()
    if dogPos == bonePos:
        #print("GOT BONE")
        woof = threading.Thread(target=playsound, args=('assets/trimmedWoof.wav',), daemon=True)
        woof.start()
        dogPlayer.neutralizeBonePos()
        lblBone.grid_forget()
        score = score + 5
        lblPlus5.grid(row=1, column=3)

    #iteration based game logic - # of rows cars have moved down
    #check if collision happened
    if iteration == 4:
        for y in range (5):
            if carLine[y] == 1:
                if y == dogPlayer.getDogPos():
                    #exit()
                    #song.stop() 
                    lblCar.grid_forget()
                    lblFzero.grid_forget()
                    lblbatMobile.grid_forget()
                    lblMysMachine.grid_forget()
                    lblDog.grid_forget()
                    lblExplode.grid(row=3, column=y, rowspan=3, columnspan=3)
                    threading.Thread(target=playsound, args=('assets/explode.wav',), daemon=True).start()
                    button1.grid_forget()
                    button2.grid_forget()
                    window.unbind_all('<Key>')
                    dogPlayer.done = True
                    dogPlayer.setDone()
                    return
        lblCar.grid_forget()
        lblFzero.grid_forget()
        lblbatMobile.grid_forget()
        lblMysMachine.grid_forget()
        carLine = [0,0,0,0,0]
        iteration = iteration - 4
        

    #generate bone 
    if iteration == 0:
        #dogbone
        bonePos = dogPlayer.calcBonePos()
        dogPos = dogPlayer.getDogPos()
        while bonePos == dogPos:
            bonePos = dogPlayer.calcBonePos()
        lblBone.grid(row=5, column = bonePos)

        #ai bot find bone
        if mode == 1: ################################################################## reset flags here
            
            AIBot.boneGot = False
            time.sleep(.005)        # have to microsleep here to make sure bonemovement happens first in thread (whole thread looping constantly - need to hit right conditional at appropriate time)
            AIBot.safe = False
            # AIThread = Thread(target=partial(AIBotThread))
            # AIThread.start()



        #init top row, car line
        possibleNumCars  = [2,3,4]
        numCars = random.choice(possibleNumCars)
        possibleColumn = [0,1,2,3,4]
        sample = random.sample(possibleColumn, 4)

        if numCars==2:
            col = sample[0]
            col2 = sample[1]
            lblCar.grid(row=2, column=col)
            carLine[col] = 1
            lblFzero.grid(row=2, column=col2)
            carLine[col2] = 1
        if numCars==3:
            col = sample[0]
            col2 = sample[1]
            col3 = sample[2]
            lblCar.grid(row=2, column=col)
            carLine[col] = 1
            lblFzero.grid(row=2, column=col2)
            carLine[col2] = 1
            lblbatMobile.grid(row=2, column=col3)
            carLine[col3] = 1
        if numCars==4:
            col = sample[0]
            col2 = sample[1]
            col3 = sample[2]
            col4 = sample[3]
            lblCar.grid(row=2, column=col)
            carLine[col] = 1
            lblFzero.grid(row=2, column=col2)
            carLine[col2] = 1
            lblbatMobile.grid(row=2, column=col3)
            carLine[col3] = 1
            lblMysMachine.grid(row=2, column=col4)
            carLine[col4] = 1

        #pass car line into bot at appropriate refresh in the game logic
        AIBot.carline = carLine

#init 2nd row (row 3)
    if iteration == 1: 
        lblCar.grid_forget()
        lblFzero.grid_forget()
        lblbatMobile.grid_forget()
        lblMysMachine.grid_forget()
        count = 0
        for y in range (5):
            if carLine[y] == 1:
                if count == 0:
                    lblCar.grid(row=3, column=y)
                if count == 1:
                    lblFzero.grid(row=3, column=y)
                if count == 2:
                    lblbatMobile.grid(row=3, column=y)
                if count == 3:
                    lblMysMachine.grid(row=3, column=y)
                count = count + 1
#init 3rd row 
    if iteration == 2: 
        lblCar.grid_forget()
        lblFzero.grid_forget()
        lblbatMobile.grid_forget()
        lblMysMachine.grid_forget()
        count = 0
        for y in range (5):
            if carLine[y] == 1:
                if count == 0:
                    lblCar.grid(row=4, column=y)
                if count == 1:
                    lblFzero.grid(row=4, column=y)
                if count == 2:
                    lblbatMobile.grid(row=4, column=y)
                if count == 3:
                    lblMysMachine.grid(row=4, column=y)
                count = count + 1
#init 4th row 
    if iteration == 3: 
        lblCar.grid_forget()
        lblFzero.grid_forget()
        lblbatMobile.grid_forget()
        lblMysMachine.grid_forget()
        lblBone.grid_forget()
        count = 0
        for y in range (5):
            if carLine[y] == 1:
                if count == 0:
                    lblCar.grid(row=5, column=y)
                if count == 1:
                    lblFzero.grid(row=5, column=y)
                if count == 2:
                    lblbatMobile.grid(row=5, column=y)
                if count == 3:
                    lblMysMachine.grid(row=5, column=y)
                count = count + 1
    
    #increment interation, score, and acceleration appropriately
    iteration = iteration + 1
    #print(iteration)
    score = score +1
    lblLine0 = tk.Label(window, text = "*SCORE: "+ str(score) + "*")
    lblLine0.grid(row=1, column=0, columnspan=5)
    #speed up game over time
    fasterIteration = fasterIteration + 1 # by 5
    if fasterIteration<12:
        window.after(600, Advance, carLine, iteration, fasterIteration, score)
    if fasterIteration>=12 and fasterIteration<24: #and
        AIBot.accel = "med"
        window.after(500, Advance, carLine, iteration, fasterIteration, score)
    if fasterIteration>=24 and fasterIteration<36:
        AIBot.accel = "fast"
        window.after(300, Advance, carLine, iteration, fasterIteration, score)
    if fasterIteration>=36:
        AIBot.accel = "veryfast"
        window.after(200, Advance, carLine, iteration, fasterIteration, score)
#-------------------------------------------------------------------------------------------

#default vars before Advance() loop is called
carLine = [0,0,0,0,0]
iteration = 0
fasterIteration = 0
Advance(carLine, iteration, fasterIteration, score)


#tkinter window/root mainloop end
window.mainloop()
