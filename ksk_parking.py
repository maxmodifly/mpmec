from Tkinter import *
import ttk
from PIL import ImageTk,Image
from tkFont import Font
from rfid_sl500 import SL500_RFID_Reader
import time
import urllib2
import logging
import sys,os

url = 'http://192.168.0.2/atmoz/parking/'
tower = '2'
readCard = 0
confirm = 0
buttonShow = 0
giff = 0
num_gif = 0
resp = 0
status =0
chk_status = 1
now_show = 0
logging.basicConfig(filename='/home/pi/program/test/log.log', filemode='a+', format='%(asctime)s - %(levelname)s - %(message)s')
logging.warning('Start Program')

reader = SL500_RFID_Reader('/dev/ttyUSB0',19200)
reader.DEBUG_MODE = False
    # reader.MUTE_MODE = True
#reader.set_key('\xFF\xFF\xFF\xFF\xFF\xFF')
reader.rf_light(reader.LED_RED)

root = Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
fnt2 = Font(family='Helvetica', size=50, weight='bold')
canvas = Canvas(root,bg="black", height=h, width=w)



canvas.pack()

root.attributes('-fullscreen', True)
root.bind("<Escape>", quit)
root.bind("x", quit)
stat = 0

fnt = Font(family='Helvetica', size=20, weight='bold')
txt = StringVar()
txt.set(time.strftime("%H:%M:%S"))
lbl = Label(root ,textvariable=txt, font=fnt, foreground="green", background="black")
lbl.place(relx=1,  anchor=NE)


def read_rfid():
    #card_data = reader.read_block(0)
    card_data = reader.read_card()
    #card_data = reader.rf_select
    return card_data

def click_confirm():
    global confirm
    confirm = 1

def quit(*args):
    root.destroy()

def show_time():
    txt.set(time.strftime("%H:%M:%S"))
    root.after(1000, show_time)

def check_status():
    try:
        response = urllib2.urlopen(url+'status.php?tower='+tower)
        html = response.read()
        return html
    except:
        logging.error('check status')
        return '9'

def send_card(card):
    try:
        response = urllib2.urlopen(url+'carin.php?tower='+tower+'&cardno='+card)

        html = response.read()
        logging.info('Car in cardID='+card+' res='+html)
        return html
    except:

        logging.error('send card='+card)
        return '2'



imgHome = ImageTk.PhotoImage(file="/home/pi/program/test/checkin_idle.png")
imgCard = ImageTk.PhotoImage(file="/home/pi/program/test/checkin_screen1.png")
imgdonw = ImageTk.PhotoImage(file="/home/pi/program/test/outofservice.png")
imgComp = ImageTk.PhotoImage(file="/home/pi/program/test/checkin_screen3.png")
imgComp2 = ImageTk.PhotoImage(file="/home/pi/program/test/checkin_screen35.png")
imgConf = ImageTk.PhotoImage(file="/home/pi/program/test/entry.png")
imgCarIn = ImageTk.PhotoImage(file="/home/pi/program/test/waitcarin.jpg")
imgCarOut = ImageTk.PhotoImage(file="/home/pi/program/test/waitcarout.jpg")
imgCarIns = ImageTk.PhotoImage(file="/home/pi/program/test/carinsystem.jpg")
imgCardno = ImageTk.PhotoImage(file="/home/pi/program/test/cardnoregis.jpg")

imgBT = ImageTk.PhotoImage(file="/home/pi/program/test/CF_BOX.png")
def show_pics(pic):

    if pic == 1:
        canvas.delete("all")
        canvas.create_image(0,0, anchor=NW, image=imgHome)
    elif pic == 2:
        canvas.delete("all")
        canvas.create_image(0,0, anchor=NW, image=imgCard)
    elif pic == 3:
        canvas.delete("all")
        canvas.create_image(0,0, anchor=NW, image=imgdonw)
    elif pic == 4:
        canvas.delete("all")
        canvas.create_image(0,0, anchor=NW, image=imgComp)
    elif pic == 5:
        canvas.delete("all")
        canvas.create_image(0,0, anchor=NW, image=imgConf)
    elif pic == 6:
        canvas.delete("all")
        canvas.create_image(0,0, anchor=NW, image=imgCarIns)
    elif pic == 7:
        canvas.delete("all")
        canvas.create_image(0,0, anchor=NW, image=imgCarIn)
    elif pic == 8:
        canvas.delete("all")
        canvas.create_image(0,0, anchor=NW, image=imgCarOut)
    elif pic == 9:
        canvas.delete("all")
        canvas.create_image(0,0, anchor=NW, image=imgComp2)
    elif pic == 10:
        canvas.delete("all")
        canvas.create_image(0,0, anchor=NW, image=imgComp2)
#print(pic)
#root.after(2000, show_pics)
#show_pics()
def main_program():


    global readCard
    global confirm
    global buttonShow
    global giff
    global num_gif
    global resp
    global status
    global chk_status
    global now_show
    if chk_status == 1:
        resps=check_status()
        stat = resps.split('&')
        status = stat[0]
        if status == '0' :
            os.system('sudo date -s "'+ stat[1] +'"')#2019-11-29 11:00:00
            os.system('vcgencmd measure_temp')
    delay_main = 5000

    if status == '0':

        bt_confrim.place_forget()
        if now_show != 1:
            now_show = 1
            show_pics(1)
        readCard=0

    elif status == '1' and readCard == 0:
        if now_show != 2:
            now_show = 2
            show_pics(2)
        delay_main = 200
        #card_no = read_rfid()
        card_no = reader.read_card()
        #print card_no
        if card_no > 0 :
            reader.rf_beep(20)
            readCard = card_no
            logging.info('Tab cardno = %s',card_no)
            print(card_no)
            #print('No RFID Card')
        reader.rf_light(reader.LED_RED)

    elif status == '1' and readCard != 0:

        if confirm == 0:
            if now_show != 5:
                now_show = 5
                show_pics(5)
            buttonShow = 1
            bt_confrim.place( x=645,y=340,width=350,height=131)#
            delay_main = 500
        else:
            try:
                #logging.error(readCard)
                if num_gif==0:
                   # logging.error(num_gif)
                    resp = send_card(readCard)
                    #logging.error('send1')
                    bt_confrim.place_forget()
                    chk_status = 0
                if resp == '1':
                    #print resp

                    if giff == 0 and num_gif < 20:
                        #print resp
                        #logging.error('send2')
                        if now_show != 4:
                            now_show = 4
                            show_pics(4)
                        num_gif += 1
                        delay_main = 500
                        giff = 1
                    elif giff == 1 and num_gif < 20:
                        if now_show != 9:
                            now_show = 9
                            show_pics(9)
                        num_gif += 1
                        #logging.error('send3')
                        giff = 0
                        delay_main = 500
                    else:
                        #logging.error('send4')
                        readCard = 0
                        confirm = 0
                        num_gif = 0
                        delay_main = 1
                        chk_status=1
                elif resp == '4':
                    #logging.error('send44')
                    readCard = 0
                    confirm = 0
                    num_gif = 0
                    bt_confrim.place_forget()
                    if now_show != 3:
                        now_show = 3
                        show_pics(3)
                    chk_status=1
                    delay_main = 10000
                else:
                    #logging.error('send55')
                    readCard = 0
                    confirm = 0
                    num_gif = 0
                    bt_confrim.place_forget()
                    if now_show != 6:
                        now_show = 6
                        show_pics(6)
                    chk_status=1
                    delay_main = 10000
            except:
                print("Oops!",sys.exc_info()[0],"occured.")
                logging.error('error send car in')
                num_gif=0;
                bt_confrim.place_forget()
                if now_show != 3:
                    now_show = 3
                    show_pics(3)
                delay_main = 10000
                readCard = 0
                chk_status=1
                confirm = 0

    elif status == '6':#
        if now_show != 6:
            now_show = 6
            show_pics(6)
        delay_main = 5000
    root.after(delay_main, main_program)



bt_confrim = Button(canvas,relief = FLAT,command= click_confirm ,image=imgBT)


#root.after(2000, show_pics)
root.after(1000, show_time)
main_program()

root.mainloop()
