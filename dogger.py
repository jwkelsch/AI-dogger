
#if time is super fast, dont go for bones further than 2? spaces - for AI
#tell bot to wait on bone for certain amount of time depending on time cycle?
#func at top of advance() - determine where AI to go, how many spaces left right fr bone, one space at a time move, the move to safe space b4 rest of func happens
#multithread bone get detection?
#def specific goleft goright funcs for AI to use - time delays and such - find bone/safespot func as well
#listener for object property? (bone) - 
#separate entity for AI - talk to each other - communicate to one another

from gettext import dpgettext
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import time
import random
from playsound import playsound
import threading
import vlc
import multiprocessing

from threading import Thread
from functools import partial


#print("AI (1) or nonAI (2) mode: ")
#mode = int(input())
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
        print(currPos, bonePos)
        print("posdiff", posDiff)
        if posDiff != 0:
            return posDiff
    def findBoneLR(self, posDiff):
        print("posdiff", posDiff)
        if posDiff < 0:
            direction = "right"
        if posDiff > 0: 
            direction = "left"
        return direction
    def moveToBone(self, posDiff, direction):
        AIBot.pos = doggy.getDogPos()
        amountMove = abs(posDiff)
        print("AMOUNTMVOE", amountMove)
        if direction == "right":
            AIBot.pos = doggy.getDogPos()
            while amountMove > 0:
                print("in r loop")
                #doggy.forceRight()
                #doggy.setDog(doggy.getDogPos()+1)
                goRight()
                AIBot.pos = doggy.getDogPos()
                updateDoglbl()
                time.sleep(.02)
                amountMove = amountMove - 1
            AIBot.boneGot = True
            AIBot.pos = doggy.getDogPos()
        if direction == "left":
            AIBot.pos = doggy.getDogPos()
            while amountMove > 0:
                print(("in L loop"))
                #doggy.forceLeft()
                #doggy.setDog(doggy.getDogPos()-1)
                goLeft()
                AIBot.pos = doggy.getDogPos()
                updateDoglbl()
                time.sleep(.02)
                amountMove = amountMove - 1
            AIBot.boneGot = True
            print("END OF BONEGET - doggyget", doggy.getDogPos())
            AIBot.pos = doggy.getDogPos()


    def moveToSafeSpot(self): #TODO try to get this to go to nearest safe spot instead of first 1 in search - split() carline on aiPos?
        if AIBot.accel == "veryfast":
            time.sleep(.06)
        if AIBot.accel == "slow" or AIBot.accel == "med" or AIBot.accel == "fast":
            time.sleep(.1)
        #time.sleep(.1)
        AIBot.pos = doggy.getDogPos()
        carLine = AIBot.carline
        print("---")
        print("current pos", AIBot.pos)
        print("current carLine", carLine)
        print("---")
        if carLine[AIBot.pos] == 0:
            AIBot.safe = True # dont need to move
            print("safe - DONT NEED TO MOVE")
            return "safe"
        index = 0
        for x in carLine:
            if x == 0:
                print(x)
                if index < AIBot.pos:
                    #go left
                    while index < AIBot.pos:
                        goLeft()
                        AIBot.pos = doggy.getDogPos()
                        updateDoglbl()
                        time.sleep(.02)
                    AIBot.safe = True
                    print("safe")
                    return "safe"
                if index > AIBot.pos:
                    while index > AIBot.pos:
                        goRight()
                        AIBot.pos = doggy.getDogPos()
                        updateDoglbl()
                        time.sleep(.02)
                    AIBot.safe = True
                    print("safe")
                    return "safe"
            index = index + 1
        AIBot.safe = True


        
            



def AIBotThread(): #communicate to main thread through AI bot class that main thread passes data to -- #third thread for UI? -- class pseudo simple neural network - teach to process data accordingly
    time.sleep(.1)
    while doggy.done == False:
        #print("test")
        #time.sleep(2)
        AIBot.pos = doggy.getDogPos()
        currPos = AIBot.pos 
        while AIBot.boneGot == False:
            #find bone
            bonePos = doggy.getBonePos()
            print("**********", currPos, bonePos)
            posDiff = AIBot.findBoneDistance(currPos, bonePos)
            print ("posdif", posDiff)
            direction = AIBot.findBoneLR(posDiff)
            AIBot.moveToBone(posDiff, direction)
            print("bonegot", AIBot.boneGot)
        while AIBot.safe == False:
            #get to safe spot
            #AIBot.safe = True
            time.sleep(.5)
            # if AIBot.accel == "slow":
            #     time.sleep(.5) #change based on accel
            # if AIBot.accel == "med":
            #     time.sleep(.4)
            # if AIBot.accel == "fast":
            #     time.sleep(.3)
            # if AIBot.accel == "veryfast":
            #     time.sleep(.2)
            AIBot.moveToSafeSpot()
            print("thread flags done")
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
 

doggy = Dog(2, False) 

AIBot = Bot(False, False, 2, [0, 0, 0, 0, 0], "slow")








def closeWindow(e):
    global window
    window.destroy()
    doggy.setDone()
    #AIThread.join()
    #vThread.join()




#main game thread, game logic and function definitions
#def mainGameThread():
#create window
window = tk.Tk()
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

imgDog = Image.open('assets/dog.png')
newdog = imgDog.resize((100, 50))
imgDog2 = ImageTk.PhotoImage(newdog)
lblDog = tk.Label(window, image=imgDog2)

# append elements to grid
lblInstrucs.grid(row=0, column=0, columnspan=5)
lblLine0.grid(row=1, column=0, columnspan=5)
lblDog.grid(row=5, column = 2)


def updateDoglbl():
    lblDog.grid(row=5, column = AIBot.pos)

#global currCol
#currCol = 2

#update dog label thread - have to start here as well to have acess to window variables
# def updateWindowThread():
#     while doggy.done == False:
#         lblDog.grid(row=5, column = AI.AIBot.pos)

# if mode == 1:
#     dogLblThread = Thread(target=partial(updateWindowThread))
#     dogLblThread.start()

#UI button clicks definitions
def goLeft():
    dPos = doggy.getDogPos()
    #print('d = ',dPos)
    if dPos>0:
        doggy.setDog(dPos-1)
        dPos = dPos-1
        lblDog.grid(row=5, column = dPos)
        #print('left')
        #print('current column: ', dPos)
    else:
        print('cant go further left')    

button1 = Button(window, text="<-", command=goLeft)
button1.grid(row=6, column=1)

def goRight():
    dPos = doggy.getDogPos()
    #print('d = ',dPos)
    if dPos<4:
        doggy.setDog(dPos+1)
        dPos = dPos+1
        lblDog.grid(row=5, column = dPos)
        #print('right')
        #print('current column: ', dPos)
    else:
        print('cant go further right')    


button2 = Button(window, text="->", command=goRight)
button2.grid(row=6, column=3)
#rows 2-5       5 being where dog stays

#bind left right arrow keys on keyboard
def any_keypress(event):
    print("in keypress")
    currDog = doggy.getDogPos()
    if event.keysym == 'Right':
        if currDog<4:
            doggy.setDog(currDog+1)
            currDog = currDog+1
            lblDog.grid(row=5, column=currDog)
    if event.keysym == "Left":
        if currDog>0:
            doggy.setDog(currDog-1)
            currDog = currDog-1
            lblDog.grid(row=5, column=currDog)
    if event.keysym == "Escape":
        window.destroy()
        #AIThread.join()
        #vThread.join()
            
window.bind_all('<Key>', any_keypress)



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
    


def testfunc():
    goLeft()

#global woof
#woof = threading.Thread(target=playsound, args=('woof.mp3',), daemon=True)
    
if mode == 1:
    AIThread = Thread(target=partial(AIBotThread))
    AIThread.start()


#main game recursive time looping function
def Advance(carLine, iteration, fasterIteration, score):
# global woof
    #if woof.is_alive:
    #   woof.join()
    #check if ate bone
    dogPos = doggy.getDogPos()
    bonePos = doggy.getBonePos()
    lblPlus5.grid_forget()
    #print("dogpos: ", dogPos)
    #print("bonepos: ", bonePos)
    if dogPos == bonePos:
        print("GOT BONE")
        #woof.start()
        woof = threading.Thread(target=playsound, args=('assets/trimmedWoof.wav',), daemon=True)
        woof.start()
        doggy.neutralizeBonePos()
        lblBone.grid_forget()
        score = score + 5
        #lblLine0 = tk.Label(window, text = "*SCORE: "+ str(score) + "*", image=pls5, compound='center')
        #lblLine0.grid(row=1, column=0, columnspan=5)
        #lblLine0 = tk.Label(window, text = "*SCORE: "+ str(score) + "*")
        #lblLine0.grid_forget()
        lblPlus5.grid(row=1, column=3)
        
        #woof = multiprocessing.Process(target=playsound, args=("woof.mp3",))
    #matrix[0][0] = 0
    #matrix[0][1] = 0
    #matrix[0][2] = 0
    #matrix[0][3] = 0
    #matrix[0][4] = 0
    #lblCar.grid_forget()
    #lblFzero.grid_forget()
    #lblbatMobile.grid_forget()
    if iteration == 4:
        for y in range (5):
            if carLine[y] == 1:
                if y == doggy.getDogPos():
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
                    doggy.done = True
                    doggy.setDone()
                    #time.sleep(1)
                    #window.destroy()
                    #playsound('explode.wav', False)
                    return
        lblCar.grid_forget()
        lblFzero.grid_forget()
        lblbatMobile.grid_forget()
        lblMysMachine.grid_forget()
        carLine = [0,0,0,0,0]
        iteration = iteration - 4
        


    if iteration == 0:
        #dogbone
        bonePos = doggy.calcBonePos()
        dogPos = doggy.getDogPos()
        while bonePos == dogPos:
            bonePos = doggy.calcBonePos()
        lblBone.grid(row=5, column = bonePos)

        #ai bot find bone
        if mode == 1: ################################################################## reset flags here
            
            AIBot.boneGot = False
            time.sleep(.005)        # have to microsleep here to make sure bonemovement happens first in thread (whole thread looping constantly - need to hit right conditional at appropriate time)
            AIBot.safe = False
            # AIThread = Thread(target=partial(AIBotThread))
            # AIThread.start()
 


#init top row
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
    
                




    print(carLine)
    iteration = iteration + 1
    #print(iteration)
    score = score +1
    lblLine0 = tk.Label(window, text = "*SCORE: "+ str(score) + "*")
    lblLine0.grid(row=1, column=0, columnspan=5)

    # if mode == 1:
    #     AIThread.join()

    #speed up game over time
    fasterIteration = fasterIteration + 1 # by 5
    #print("faster: ", fasterIteration)
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
        
    #if fasterIteration<25:
    #  window.after(200, Advance, carLine, iteration, fasterIteration)
#end of advance definition

#threading.Thread(target=playsound, args=('shovelKnightSong.mp3',), daemon=True).start()
#song = vlc.MediaPlayer("shovelKnightSong.mp3")

#song = vlc.MediaPlayer("assets/highway.mp3") 
#song.play()
carLine = [0,0,0,0,0]
iteration = 0
fasterIteration = 0
Advance(carLine, iteration, fasterIteration, score)



window.mainloop()


    

#multithread starts - run in parallel
#gameThread = Thread(target=partial(mainGameThread))
#gameThread.start()



    



#AIThread.join() #find ddifferent way to end threads/whole program
#vThread.join()

# while doggy.done == False:
#     if doggy.done == True:
#         exit()



###################################################################################################################################################################################



    
#AIBot = Bot(False, False, 2)


            



####################################################################################################################################################################

def virtualInputDisplayThread(): #TODO create UI for button inputs/highlights - highlight when call update lbl in AI thread methods -- tkinter widgets?
    while doggy.done == False:
        print("visual comp test thread")          #add extra grid row on bottom? just change picture/label to highlight inputs - could also coordinate with human inputs
        time.sleep(2)



#if AI mode start AI related threads
if mode == 1:
    vThread = Thread(target=partial(virtualInputDisplayThread))
    #vThread.start()

    AIThread = Thread(target=partial(AIBotThread))
    AIThread.start()

    
