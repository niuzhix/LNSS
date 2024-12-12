'''
@discription  : Copyright © 2021-2024 Blue Summer Studio. All rights reserved.
@Author       : Niu zhixin
@Date         : 2024-06-28 09:54:20
@LastEditTime : 2024-12-08 19:57:51
@LastEditors  : Niu zhixin
'''
import json
import socket
import time
#// import pystray
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showwarning,askyesnocancel
from tkinter.simpledialog import askstring
from tkinter.ttk import Style,Treeview,Notebook,Labelframe,Combobox,Spinbox,Button
from typing import NoReturn
from PIL import Image,ImageTk
import sys,os

VERSION = 'v.0.5.3'
users = []
expression_button = {}
buttons = {}
expression = list('😀😁😂🤣😃😄😅😆😉😊😋😎😍😘🥰😗😙🥲😚🙂🤗🤩🤔🫡🤨😐😑😶🫥🙄😏😣😥😮🤐😯😪😫🥱😴😌😛😜😝🤤😒😓😔😕🫤🙃🫠🤑😲🙁😖😞😟😤😢😭😦😧😨😩🤯😬😮‍💨😰😱🥵🥶😳🤪😵😵‍💫🥴😠😡🤬😷🤒🤕🤢🤮🤧😇🥳🥸🥺🥹🤠🤡🤥🫨🙂‍↔️🙂‍↕️🤫🤭🫢🫣🧐🤓😈👿👹👺💀☠️👻👽👾🤖💩😺😸😹😻😼😽🙀😿😾🙈🙉🙊🐵🐶🐺🐱🦁🐯🦒🦝🦊🐮🐷🐗🐭🐹🐰🐸🐼🐨🐻‍❄️🐻🦓🐲🐔🦄🫏🫎🐴🐽🐾🐒🦍🦧🦮🐅🐈‍⬛🐈🐕🐩🐕‍🦺🐆🐎🦌🦬🦏🦛🐑🐏🐖🐄🐃🐂🐐🐪🐫🦙🦘🦥🐀🐁🦣🐘🦡🦨🦔🐇🐿️🦫🦎🐊🦦🦖🦕🐉🐍🐢🦈🐬🦭🐳🐋🐟🦞🐙🦑🦐🐡🐠🦀🐚🪸🪼🦆🦟')

def destroied(master:Tk) -> None:
    master.withdraw()
    try:
        expression_choose.withdraw()
    except:
        pass

def menu(item) -> None:
    print(item)
    if str(item) == '显示':
        client_root.deiconify()
    elif str(item) == '退出':
        is_destroy = askyesnocancel('警告！','一但关闭程序，所有连接将断开（无法恢复！）')
        print(is_destroy)
        if not is_destroy is None:
            if is_destroy:
                threading.Thread(target=icon.stop,daemon=True).start()
                socket_client.close()
                client_root.quit()
                client_root.destroy()
                icon.stop()



class MenuHelp:
    def __about__(master:Tk) -> None:
        about = Toplevel(master)
        about.title('关于')
        about.geometry('300x160+350+200')
        about.resizable(False,False)
        about.iconphoto(False, PhotoImage(file=f'{os.getcwd()}\\data\\Lib\\show.png'))
        Label(about, image=Image_load.__load__(master,f'{os.getcwd()}\\data\\Lib\\show.png',(64,64))).place(x=20,y=40)
        Label(about, text='LNSS,版本 '+VERSION+'\n\n版权所有(c)2024', font=('华文新魏', 11), justify=LEFT).place(x=120,y=40)

def askIP(root:Tk) -> None:
    root.title('IP地址')
    Label(root,text='请输入服务器端的IP地址：',anchor=W).grid(column=0,row=0,columnspan=7)
    n = 1
    data_from = []
    for i in [192,168,1,1]:
        stv = IntVar()
        ip = Spinbox(root,from_=1,to=255,textvariable=stv,width=8)
        stv.set(i)
        ip.grid(column=2*n-1,row=1)
        data_from.append(stv)
        if n == 4:
            pass
        else:
            Label(root,text='.').grid(column=2*n,row=1)
        n += 1
    Button(text='确认',command=lambda: get_data(root,data_from)).grid(column=3,row=2)
    Button(text='取消',command=lambda: os._exit(0)).grid(column=5,row=2)
    root.mainloop()

def get_data(root:Tk,data_from:list) -> None:
    global IP
    datas = []
    for data in data_from:
        datas.append(str(data.get()))
    IP = '.'.join(datas)
    root.destroy()

class send():
    def run(msg,INPUT:StringVar) -> None:
        if msg != '':
            socket_client.send((socket.gethostname()+':'+msg).encode("UTF-8"))
            INPUT.set('')
            receives.insert(END,socket.gethostname()+':','mine')
            receives.insert(END,msg,'message')
            receives.insert(END,'\n')
        else:
            showwarning('警告！','发布内容不能为空！')

class receive(threading.Thread):
    def run(self) -> NoReturn:
        while True:
            try:
                data = socket_client.recv(1024).decode("UTF-8")
                if data[0:6]=='[系统提示]':
                    if data[6:18] == 'user_append:':
                        print('APPEND')
                        users.append(data[17:])
                        member.insert('',END,values=data[17:])
                    elif data[6:18] == 'user_delete:':
                        print('DELETE')
                        delete = users.count(data[17:])
                        member.delete(delete)
                        users.pop(delete)
                    elif data == '[系统提示]服务器已关闭连接，即将退出程序！':
                        time.sleep(5)
                        socket_client.close()
                        client_root.quit()
                        client_root.destroy()
                    else:
                        receives.insert(END,data,'system')
                        receives.insert(END,'\n')
                        print('SYSTEM')
                        receives.see(END)
                else:
                    receives.insert(END,data,'others')
                    receives.insert(END,'\n')
                    receives.see(END)
            except:
                break


class Demo():
    def __init__(self,window:Tk) -> None:
        self.window = window
    
    def __set__(self) -> None:
        global receives,member,menubar,about,other,is_alt,settings_value,settings_option,style,font_size,sends,INPUT
        font_size = ('楷体',12)
        style = Style()
        style.configure('LNSS.Treeview',font=font_size)
        is_alt = False
        root = self.window
        root.geometry('640x480')
        root.title('socket client')
        root.resizable(False,False)
        root.iconphoto(False, PhotoImage(file=f'{os.getcwd()}\\Lib\\show.png'))
        receives = ScrolledText(root,background='#f2f2f2',cursor='arrow',wrap=WORD)
        receives.place(x=5,y=0,width=490,height=310)
        receives.tag_config('mine',foreground='#000000',background='#43a649',font=font_size)
        receives.tag_config('others',foreground='#000000',background='#ffffff',font=font_size)
        receives.tag_config('system',foreground='#ff0000',background='#ffff00',font=font_size)
        receives.tag_config('message',foreground='#000000',background='#ffffff',font=font_size)
        member = Treeview(root,show='headings',columns='NAME',style='LNSS.Treeview')
        member.place(x=495,y=0,width=145,height=310)
        member.column('NAME',width=145)
        member.heading('NAME',text='当前在线：')
        for user in users: member.insert('',END,values=user+'\n')
        member.update()
        INPUT = StringVar()
        INPUT.set('')
        sends = Entry(root,width=110,textvariable=INPUT)
        sends.place(x=5,y=310,width=545,height=170)
        sending = Button(root,text='发送',command=lambda:send.run(sends.get(),INPUT))
        sending.place(x=552,y=310)
        expressions = Button(root,text='表情',command=lambda:self.expression())
        expressions.place(x=552,y=335)
        menubar = Menu(root)
        root.config(menu=menubar)
        about = Menu(menubar,tearoff=0)
        about.add_command(label='关于...(A)',command=lambda:MenuHelp.__about__(root),accelerator='Ctrl+A',underline=6)
        about.add_command(label='帮助(H)',command=lambda:MenuHelp.__about__(root),accelerator='F1',underline=4)
        menubar.add_cascade(label='关于(A)',menu=about,underline=3)
        root.bind('<Key>',lambda event:self.onkey(event))
    
    def onkey(self,event:Event) -> None:
        if event.state in (4,6,12,14,36,38,44,46):
            if event.keysym.upper() == 'A':
                MenuHelp.__about__(self.window)
    
    def expression(self):
        global buttons,expression_button,expression_choose
        expression_choose = Toplevel(self.window)
        for i in range(11):
            for j in range(6):
                button = Button(expression_choose,text=expression[(i-1)*6+j],command=lambda i=i,j=j:send.expression(i,j),width=3)
                button.grid(column=i,row=j)
                buttons[i,j] = button
                expression_button[i,j] = expression[(i-1)*6+j]

class Image_load:
    def __load__(master:Tk|None,image_file:str|bytes,size:tuple[int,int]|None=None) -> PhotoImage:
        global img_load,img
        img_load = Image.open(image_file)
        if not size is None:
            img_load.thumbnail(size)
        if not master is None:
            img = ImageTk.PhotoImage(img_load)
            return img
        else:
            return img_load

def main(passwords):
    global socket_client,client_root,icon
    socket_client = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_client.connect(('192.168.101.38',30247))
    print(1)
    print(passwords)
    #// while True:
    #//     ask = Tk()
    #//     askIP(ask)
    #//     try:
    #//         socket_client.settimeout(5)
    #//         socket_client.connect((IP,1024))
    #//         socket_client.settimeout(None)
    #//         break
    #//     except:
    #//         showwarning('警告！','IP地址不符合规定！请重试！')

    check = False
    password = socket_client.recv(1024).decode('utf-8')
    print(2)
    print(password)
    if password != 'no_password':
        if passwords == password:
            check = True
    else:
        check = True
        print(check)
    if check:
        socket_client.send(password.encode('utf-8'))
        socket_client.send(socket.gethostname().encode('utf-8'))
        users = json.loads(socket_client.recv(1024).decode('utf-8'))
        print(users)
        client_root = Toplevel()
        main = Demo(client_root)
        main.__set__()
        func_receive = receive()
        func_receive.start()
        client_root.protocol('WM_DELETE_WINDOW',lambda:destroied(client_root))
        client_root.mainloop()

if __name__ == '__main__':
    main('')