'''
@discription  : Copyright © 2021-2024 Blue Summer Studio. All rights reserved.
@Author       : Niu zhixin
@Date         : 2024-12-21 16:35:05
@LastEditTime : 2025-01-25 16:51:53
@LastEditors  : Niu zhixin
'''
#!! Tkinter
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import askyesnocancel,showwarning
from tkinter.filedialog import asksaveasfilename
from tkinter.ttk import Treeview,Notebook,Button,Labelframe,Combobox,Style

#!! Built In Libraries
import re
import os
import json
import time
from typing import NoReturn
import sqlite3
import gettext
from configparser import ConfigParser

#!! Third Party Libraries
import socket
import threading
import secrets
from PIL import Image,ImageTk
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.fernet import Fernet
import concurrent.futures

LANGUAGE_LIST = ['简体中文','English']
KEY = b'H5njeRP8RXXy3SNNs_j7AyQWpTs87d_Moq5pcDoeXME='
sql_conn = sqlite3.connect(r'.\Lib\user.db')
cursor = sql_conn.cursor()
USER = []
LOGIN = ''
ini_cursor = ConfigParser()
ini_cursor.read(f'{os.getcwd()}\\Lib\\config.ini',encoding='gb2312')
print(ini_cursor.has_section('Settings'))
LANG = ini_cursor.get('Settings','language')
if LANG == 'English':
    lang = gettext.translation('en', localedir='locales', languages=['en'])
    lang.install()
    _ = lang.gettext
else:
    def _(message:str) -> str:return message

server_users = []
server_conns = []
server_iid = []
server_expression_button = {}
server_buttons = {}
server_expression = list('😀😁😂🤣😃😄😅😆😉😊😋😎😍😘🥰😗😙🥲😚🙂🤗🤩🤔🫡🤨😐😑😶🫥🙄😏😣😥😮🤐😯😪😫🥱😴😌😛😜😝🤤😒😓😔😕🫤🙃🫠🤑😲🙁😖😞😟😤😢😭😦😧😨😩🤯')
VERSION = _('v.2.0.3发布版')

class server:
    def __init__(self,window:Tk|None=None) -> None:
        global socket_server, ip_address ,server_users
        socket_server=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,True)
        ip_address = socket.gethostbyname(socket.gethostname())
        socket_server.bind((ip_address,30247))
        socket_server.listen(10)
        if not window is None:
            self.window = window
        server_users.append(LOGIN)
    
    def __set__(self,password) -> None:
        global receives,member,menubar,about,other,is_alt,settings_value,settings_option,style,font_size,sends,INPUT
        font_size = ('楷体',12)
        style = Style()
        style.configure('LNSS.Treeview',font=font_size)
        is_alt = False
        root = self.window
        root.title(_('socket server'))
        root.geometry('640x480')
        root.resizable(False,False)
        root.iconphoto(False, Image_load.load(root,image_file=f'{os.getcwd()}\\Lib\\show.png'))
        receives = ScrolledText(root,background='#f2f2f2',cursor='arrow',wrap=WORD)
        receives.place(x=5,y=0,width=490,height=310)
        receives.tag_config('mine',foreground='#000000',background='#43a649',font=font_size)
        receives.tag_config('others',foreground='#000000',background='#ffffff',font=font_size)
        receives.tag_config('system',foreground='#ff0000',background='#ffff00',font=font_size)
        receives.tag_config('message',foreground='#000000',background='#ffffff',font=font_size)
        receives.insert(END,_('请在客户端输入以下IP：')+ip_address,'system')
        receives.insert(END,'\n')
        receives.insert(END,_('请在客户端输入以下密码：')+password,'system')
        receives.insert(END,'\n')
        member = Treeview(root,show='headings',columns='NAME',style='LNSS.Treeview')
        member.place(x=495,y=0,width=145,height=310)
        member.column('NAME',width=145)
        member.heading('NAME',text=_('当前在线：'))
        member.insert('',END,values=LOGIN+'\n')
        INPUT = StringVar()
        INPUT.set('')
        sends = Entry(root,width=110,textvariable=INPUT)
        sends.place(x=5,y=310,width=545,height=170)
        sending = Button(root,text=_('发送'),command=lambda:self.send(sends.get(),INPUT))
        sending.place(x=552,y=310)
        expressions = Button(root,text=_('表情'),command=lambda:self.expressions())
        expressions.place(x=552,y=335)
        menubar = Menu(root)
        root.config(menu=menubar)
        about = Menu(menubar,tearoff=0)
        about.add_command(label=_('关于...(A)'),command=lambda:self.MenuHelp(root),accelerator='Ctrl+A',underline=6)
        about.add_command(label=_('帮助(H)'),command=lambda:self.MenuHelp(root),accelerator='F1',underline=4)
        menubar.add_cascade(label=_('关于(A)'),menu=about,underline=3)
        save_as = Menu(menubar,tearoff=0)
        save_as.add_command(label=_('保存对话(S)'),command=lambda:self.save_as(),accelerator='Ctrl+S',underline=5)
        menubar.add_cascade(label=_('更多(M)'),menu=save_as,underline=3)
        root.bind('<Key>',lambda event:self.onkey(event))
        sends.bind('<Return>',lambda events:self.send(sends.get(),INPUT))
        

    def __accept__(self) -> NoReturn:
        while True:
            try:
                result=socket_server.accept()
                conn=result[0]
                address=result[1]
                if self.check(conn):
                    server_conns.append(conn)
                    user_name = conn.recv(1024).decode("UTF-8")
                    server_users.append(user_name)
                    server_iid.append(member.insert('',END,values=user_name))
                    conn.send(json.dumps(server_users).encode('UTF-8'))
                    receives.insert(END,_('[系统提示]%s加入群聊！')%user_name,'system')
                    receives.insert(END,'\n')
                    self.send_all(server_conns,None,_('[系统提示]%s加入群聊！')%user_name)
                    self.send_all(server_conns,conn,_('[系统提示]user_append:%s')%user_name)
                    threading.Thread(target=self.show,args=(conn,server_conns)).start()
            except:
                break
    
    def check(self,conn:socket.socket) -> bool:
        conn.send(password.encode("UTF-8"))
        
        while True:
            re = conn.recv(1024).decode('utf-8')
            if re == password:
                return True
            elif re == 'error':
                return False
    
    def onkey(self,event:Event) -> None:
        if event.state in (4,6,12,14,36,38,44,46):
            if event.keysym.upper() == 'A':
                self.MenuHelp(self.window)
            if event.keysym.upper() == 'S':
                self.save_as()
    
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
        if str(item) == _('显示'):
            server_root.deiconify()
        elif str(item) == '退出':
            is_destroy = askyesnocancel(_('警告！'),_('一但关闭程序，所有连接将断开（无法恢复！）'))
            if not is_destroy is None:
                if is_destroy:
                    threading.Thread(target=icon.stop,daemon=True).start()
                    self.send_all(server_conns,None,_('[系统提示]服务器已关闭连接，即将退出程序！'))
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
            showwarning(_('警告！'),_('发布内容不能为空！'))
    
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
                receives.insert(END,_('[系统提示]%s退出群聊！')%server_users[delete],'system')
                receives.insert(END,'\n')
                server_conns.pop(delete-1)
                self.send_all(server_conns,conn,_('[系统提示]%s退出群聊！'%server_users[delete]))
                self.send_all(server_conns,conn,_('[系统提示]user_delete:%s'%server_users[delete]))
                server_users.pop(delete)
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
        about.title(_('关于'))
        about.geometry('300x160+350+200')
        about.resizable(False,False)
        about.iconphoto(False, PhotoImage(file=f'{os.getcwd()}\\Lib\\show.png'))
        Label(about, image=Image_load.load(master,f'{os.getcwd()}\\Lib\\show.png',(64,64))).place(x=20,y=40)
        Label(about, text='LNSS,'+_('版本 %s\n\n版权所有(c)2024')%VERSION, font=('华文新魏', 11), justify=LEFT).place(x=120,y=40)
    
    def save_as(self) -> None:
        file = asksaveasfilename(filetypes=[('LNSS '+_('聊天记录文件'),'*.lns')],defaultextension='.lns',initialfile=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))
        if file:
            self.decrypt_file(file)
    
    def decrypt_file(self,output_file_path):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        data = receives.get(0.0,END)
        
        with open(output_file_path, 'wb') as outfile:
            outfile.write(Fernet(KEY).encrypt(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )))#!! Write the private key to the output file
            
            outfile.write(b'\n')#!! Write a newline character to the output file
            
            outfile.write(public_key.encrypt(
                data.encode('gb2312',errors='ignore'),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            ))#!! Write the encrypted data to the output file

class Image_load:
    def load(master:Tk|None=None,image_file:str|bytes|None=None,size:tuple[int,int]|None=None) -> PhotoImage:
        global img_load,img
        img_load = Image.open(image_file)
        if not size is None:
            img_load.thumbnail(size)
        if not master is None:
            img = ImageTk.PhotoImage(img_load)
            return img
        else:
            return img_load

#!! 仅限中国大陆用户使用
class Netfind:
    def ip() -> list:
        all_ip = []
        os.popen('arp -d *','r')
        ip3 = int(os.popen('ipconfig').read().split('无线局域网适配器 WLAN:')[1].split('默认网关')[1].split(': ')[1].split('.1\n')[0].split('192.168.')[1])
        def scan(ip3:int,ip4:int):
            os.popen(f'ping -n 1 192.168.{ip3}.{ip4}')

        with concurrent.futures.ThreadPoolExecutor(max_workers=255) as executor:
            futures = {executor.submit(scan, ip3,ip4): ip4 for ip4 in range(1,256)}

        for line in (os.popen('arp -a').read().split('\n'))[4:-1]:
            if f'192.168.{ip3}.' in line:
                if '动态' in line:
                    all_ip.append(f'192.168.{ip3}.'+line.split(f'192.168.{ip3}.')[1].split(' ')[0])
        
        return all_ip

def smain(password_type,passwords):
    global server_root, main, icon, password
    print(password_type)
    if password_type == 'random_password':
        password = secrets.token_urlsafe(6)
        print(password)
    else:
        password = passwords
    #// logging.basicConfig(filename=f'{os.getcwd()}\\information\\_configure\\{Decimal(time.time()).quantize(Decimal("1."),rounding=ROUND_HALF_UP)}.log',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',datefmt = '%Y-%m-%d %H:%M:%S')
    #// logging.info('Lancher starts.')
    server_root = Toplevel()
    main = server(server_root)
    main.__set__(password)
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
        member.heading('NAME',text=_('当前在线：'))
        for user in client_users: member.insert('',END,values=user+'\n')
        member.update()
        INPUT = StringVar()
        INPUT.set('')
        sends = Entry(root,width=110,textvariable=INPUT)
        sends.place(x=5,y=310,width=545,height=170)
        sending = Button(root,text=_('发送'),command=lambda:self.send(sends.get(),INPUT))
        sending.place(x=552,y=310)
        expressions = Button(root,text=_('表情'),command=lambda:self.expressions())
        expressions.place(x=552,y=335)
        menubar = Menu(root)
        root.config(menu=menubar)
        about = Menu(menubar,tearoff=0)
        about.add_command(label=_('关于...(A)'),command=lambda:self.MenuHelp(root),accelerator='Ctrl+A',underline=6)
        about.add_command(label=_('帮助(H)'),command=lambda:self.MenuHelp(root),accelerator='F1',underline=4)
        menubar.add_cascade(label=_('关于(A)'),menu=about,underline=3)
        save_as = Menu(menubar,tearoff=0)
        save_as.add_command(label=_('保存对话(S)'),command=lambda:self.save_as(),accelerator='Ctrl+S',underline=5)
        menubar.add_cascade(label=_('更多(M)'),menu=save_as,underline=3)
        root.bind('<Key>',lambda event:self.onkey(event))
        sends.bind('<Return>',lambda events:self.send(sends.get(),INPUT))
    
    def onkey(self,event:Event) -> None:
        if event.state in (4,6,12,14,36,38,44,46):
            if event.keysym.upper() == 'A':
                self.MenuHelp(self.window)
            if event.keysym.upper() == 'S':
                self.save_as()
    
    def expressions(self):
        global client_buttons,client_expression_button,expression_choose
        expression_choose = Toplevel(self.window)
        for i in range(11):
            for j in range(6):
                button = Button(expression_choose,text=client_expression[(i-1)*6+j],command=lambda i=i,j=j:self.expression(i,j),width=3)
                button.grid(column=i,row=j)
                client_buttons[i,j] = button
                client_expression_button[i,j] = client_expression[(i-1)*6+j]
    
    def destroied(self,master:Tk) -> None:
        master.withdraw()
        try:
            expression_choose.withdraw()
        except:
            pass
    
    def menu(item) -> None:
        if str(item) == '显示':
            client_root.deiconify()
        elif str(item) == '退出':
            is_destroy = askyesnocancel(_('警告！'),_('一但关闭程序，所有连接将断开（无法恢复！）'))
            if not is_destroy is None:
                if is_destroy:
                    threading.Thread(target=icon.stop,daemon=True).start()
                    socket_client.close()
                    client_root.quit()
                    client_root.destroy()
                    icon.stop()
    
    def Menuhelp(master:Tk) -> None:
        about = Toplevel(master)
        about.title(_('关于'))
        about.geometry('300x160+350+200')
        about.resizable(False,False)
        about.iconphoto(False, PhotoImage(file=f'{os.getcwd()}\\data\\Lib\\show.png'))
        Label(about, image=Image_load.load(master,f'{os.getcwd()}\\data\\Lib\\show.png',(64,64))).place(x=20,y=40)
        Label(about, text='LNSS,'+_('版本 %s \n\n版权所有(c)2024'%VERSION), font=('华文新魏', 11), justify=LEFT).place(x=120,y=40)
    
    def get_data(self,root:Tk,data_from:list) -> None:
        global IP
        datas = []
        for data in data_from:
            datas.append(str(data.get()))
        IP = '.'.join(datas)
        root.destroy()
        
    def expression(self,x,y) -> None:
        global sends,INPUT
        INPUT.set(sends.get()+client_expression_button[x,y])

        
    def send(self,msg,INPUT:StringVar) -> None:
        if msg != '':
            socket_client.send((socket.gethostname()+':'+msg).encode("UTF-8"))
            INPUT.set('')
            receives.insert(END,socket.gethostname()+':','mine')
            receives.insert(END,msg,'message')
            receives.insert(END,'\n')
        else:
            showwarning(_('警告！'),_('发布内容不能为空！'))
    
    def receive(self) -> NoReturn:
        while True:
            try:
                data = socket_client.recv(1024).decode("UTF-8")
                if data[0:6]==_('[系统提示]'):
                    if data[6:18] == 'user_append:':
                        client_users.append(data[17:])
                        member.insert('',END,values=data[17:])
                    elif data[6:18] == 'user_delete:':
                        delete = client_users.count(data[17:])
                        member.delete(delete)
                        client_users.pop(delete)
                    elif data == _('[系统提示]服务器已关闭连接，即将退出程序！'):
                        time.sleep(5)
                        socket_client.close()
                        client_root.quit()
                        client_root.destroy()
                    else:
                        receives.insert(END,data,'system')
                        receives.insert(END,'\n')
                        receives.see(END)
                else:
                    receives.insert(END,data,'others')
                    receives.insert(END,'\n')
                    receives.see(END)
            except:
                break
    
    def save_as(self) -> None:
        file = asksaveasfilename(filetypes=[('LNSS '+_('聊天记录文件'),'*.lns')],defaultextension='.lns')
        if file:
            self.encrypt_file(file)
    
    def encrypt_file(self,output_file_path):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        data = receives.get(0.0,END)
        with open(output_file_path, 'wb') as outfile:
            outfile.write(Fernet(KEY).encrypt(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )))#!! Write the private key to the output file
            outfile.write(b'\n')#!! Write a newline character to the output file
            outfile.write(public_key.encrypt(
                data.encode('gb2312'),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            ))#!! Write the encrypted data to the output file

        os.remove('temp.txt')

def cmain(passwords,ips):
    global socket_client,client_root,icon
    socket_client = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_client.connect((ips,30247))
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
    if passwords == password:
        check = True
    if check:
        socket_client.send(password.encode('utf-8'))
        socket_client.send(socket.gethostname().encode('utf-8'))
        client_users = json.loads(socket_client.recv(1024).decode('utf-8'))
        client_root = Toplevel()
        main = client(client_root)
        main.__set__()
        threading.Thread(target=main.receive).start()
        client_root.protocol('WM_DELETE_WINDOW',lambda:main.destroied(client_root))
        client_root.mainloop()


class Login:
    def __init__(self,window:Tk|None=None) -> None:
        if not window is None:
            self.window = window

    def __choose_user__(self) -> None:
        self.window.withdraw()
        self.login = Toplevel(self.window)
        self.login.title(_('选择登入用户'))
        self.login.geometry('300x160+350+200')
        self.login.resizable(False,False)
        self.login.iconphoto(False, PhotoImage(file=f'{os.getcwd()}\\Lib\\show.png'))
        Label(self.login, text=_('选择登入用户：'), font=('楷体', 10)).place(x=20,y=20)
        self.user = Combobox(self.login, values=USER, font=('楷体', 10))
        self.user.current(0)
        self.user.place(x=20,y=60,width=260)
        # user_info =
        Button(self.login, text=_('注册'), command=lambda:self.sign_up(), width=10).place(x=20,y=100)
        Button(self.login, text=_('确定'), command=lambda:self.get_data(self.window,[self.user]), width=10).place(x=100,y=100)


    def get_data(self,window:Tk|None=None,entry:list[Combobox]=[]) -> None:
        global LOGIN
        if not window is None:
            self.window = window
        if not entry is None:
            self.entry = entry
        LOGIN = self.entry[0].get()
        print(LOGIN)
        self.login.destroy()
        main = Demo(server_root)
        main.__set__()
        self.window.deiconify()
    
    def sign_up(self) -> None:
        self.login.withdraw()
        self.sign = Toplevel(self.login)
        self.sign.title(_('注册用户'))
        self.sign.geometry('300x160+350+200')
        self.sign.resizable(False,False)
        self.sign.iconphoto(False, PhotoImage(file=f'{os.getcwd()}\\Lib\\show.png'))
        Label(self.sign, text=_('注册用户：'), font=('楷体', 10)).place(x=20,y=20)
        user = Entry(self.sign, font=('楷体', 10))
        user.place(x=100,y=20,width=160)
        is_admin = BooleanVar()
        is_admin.set(False)
        Checkbutton(self.sign, text=_('管理员'), font=('楷体',10),variable=is_admin).place(x=20,y=60)
        Button(self.sign, text=_('确定'), command=lambda:self.get_sign_up_data(self.login,[user,is_admin]), width=10).place(x=80,y=100)
    
    def get_sign_up_data(self,window:Tk|None=None,entry:list[Entry|BooleanVar]=[]) -> None:
        global USER
        if not window is None:
            self.swindow = window
        if not entry is None:
            self.entry = entry
        if self.entry[1].get():
            is_admin = True
        else:
            is_admin = False
        sql = '''INSERT INTO user_info (name,id,create_time,is_admin) VALUES (?,?,?,?)'''
        cursor.execute(sql,(self.entry[0].get(),int(secrets.token_hex(6),16),time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())),is_admin))
        USER.append(self.entry[0].get())
        self.user['values'] = USER
        self.user.current(len(USER)-1)
        self.user.update()
        sql_conn.commit()
        self.swindow.deiconify()
        self.sign.destroy()


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
        print(LOGIN)
        main_page = Notebook(root,padding='5 10 10 10')
        
        
        
        
        
        
        
        
        
        
        server_page = Frame(main_page)
        server_page.grid(sticky=(N, S, W, E))
        
        Label(server_page,text=_('密码：')).grid(column=0,row=0,sticky=NW)
        is_password = StringVar(value='random_password')
        self.is_password = is_password
        Radiobutton(server_page,text=_('自定义密码'),variable=is_password,value='custom_password').grid(column=1,row=0)
        password = Entry(server_page,validate='focus',validatecommand=self.check_password)
        password.grid(column=2,row=0)
        self.password = password
        self.custom_check = Label(server_page,fg='grey',font=("TkDefaultFont",8),text='',foreground='red',compound=LEFT)
        self.custom_check.grid(column=2,row=1,sticky=W)
        Radiobutton(server_page,text=_('随机密码'),variable=is_password,value='random_password').grid(column=1,row=2,sticky=W)
        
        Label(server_page,text=_('网络：')).grid(column=0,row=3,sticky=NW)
        Label(server_page,text=self.get_wifi()).grid(column=1,row=3,sticky=NW)
        
        Button(server_page,text=_('创建'),command=lambda:smain(self.is_password.get(),self.password.get())).grid(column=0,row=4,columnspan=3)
        
        
        
        
        
        client_page = Frame(main_page)
        client_page.grid(sticky=(N, S, W, E))
        
        Label(client_page,text=_('主机地址：')).grid(column=0,row=0,sticky=NW)
        cip = Entry(client_page,validate='focusout')
        cip.grid(column=1,row=0)
        
        Label(client_page,text=_('密码：')).grid(column=0,row=1,sticky=NW)
        cpassword = Entry(client_page,validate='focusout',validatecommand=self.check_password)
        cpassword.grid(column=1,row=1)
        self.cpassword = cpassword
        
        Label(client_page,text=_('网络：')).grid(column=0,row=2,sticky=NW)
        Label(client_page,text=self.get_wifi()).grid(column=1,row=2,sticky=NW)
        
        Button(client_page,text=_('加入'),command=lambda:cmain(self.cpassword.get(),cip.get())).grid(column=0,row=3,columnspan=3,rowspan=4)
        
        
        
        
        
        welcome_page = Frame(main_page)
        welcome_page.grid(sticky=(N, S, W, E))
        Label(welcome_page,text=_('你好，%s!')%LOGIN,font=('楷体',12),anchor=W).grid(column=0,row=0,sticky=W)
        Label(welcome_page,text=_('欢迎使用 LNSS 聊天系统！'),font=('楷体',10),anchor=W).grid(column=0,row=2,sticky=W)
        Label(welcome_page,text=_('版本：%s')%VERSION,font=('楷体',10),anchor=W).grid(column=0,row=3,sticky=W)
        Label(welcome_page,text=_('作者：牛 志鑫 & Blue Summer Studio'),font=('楷体',10),anchor=W).grid(column=0,row=4,sticky=W)
        Button(welcome_page,text=_('更多...'),command=lambda:self.show_more()).grid(column=0,row=5,sticky=W)
        Button(welcome_page,text=_('设置...'),command=lambda:self.settings()).grid(column=1,row=5)
        
        
        
        main_page.add(server_page,text=_('服务端'))
        main_page.add(client_page,text=_('客户端'))
        main_page.add(welcome_page,text=_('欢迎'))
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
            self.custom_check.config(text=_('密码可用'),foreground='green',image=Image_load.load(self.window,f'{os.getcwd()}\\Lib\\correct.png',(10,10)))
            return True
        else:
            self.custom_check.config(text=_('密码不可用'),foreground='red',image=Image_load.load(self.window,f'{os.getcwd()}\\Lib\\warning.png',(10,10)))
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
            return str(_('无网络'))
    
    def show_more(self) -> None:
        with open(f'{os.getcwd()}\\LICENSES','r',encoding='utf-8') as f:
            premits = f.read()
        more = Toplevel(self.window)
        more.resizable(False,False)
        more.geometry('400x320+350+200')
        more.iconphoto(False, PhotoImage(file=f'{os.getcwd()}\\Lib\\show.png'))
        more.title(_('更多信息'))
        main = Notebook(more)
        
        premit = Frame(main)
        premit_scroll = Scrollbar(premit)
        premit_show = Text(premit,font=('楷体',10),wrap=WORD,yscrollcommand=premit_scroll.set)
        premit_scroll.config(command=premit_show.yview)
        premit_show.insert(END,premits)
        premit_show.config(state=DISABLED)
        premit_show.pack(side=LEFT,fill=Y)
        premit_scroll.pack(side=RIGHT,fill=Y)

        
        premit.pack(fill=BOTH)
        main.add(premit,text=_('许可证'))  
        main.pack(fill=BOTH)
    
    def settings(self) -> None:
        self.setting = Toplevel(self.window)
        self.setting.resizable(False,False)
        self.setting.geometry('365x410+350+200')
        self.setting.title(_('设置'))
        notebook = Notebook(self.setting,padding='5 10 10 10')
        
        language = Frame(notebook)
        language_frame = LabelFrame(language,text=_('语言'),height=350)
        language_frame.pack(fill=X,side=TOP)
        self.language_famliy = Combobox(language_frame,width=30,height=8,values=LANGUAGE_LIST)
        self.language_famliy.current(LANGUAGE_LIST.index(LANG))
        self.language_famliy.grid(column=0,row=0)
        
        language.pack(fill=BOTH)
        notebook.add(language,text=_('语言'))
        notebook.pack(fill=BOTH,expand=1)
        Button(self.setting,text=_('应用'),command=lambda:self.apply()).pack(side=RIGHT)
    
    def apply(self) -> None:
        LANG = self.language_famliy.get()
        ini_cursor.set('Settings','language',LANG)
        with open(f'{os.getcwd()}\\Lib\\config.ini','w') as f:
            ini_cursor.write(f)
        self.setting.destroy()
    
def sign_up() -> None:
    sign = Tk()
    sign.title(_('注册'))
    sign.geometry('400x160+350+200')
    sign.resizable(False,False)
    sign.iconphoto(False, PhotoImage(file=f'{os.getcwd()}\\Lib\\show.png'))
    sign.protocol('WM_DELETE_WINDOW',lambda:os._exit(0))
    Label(sign,text=_('让我们开始吧！'),font=('楷体',12)).place(x=20,y=20)
    Label(sign,text=_('您的用户名是：'),font=('楷体',10)).place(x=20,y=60)
    user = Entry(sign,font=('楷体',10))
    user.place(x=160,y=60)
    Button(sign,text=_('确定'),command=lambda:sign_up_data(sign,user)).place(x=20,y=100)
    Button(sign,text=_('取消'),command=lambda:os._exit(0)).place(x=120,y=100)
    sign.mainloop()

def sign_up_data(master:Tk,user:Entry) -> None:
    sql = '''INSERT INTO user_info (name,id,create_time,is_admin) VALUES (?,?,?,TRUE)'''
    cursor.execute(sql,(user.get(),int(secrets.token_hex(6),16),time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))))
    sql_conn.commit()
    master.destroy()


def check_table() -> None:
    sql = '''CREATE TABLE IF NOT EXISTS user_info (
        name TEXT NOT NULL, 
        id INTEGER PRIMARY KEY UNIQUE NOT NULL,
        create_time NUMBER NOT NULL, 
        last_login NUMBER, 
        is_admin BOOLEAN
        )'''
    cursor.execute(sql)
    if ini_cursor.get('Users','is_first_run'):
        sign_up()
        ini_cursor.set('Users','is_first_run','False')
        with open(f'{os.getcwd()}\\Lib\\config.ini','w') as f:
            ini_cursor.write(f)
    sql = '''SELECT * FROM user_info'''
    cursor.execute(sql)
    for i in cursor.fetchall():
        USER.append(i[0])
    
def main():
    global server_root
    check_table()
    server_root = Tk()
    Login(server_root).__choose_user__()
    server_root.mainloop()

main()
