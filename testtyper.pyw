from tkinter import *
import time
from pathlib import Path
import math

completed=0
local_wrongkey=0
keytimes=[]
lastkeytime=0
starttime=0
wrongkeys=0
text = open("TestText.txt", "r")
textstr=""
vergleichstext=[]

for line in text:
    textstr+=(line.rstrip())
text.close()

schriftart=('Courier','24')

buchstabe_x=19
buchstabe_y=36

##########################Fensterbreite kann man hier einstellen
breite=1000
##########################

spalten=int(breite/buchstabe_x)
reihen=int(len(textstr)/spalten)+1
hoehe=buchstabe_y*(reihen)
for i in range(reihen-1,0,-1):
    vergleichstext+=[textstr[i*spalten:(i+1)*spalten]]
    textstr=textstr[0:i*spalten]+"\n"+textstr[i*spalten:len(textstr)]
vergleichstext+=[textstr[0*spalten:(0+1)*spalten]]
vergleichstext=vergleichstext[::-1]

textend=[ len(vergleichstext[len(vergleichstext)-1])-1, len(vergleichstext)-1]

for y in range(len(vergleichstext)):
    for x in range(len(vergleichstext[y])):
                   keytimes+=[[vergleichstext[y][x]]]

#---------------------------------------------------

def callback(event):
    global starttime,lastkeytime,keytimes,wrongkeys,local_wrongkey
    if(event.char!=""):
        currenttime=time.time()
        if starttime==0:
            starttime=currenttime
            lastkeytime=currenttime
        lastpressed=event.char
        if(lastpressed==vergleichstext[cursorpos[1]][cursorpos[0]]):
            
            if lastkeytime==0:
                lastkeytime=currenttime

            keytimes[cursorpos[0]+spalten*cursorpos[1]]+=[int(round(currenttime-lastkeytime,3)*1000),local_wrongkey]
            lastkeytime=currenttime
            
            local_wrongkey=0
            entry.create_rectangle(buchstabe_x*cursorpos[0],buchstabe_y*cursorpos[1],buchstabe_x*(cursorpos[0]+1),buchstabe_y*(cursorpos[1]+1),outline="lightgreen",fill="lightgreen",tag="deletable")
            entry.tag_lower("deletable")
            move_cursor()
            entry.itemconfig(cursor,fill="lightgrey")
        else:
            entry.itemconfig(cursor,fill="red")
            wrongkeys+=1
            local_wrongkey+=1
            
def move_cursor():
    global cursorpos
    if textend==cursorpos:
        conclude()
        return
    cursorpos[1]= cursorpos[1] + int((cursorpos[0]+1)/spalten)
    cursorpos[0]=(cursorpos[0]+1)%spalten
    entry.coords(cursor,buchstabe_x*cursorpos[0],buchstabe_y*cursorpos[1],buchstabe_x*(cursorpos[0]+1),buchstabe_y*(cursorpos[1]+1))
    


    
def conclude():
    global starttime,completed
    completed=1
    root.unbind("<Key>")
    zeit=time.time()-starttime
    entry.itemconfig(cursor,state='hidden')
    timelabel.config(text=str(round(zeit,2))+" Sekunden")
#---------------------------
    nr=1
    path="data/results_"
    path2="data\\results_"
    while(Path(path+"0"*(10-int(math.log(nr,10)))+str(nr)+".txt").is_file()):
        nr+=1
    fname=(path2+"0"*(10-int(math.log(nr,10)))+str(nr)+".txt")

    file=open(fname,"w")
    file.write("Gesamtzeit:\t" + str(round(zeit,2))+" Sekunden\n")
    file.write("Zeichenzahl:\t" + str(len(keytimes))+"\n")
    file.write("TpM:\t" + str(round(len(keytimes)/zeit*60,2))+"\n")
    file.write("Fehlerquote:\t" + str(round(wrongkeys*100/(len(keytimes)+wrongkeys),2))+"%\n")
    file.write("Gesamtfehler:\t" + str(wrongkeys)+"\n\n--------------------------------------------------\n")
    for element in keytimes:
        file.write(element[0]+"\t"+str(element[1])+"\t"+str(element[2])+"\n")
    file.close()
#-----------------------------------
def reset():
    global starttime,lastkeytimes,keytimes,wrongkeys,completed
    #---------------------------
    if(completed==0 and len(keytimes[0])==3):
        nr=1
        path="data/results_incomplete_"
        path2="data\\results_incomplete_"
        while(Path(path+"0"*(10-int(math.log(nr,10)))+str(nr)+".txt").is_file()):
            nr+=1
        fname=(path2+"0"*(10-int(math.log(nr,10)))+str(nr)+".txt")

        file=open(fname,"w")
        for element in keytimes:
            if(len(element)==3):
                file.write(element[0]+"\t"+str(element[1])+"\t"+str(element[2])+"\n")
        file.close()
    #-----------------------------------
    
    keytimes=[]
    for y in range(len(vergleichstext)):
        for x in range(len(vergleichstext[y])):
                   keytimes+=[[vergleichstext[y][x]]]
    lastkeytime=0
    completed=0
    starttime=0
    wrongkeys=0
    #-----------------------------
    timelabel.config(text="")
    entry.itemconfig(cursor,fill="lightgrey",state='normal')
    entry.delete("deletable")
    cursorpos[1]=0
    cursorpos[0]=0
    entry.coords(cursor,buchstabe_x*cursorpos[0],buchstabe_y*cursorpos[1],buchstabe_x*(cursorpos[0]+1),buchstabe_y*(cursorpos[1]+1))
    root.bind("<Key>",callback)

    
root=Tk()
root.title("TippTestTool")

entry=Canvas(root,width=breite,height=hoehe,bg='white')
entry.grid(row=0,column=0,columnspan=3)


cursor=entry.create_rectangle(0,0,buchstabe_x,buchstabe_y,fill='lightgrey')
cursorpos=[0,0]


txt=entry.create_text(1,1,anchor=NW,font=schriftart,text=textstr)

resetbutton=Button(root,text="Reset",command=reset)
resetbutton.grid(column=0,row=1)

timelabel=Label(root,text="")
timelabel.grid(column=1,row=1)

reset()
root.mainloop()


