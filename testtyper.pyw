from tkinter import *
import tkinter
import time
import hashlib
from pathlib import Path
import math

completed=0
local_wrongkey=0
keytimes=[]
keydata=[]
lastkeytime=0
starttime=0
disptime=1
wrongkeys=0
fname=""
textstr=""
vergleichstext=[]

text = open("TestText.txt", "r")
for line in text:
    textstr+=(line.rstrip())
text.close()
textstr=textstr.replace("$","")
textlength=len(textstr)

#------------------------
m = hashlib.md5()
m.update(textstr.encode('utf-8'))

#------------------------
schriftart=('Courier','24')

buchstabe_x=19
buchstabe_y=36

################################################################################################

textstr=""
text = open("TestText.txt", "r")
for line in text:
    textstr+=(line.rstrip())
text.close()
textstr=textstr.split("$")
##########################Fensterbreite kann man hier einstellen
breite=1000
##########################

spalten=int(breite/buchstabe_x)

reihenlist=[]
rowlength=[]

for i in textstr:
    reihenlist+=[int(len(i)/spalten)+1]
reihen=0
for i in reihenlist:
    reihen+=i


hoehe=buchstabe_y*(reihen)


for j in range(len(textstr)):

    for i in range(reihenlist[j]):
        if (i==reihenlist[j]-1):
           vergleichstext+=[textstr[j][i*spalten:]]
           rowlength+=[len(textstr[j][i*spalten:])]
        else:
            vergleichstext+=[textstr[j][i*spalten:(i+1)*spalten]]
            rowlength+=[spalten]


textstr=""
for i in vergleichstext:
    textstr+=i+"\n"

    
################################################################################################
##for i in range(reihen-1,0,-1):   
##    vergleichstext+=[textstr[i*spalten:(i+1)*spalten]]
##    textstr=textstr[0:i*spalten]+"\n"+textstr[i*spalten:textlength]
##vergleichstext+=[textstr[0*spalten:(0+1)*spalten]]
##vergleichstext=vergleichstext[::-1]
################################################################################################
textend=[ len(vergleichstext[len(vergleichstext)-1])-1, len(vergleichstext)-1]

for y in range(len(vergleichstext)):
    for x in range(len(vergleichstext[y])):
                   keytimes+=[[vergleichstext[y][x]]]

keydata+=[["t"]]
keydata+=[["tpm"]]
keydata+=[["fehler"]]
keydata+=[["gesamtf"]]

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


            stelle=0
            for i in range(0,cursorpos[1],1):
                print(reihenlist)
                stelle+=rowlength[i]
            stelle+=cursorpos[0]
                           
            keytimes[stelle]+=[int(round(currenttime-lastkeytime,3)*1000),local_wrongkey]
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

    next_y= cursorpos[1] + int((cursorpos[0]+1)/rowlength[cursorpos[1]])
    next_x=(cursorpos[0]+1)%rowlength[cursorpos[1]]

    cursorpos=[next_x,next_y]
    entry.coords(cursor,buchstabe_x*cursorpos[0],buchstabe_y*cursorpos[1],buchstabe_x*(cursorpos[0]+1),buchstabe_y*(cursorpos[1]+1))
    


    
def conclude():
    global starttime,completed, fname,disptime
    resetbutton.config(state="normal")
    completed=1
    root.unbind("<Key>")
    zeit=time.time()-starttime
    entry.itemconfig(cursor,state='hidden')

    if(disptime):
        timelabel.config(text=str(round(zeit,2))+" Sekunden")
    
#---------------------------

    keydata[0]+=[str(round(zeit,2))]
    keydata[1]+=[str(round(len(keytimes)/zeit*60,2))]
    keydata[2]+=[str(round(wrongkeys*100/(len(keytimes)+wrongkeys),2))]
    keydata[3]+=[str(wrongkeys)]
    
    file=open(fname,"w")
    file.write("TextID:\t" + m.hexdigest()+"\n")
    file.write("Zeichenzahl:\t" + str(len(keytimes))+"\n")
    file.write("\n--------------------------------------------------\n")

    for element in keydata:
        erg=str(element[0])+"\t"
        for sp in range(1,len(element)):
            erg+=str(element[sp])+"\t\t"
        file.write(erg+"\n")
        
    file.write("\n--------------------------------------------------\n")
    
    for element in keytimes:
        erg=""
        for sp in element:
            erg+=str(sp)+"\t"
        file.write(erg+"\n")
    file.close()
#-----------------------------------
def reset():
    global starttime,lastkeytimes,keytimes,wrongkeys,completed
    lastkeytime=0
    completed=0
    starttime=0
    wrongkeys=0
    #-----------------------------
    if(disptime):
        timelabel.config(text="")
    entry.itemconfig(cursor,fill="lightgrey",state='normal')
    entry.delete("deletable")
    cursorpos[1]=0
    cursorpos[0]=0
    entry.coords(cursor,buchstabe_x*cursorpos[0],buchstabe_y*cursorpos[1],buchstabe_x*(cursorpos[0]+1),buchstabe_y*(cursorpos[1]+1))
    root.bind("<Key>",callback)
    resetbutton.config(state="disabled")
    
def reset_all():
    global starttime,lastkeytimes,keytimes,wrongkeys,completed,fname
    keytimes=[]
    for y in range(len(vergleichstext)):
        for x in range(len(vergleichstext[y])):
                   keytimes+=[[vergleichstext[y][x]]]
    lastkeytime=0
    completed=0
    starttime=0
    wrongkeys=0
    #-----------------------------
    nr=1
    path="data/results_"
    path2="data\\results_"
    while(Path(path+"0"*(10-int(math.log(nr,10)))+str(nr)+".txt").is_file()):
        nr+=1
    fname=(path2+"0"*(10-int(math.log(nr,10)))+str(nr)+".txt")
    #-----------------------------
    if(disptime):
        timelabel.config(text="")
    entry.itemconfig(cursor,fill="lightgrey",state='normal')
    entry.delete("deletable")
    cursorpos[1]=0
    cursorpos[0]=0
    entry.coords(cursor,buchstabe_x*cursorpos[0],buchstabe_y*cursorpos[1],buchstabe_x*(cursorpos[0]+1),buchstabe_y*(cursorpos[1]+1))
    root.bind("<Key>",callback)
    resetbutton.config(state="disabled")
def toggle_time():
    global disptime
    disptime=(disptime+1)%2
    if(disptime==0):
        timelabel.config(text="Zeitanzeige deaktiviert!")
    else:
        timelabel.config(text="")
    
root=Tk()
root.title("TippTestTool")

entry=Canvas(root,width=breite,height=hoehe,bg='white')
entry.grid(row=0,column=0,columnspan=3)


cursor=entry.create_rectangle(0,0,buchstabe_x,buchstabe_y,fill='lightgrey')
cursorpos=[0,0]


txt=entry.create_text(1,1,anchor=NW,font=schriftart,text=textstr)

resetbutton=Button(root,text="Reset",command=reset)
resetbutton.grid(column=0,row=1)
resetbutton.config(state="disabled")

menubar=Menu(root)
submenu=Menu(menubar)
submenu.add_command(label="New User", command=reset_all)
submenu.add_command(label="Toggle Time Display",command=toggle_time)
menubar.add_cascade(label="File",menu=submenu)
root.config(menu=menubar)

timelabel=Label(root,text="")
timelabel.grid(column=1,row=1)

reset_all()
root.mainloop()


