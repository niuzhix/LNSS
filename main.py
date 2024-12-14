'''
@discription  : Copyright © 2021-2024 Blue Summer Studio. All rights reserved.
@Author       : Niu zhixin
@Date         : 2024-10-19 15:12:58
@LastEditTime : 2024-12-14 15:49:07
@LastEditors  : Niu zhixin
'''
import json
import socket
import math
#// import logging
import pystray
import threading
import time
import secrets
import os
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import askyesnocancel,showwarning
from tkinter.filedialog import asksaveasfilename,askopenfilename
from tkinter.ttk import Treeview,Notebook,Button,Labelframe,Combobox,Style
from typing import NoReturn
from PIL import Image,ImageTk
import re

server_users = [socket.gethostname()]
server_conns = []
server_iid = []
server_expression_button = {}
server_buttons = {}
server_expression = list('😀😁😂🤣😃😄😅😆😉😊😋😎😍😘🥰😗😙🥲😚🙂🤗🤩🤔🫡🤨😐😑😶🫥🙄😏😣😥😮🤐😯😪😫🥱😴😌😛😜😝🤤😒😓😔😕🫤🙃🫠🤑😲🙁😖😞😟😤😢😭😦😧😨😩🤯')
VERSION = 'v.0.5.3'

class server:
    def __init__(self,window:Tk|None=None) -> None:
        global socket_server, ip_address
        socket_server=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,True)
        ip_address = socket.gethostbyname(socket.gethostname())
        socket_server.bind((ip_address,30247))
        socket_server.listen(10)
        if not window is None:
            self.window = window
    
    def __set__(self) -> None:
        global receives,member,menubar,about,other,is_alt,settings_value,settings_option,style,font_size,sends,INPUT
        font_size = ('楷体',12)
        style = Style()
        style.configure('LNSS.Treeview',font=font_size)
        is_alt = False
        root = self.window
        root.title('socket server')
        root.geometry('640x480')
        root.resizable(False,False)
        print(type(Image_load.__load__(root,image_file=f'{os.getcwd()}\\Lib\\show.png')))
        root.iconphoto(False, Image_load.__load__(root,image_file=f'{os.getcwd()}\\Lib\\show.png'))
        receives = ScrolledText(root,background='#f2f2f2',cursor='arrow',wrap=WORD)
        receives.place(x=5,y=0,width=490,height=310)
        receives.tag_config('mine',foreground='#000000',background='#43a649',font=font_size)
        receives.tag_config('others',foreground='#000000',background='#ffffff',font=font_size)
        receives.tag_config('system',foreground='#ff0000',background='#ffff00',font=font_size)
        receives.tag_config('message',foreground='#000000',background='#ffffff',font=font_size)
        receives.insert(END,'请在客户端输入以下IP：'+ip_address,'system')
        receives.insert(END,'\n')
        member = Treeview(root,show='headings',columns='NAME',style='LNSS.Treeview')
        member.place(x=495,y=0,width=145,height=310)
        member.column('NAME',width=145)
        member.heading('NAME',text='当前在线：')
        member.insert('',END,values=socket.gethostname()+'\n')
        INPUT = StringVar()
        INPUT.set('')
        sends = Entry(root,width=110,textvariable=INPUT)
        sends.place(x=5,y=310,width=545,height=170)
        sending = Button(root,text='发送',command=lambda:self.send(sends.get(),INPUT))
        sending.place(x=552,y=310)
        expressions = Button(root,text='表情',command=lambda:self.expressions())
        expressions.place(x=552,y=335)
        menubar = Menu(root)
        root.config(menu=menubar)
        about = Menu(menubar,tearoff=0)
        about.add_command(label='关于...(A)',command=lambda:self.MenuHelp(root),accelerator='Ctrl+A',underline=6)
        about.add_command(label='帮助(H)',command=lambda:self.MenuHelp(root),accelerator='F1',underline=4)
        menubar.add_cascade(label='关于(A)',menu=about,underline=3)
        root.bind('<Key>',lambda event:self.onkey(event))
        sends.bind('<Return>',lambda events:self.send(sends.get(),INPUT))
        

    def __accept__(self) -> NoReturn:
        while True:
            try:
                print('****')
                result=socket_server.accept()
                conn=result[0]
                address=result[1]
                if self.check(conn):
                    server_conns.append(conn)
                    user_name = conn.recv(1024).decode("UTF-8")
                    server_users.append(user_name)
                    server_iid.append(member.insert('',END,values=user_name))
                    conn.send(json.dumps(server_users).encode('UTF-8'))
                    receives.insert(END,'[系统提示]'+user_name+'加入群聊！','system')
                    receives.insert(END,'\n')
                    self.send_all(server_conns,None,'[系统提示]'+user_name+'加入群聊！')
                    self.send_all(server_conns,conn,'[系统提示]user_append:'+user_name)
                    threading.Thread(target=self.show,args=(conn,server_conns)).start()
            except:
                break
    
    def check(self,conn:socket.socket) -> bool:
        print(4444)
        conn.send(password.encode("UTF-8"))
        
        while True:
            re = conn.recv(1024).decode('utf-8')
            print(re)
            if re == password:
                return True
            elif re == 'error':
                return False
    
    def onkey(self,event:Event) -> None:
        if event.state in (4,6,12,14,36,38,44,46):
            if event.keysym.upper() == 'A':
                self.MenuHelp(self.window)
    
    def expressions(self):
        global server_buttons,server_expression_button,expression_choose
        expression_choose = Toplevel(self.window)
        for i in range(11):
            for j in range(6):
                button = Button(expression_choose,text=server_expression[(i-1)*6+j],command=lambda i=i,j=j:self.expression(i,j),width=3)
                button.grid(column=i,row=j)
                server_buttons[i,j] = button
                server_expression_button[i,j] = server_expression[(i-1)*6+j]
    
    def destroied(self,master:Tk) -> None:
        master.withdraw()
        try:
            expression_choose.withdraw()
        except:
            pass
        
    def menu(self,item) -> None:
        print(item)
        if str(item) == '显示':
            server_root.deiconify()
        elif str(item) == '退出':
            is_destroy = askyesnocancel('警告！','一但关闭程序，所有连接将断开（无法恢复！）')
            print(is_destroy)
            if not is_destroy is None:
                if is_destroy:
                    threading.Thread(target=icon.stop,daemon=True).start()
                    self.send_all(server_conns,None,'[系统提示]服务器已关闭连接，即将退出程序！')
                    for conn in server_conns: conn.close()
                    socket_server.close()
                    server_root.quit()
                    server_root.destroy()
                    icon.stop()
    
    def send(self,msg,INPUT:StringVar|None=None) -> None:
        if msg != '':
            INPUT.set('')
            for conn in server_conns:
                conn.send((socket.gethostname()+':'+msg).encode("UTF-8"))
            receives.insert(END,socket.gethostname()+':','mine')
            receives.insert(END,msg,'message')
            receives.insert(END,'\n')
            receives.see(END)
            receives.update()
        else:
            showwarning('警告！','发布内容不能为空！')
    
    def expression(self,x,y) -> None:
        global sends,INPUT
        INPUT.set(sends.get()+server_expression_button[x,y])
        
    def show(self,conn,user) -> None:
        global server_conns
        while True:
            try:
                data = conn.recv(1024).decode("UTF-8")
                receives.insert(END,data,'others')
                receives.insert(END,'\n')
                receives.see(END)
                receives.update()
                self.send_all(user,conn,data)
            except:
                delete = server_conns.count(conn)
                print(delete)
                print(server_users)
                receives.insert(END,'[系统提示]'+server_users[delete-1]+'退出群聊！','system')
                receives.insert(END,'\n')
                server_conns.pop(delete-1)
                self.send_all(server_conns,conn,'[系统提示]'+server_users[delete-1]+'退出群聊！')
                self.send_all(server_conns,conn,'[系统提示]user_delete:'+server_users[delete-1])
                server_users.pop(delete-1)
                member.delete(server_iid[delete-1])
                server_iid.pop(delete-1)
                break
        return
    
    def send_all(self,user,send,msg) -> None:
        for people in user:
            if not people == send:
                people.send(msg.encode("UTF-8"))
    
    def MenuHelp(self,master:Tk) -> None:
        about = Toplevel(master)
        about.title('关于')
        about.geometry('300x160+350+200')
        about.resizable(False,False)
        about.iconphoto(False, PhotoImage(file=f'{os.getcwd()}\\Lib\\show.png'))
        Label(about, image=Image_load.__load__(master,f'{os.getcwd()}\\Lib\\show.png',(64,64))).place(x=20,y=40)
        Label(about, text='LNSS,版本 '+VERSION+'\n\n版权所有(c)2024', font=('华文新魏', 11), justify=LEFT).place(x=120,y=40)

class Image_load:
    def __load__(master:Tk|None=None,image_file:str|bytes|None=None,size:tuple[int,int]|None=None) -> PhotoImage:
        global img_load,img
        img_load = Image.open(image_file)
        if not size is None:
            img_load.thumbnail(size)
        if not master is None:
            img = ImageTk.PhotoImage(img_load)
            return img
        else:
            return img_load

def smain(password_type):
    global server_root, main, icon, password
    if password_type == 'no_password':
        password = 'no_password'
    elif password_type == 'random_password':
        password = secrets.token_urlsafe(6)
    else:
        password = password_type
    print(password)
    print(os.getcwd())
    #// logging.basicConfig(filename=f'{os.getcwd()}\\information\\_configure\\{Decimal(time.time()).quantize(Decimal("1."),rounding=ROUND_HALF_UP)}.log',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',datefmt = '%Y-%m-%d %H:%M:%S')
    #// logging.info('Lancher starts.')
    server_root = Toplevel()
    main = server(server_root)
    main.__set__()
    threading.Thread(target=main.__accept__).start()
    server_root.protocol('WM_DELETE_WINDOW',lambda:server.destroied(main,server_root))
    server_root.mainloop()


client_users = []
client_expression_button = {}
client_buttons = {}
client_expression = list('😀😁😂🤣😃😄😅😆😉😊😋😎😍😘🥰😗😙🥲😚🙂🤗🤩🤔🫡🤨😐😑😶🫥🙄😏😣😥😮🤐😯😪😫🥱😴😌😛😜😝🤤😒😓😔😕🫤🙃🫠🤑😲🙁😖😞😟😤😢😭😦😧😨😩🤯😬😮‍💨😰😱🥵🥶😳🤪😵😵‍💫🥴😠😡🤬😷🤒🤕🤢🤮🤧😇🥳🥸🥺🥹🤠🤡🤥🫨🙂‍↔️🙂‍↕️🤫🤭🫢🫣🧐🤓😈👿👹👺💀☠️👻👽👾🤖💩😺😸😹😻😼😽🙀😿😾🙈🙉🙊🐵🐶🐺🐱🦁🐯🦒🦝🦊🐮🐷🐗🐭🐹🐰🐸🐼🐨🐻‍❄️🐻🦓🐲🐔🦄🫏🫎🐴🐽🐾🐒🦍🦧🦮🐅🐈‍⬛🐈🐕🐩🐕‍🦺🐆🐎🦌🦬🦏🦛🐑🐏🐖🐄🐃🐂🐐🐪🐫🦙🦘🦥🐀🐁🦣🐘🦡🦨🦔🐇🐿️🦫🦎🐊🦦🦖🦕🐉🐍🐢🦈🐬🦭🐳🐋🐟🦞🐙🦑🦐🐡🐠🦀🐚🪸🪼🦆🦟')

class client():
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
        for user in client_users: member.insert('',END,values=user+'\n')
        member.update()
        INPUT = StringVar()
        INPUT.set('')
        sends = Entry(root,width=110,textvariable=INPUT)
        sends.place(x=5,y=310,width=545,height=170)
        sending = Button(root,text='发送',command=lambda:self.send(sends.get(),INPUT))
        sending.place(x=552,y=310)
        expressions = Button(root,text='表情',command=lambda:self.expression())
        expressions.place(x=552,y=335)
        menubar = Menu(root)
        root.config(menu=menubar)
        about = Menu(menubar,tearoff=0)
        about.add_command(label='关于...(A)',command=lambda:self.MenuHelp(root),accelerator='Ctrl+A',underline=6)
        about.add_command(label='帮助(H)',command=lambda:self.MenuHelp(root),accelerator='F1',underline=4)
        menubar.add_cascade(label='关于(A)',menu=about,underline=3)
        root.bind('<Key>',lambda event:self.onkey(event))
    
    def onkey(self,event:Event) -> None:
        if event.state in (4,6,12,14,36,38,44,46):
            if event.keysym.upper() == 'A':
                self.MenuHelp(self.window)
    
    def expression(self):
        global buttons,expression_button,expression_choose
        expression_choose = Toplevel(self.window)
        for i in range(11):
            for j in range(6):
                button = Button(expression_choose,text=client_expression[(i-1)*6+j],command=lambda i=i,j=j:self.expressions(i,j),width=3)
                button.grid(column=i,row=j)
                buttons[i,j] = button
                expression_button[i,j] = client_expression[(i-1)*6+j]
    
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
    
    def Menuhelp(master:Tk) -> None:
        about = Toplevel(master)
        about.title('关于')
        about.geometry('300x160+350+200')
        about.resizable(False,False)
        about.iconphoto(False, PhotoImage(file=f'{os.getcwd()}\\data\\Lib\\show.png'))
        Label(about, image=Image_load.__load__(master,f'{os.getcwd()}\\data\\Lib\\show.png',(64,64))).place(x=20,y=40)
        Label(about, text='LNSS,版本 '+VERSION+'\n\n版权所有(c)2024', font=('华文新魏', 11), justify=LEFT).place(x=120,y=40)
    
    def get_data(self,root:Tk,data_from:list) -> None:
        global IP
        datas = []
        for data in data_from:
            datas.append(str(data.get()))
        IP = '.'.join(datas)
        root.destroy()
    
    def askIP(self,root:Tk) -> None:
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
        Button(text='确认',command=lambda: self.get_data(root,data_from)).grid(column=3,row=2)
        Button(text='取消',command=lambda: os._exit(0)).grid(column=5,row=2)
        root.mainloop()
        
    def send(self,msg,INPUT:StringVar) -> None:
        if msg != '':
            socket_client.send((socket.gethostname()+':'+msg).encode("UTF-8"))
            INPUT.set('')
            receives.insert(END,socket.gethostname()+':','mine')
            receives.insert(END,msg,'message')
            receives.insert(END,'\n')
        else:
            showwarning('警告！','发布内容不能为空！')
    
    def receive(self) -> NoReturn:
        while True:
            try:
                data = socket_client.recv(1024).decode("UTF-8")
                if data[0:6]=='[系统提示]':
                    if data[6:18] == 'user_append:':
                        print('APPEND')
                        client_users.append(data[17:])
                        member.insert('',END,values=data[17:])
                    elif data[6:18] == 'user_delete:':
                        print('DELETE')
                        delete = client_users.count(data[17:])
                        member.delete(delete)
                        client_users.pop(delete)
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

def cmain(passwords):
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
        client_users = json.loads(socket_client.recv(1024).decode('utf-8'))
        print(client_users)
        client_root = Toplevel()
        main = client(client_root)
        main.__set__()
        func_receive = client.receive(main)
        func_receive.start()
        client_root.protocol('WM_DELETE_WINDOW',lambda:client.destroied(client,client_root))
        client_root.mainloop()



class Demo():
    def __init__(self,window:Tk|None=None) -> None:
        if not window is None:
            self.window = window
    
    def __set__(self) -> None:
        self.custom = None
        root = self.window
        root.geometry('380x210')
        root.title('socket client')
        root.resizable(False,False)
        root.iconphoto(False, PhotoImage(file=f'{os.getcwd()}\\Lib\\show.png'))
        main_page = Notebook(root)
        
        
        
        
        
        server_page = Frame(main_page)
        server_page.pack(fill=BOTH)
        
        Label(server_page,text='密码：').grid(column=0,row=0,sticky=NW)
        is_password = StringVar(value='random_password')
        self.is_password = is_password
        Radiobutton(server_page,text='无密码',variable=is_password,value='no_password').grid(column=1,row=0,sticky=W)
        Radiobutton(server_page,text='自定义密码',variable=is_password,value='custom_password').grid(column=1,row=1)
        password = Entry(server_page,validate='focus',validatecommand=self.check_password)
        password.grid(column=2,row=1)
        self.password = password
        self.custom_check = Label(server_page,fg='grey',font=("TkDefaultFont",8),text='',foreground='red',compound=LEFT)
        self.custom_check.grid(column=2,row=2,sticky=W)
        Radiobutton(server_page,text='随机密码',variable=is_password,value='random_password').grid(column=1,row=3,sticky=W)
        
        Label(server_page,text=f'网络：{self.get_wifi()}').grid(column=0,row=4,sticky=NW)
        
        Label(server_page,text='人数上限：\n（0为不限制）').grid(column=0,row=5)
        num = Entry(server_page,validate='focusout',validatecommand=self.check_int)
        num.grid(column=1,row=5,columnspan=2,sticky=NW)
        
        Button(server_page,text='创建',command=lambda:smain(self.password.get())).grid(column=0,row=9,columnspan=3,rowspan=4)
        
        
        
        
        
        client_page = Frame(main_page)
        client_page.pack(fill=BOTH)
        
        Label(client_page,text='密码：').grid(column=0,row=0,sticky=NW)
        cpassword = Entry(client_page,validate='focusout',validatecommand=self.check_password)
        cpassword.grid(column=1,row=0)
        self.cpassword = cpassword
        
        Label(client_page,text=f'网络：{self.get_wifi()}').grid(column=0,row=1,sticky=NW)
        
        Button(client_page,text='加入',command=lambda:cmain(self.cpassword.get())).grid(column=0,row=2,columnspan=3,rowspan=4)
        
        
        
        
        
        main_page.add(server_page,text='服务端')
        main_page.add(client_page,text='客户端')
        main_page.pack(fill=BOTH)
        root.after(0,lambda:self.upload())
    
    def upload(self) -> None:
        if self.is_password.get() != 'custom_password':
            self.password.config(state=DISABLED)
            self.custom_check.config(text='',image='')
        else:
            self.password.config(state=NORMAL)
        self.window.after(100,lambda:self.upload())
    
    def check_password(self)  -> bool:
        text = self.password.get()
        ret = re.match(r'[a-zA-Z0-9_]{6,8}',text)
        if (not ret is None) and len(text) <= 8 and len(text) >=6:
            self.custom_check.config(text='密码可用',foreground='green',image=Image_load.__load__(self.window,f'{os.getcwd()}\\Lib\\correct.png',(10,10)))
            return True
        else:
            self.custom_check.config(text='密码不可用',foreground='red',image=Image_load.__load__(self.window,f'{os.getcwd()}\\Lib\\warning.png',(10,10)))
            return False
    
    def check_int(self)  -> bool:
        text = self.password.get()
        ret = re.match(r'[1-9]?\d*',text)
        if (not ret is None) and len(text) <= 8 and len(text) >=6:
            return True
        else:
            return False
    
    def get_wifi(self) -> str:
        try:
            return os.popen('netsh wlan show interfaces').read().split('SSID')[1].split(': ')[1].split('\n')[0]
        except:
            return str('无网络')

class Image_load:
    def __load__(master:Tk|None=None,image_file:str|bytes|None=None,size:tuple[int,int]|None=None) -> PhotoImage:
        global img_load,img
        img_load = Image.open(image_file)
        if not size is None:
            img_load.thumbnail(size)
        if not master is None:
            img = ImageTk.PhotoImage(img_load)
            return img
        else:
            return img_load

def main():
    server_root = Tk()
    main = Demo(server_root)
    main.__set__()

    server_root.mainloop()

main()