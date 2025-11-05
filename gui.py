#tkinter koska keeping it real
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import logic #logic.py tiedosto
#######################################################################################################
def ConnectionCheck():
    bridgeIP = ipAdrStr.get()
    connectionStatus = logic.TestHueConnection(bridgeIP)
    # Swapataan kuva tuloksen mukaan. Toimiikohan...
    if connectionStatus == True:
        bgCanvas.itemconfig(status_img_item, image=okImg)
        pairingBtn.config(state="normal")
    else:
        bgCanvas.itemconfig(status_img_item, image=notOkImg)
        pairingBtn.config(state='disabled')

def AutoDiscover():
    bridgeIP = logic.BridgeDiscovery()
    if str(bridgeIP).startswith("Discovery failed"):
        return
    else:
        ipAdrStr.set(bridgeIP)
def Pairing():
    userAnswer = messagebox.askokcancel("HUE Pair", "Press HUE Bridge button and click ok")
    if userAnswer == True:
        logic.GetUserAndKey(ipAdrStr.get())

    
#######################################################################################################
#Tkinter sälää
#Päänäytön määritys
root = tk.Tk()
root.title("HUE DYI")
root.geometry("600x600")
root.minsize(600,600)
root.maxsize(600,600)

#Tausta
bgImg = PhotoImage(file=r"media\background.png")
bgCanvas = tk.Canvas(root,width=600,height=600)
bgCanvas.pack(fill="both",expand=True)
bgCanvas.create_image(0,0,image=bgImg,anchor="nw")
bgCanvas.create_text(300,40, text="Philips HUE Control Application", font=("Gill Sans MT",30), fill="black")

#IP-osoitteen syöttö
ipAdrStr = tk.StringVar()
ipAdrLbl = tk.Label(root, text="Bridge IP", font=("Arial",10,"bold"), width=13)
ipAdrEntry = tk.Entry(root,textvariable=ipAdrStr, font=("Arial",10,"bold"),width=15)
ipAdrBtn = tk.Button(root,text="Submit",width=15, padx=0,pady=0, command=ConnectionCheck)
ipAdrBtn.config(highlightthickness=1, borderwidth=1)

#Nappi, joka suorittaa Hue Discoveryn
discoveryBtn = tk.Button(root, text="Discover", width=15, padx=0, pady=0, command=AutoDiscover)
discoveryBtn.config(highlightthickness=1, borderwidth=1)

#Nappi, joka hakee käyttäjätunnuksen ja keyn
pairingBtn = tk.Button(root, text="Pair", width=15, padx=0, pady=0, command=Pairing)
pairingBtn.config(highlightthickness=1, borderwidth=1, state="disabled")

#Tähän tulee taulukko, joka näyttää löydetyt laitteet. Taulukossa on sarakkeet: laite, nimi, tila

#Säilötään kuvat, ettei mene roskikseen (CoPilot sanoi niin)
okImg_pil = logic.Make_Transparent(r"media\connectionOK.png")
okImg = ImageTk.PhotoImage(okImg_pil)
notOkImg_pil = logic.Make_Transparent(r"media\connectionNotOK.png")
notOkImg = ImageTk.PhotoImage(notOkImg_pil)

bgCanvas.create_window(20,93,window=ipAdrLbl, anchor="nw")
bgCanvas.create_window(20,115,window=ipAdrEntry, anchor="nw")
bgCanvas.create_window(20,136,window=ipAdrBtn, anchor="nw")
bgCanvas.create_window(20,158,window=discoveryBtn, anchor="nw")
bgCanvas.create_window(20,180,window=pairingBtn, anchor="nw")
bgCanvas.create_text(180,92, text="Bridge\nResponse", font=("Arial",10, "bold"), fill="black")

#Yhteyskoe tulos TestHueConnection funktiosta (jos GET 200 YK OK)
status_img_item = bgCanvas.create_image(150,110,image=notOkImg, anchor="nw")

#######################################################################################################
#Execute
root.mainloop()