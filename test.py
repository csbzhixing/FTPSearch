    #!/usr/bin/python=
    # This Python file uses the following encoding: utf-8
    
    
from Tkinter import *
from tkMessageBox import *
import threading
from ftplib import FTP
from multiprocessing.dummy import Pool
import socket

#这个是我的课程设计，做的很简单
    
root = Tk()
socket.setdefaulttimeout(3)
ftp = FTP()
pathList=[]

def goBack(event):
    try:
            path=ui.pathList.pop()
            ui.ftp.cwd(path)
            ui.fileList.delete(0,END)
            for i in ui.ftp.nlst():
                name=i.decode('gbk')
                ui.fileList.insert(END,name)
    except:
            return
            
def openFile(event):
    try:
            fi = ui.fileList.get(my_ui.fileList.curselection())
            fi=fi.encode('gbk')
            my_ui.pathList.append(my_ui.ftp.pwd())
            my_ui.ftp.cwd(fi)
            my_ui.fileList.delete(0,END)
            for i in my_ui.ftp.nlst():
                name=i.decode('gbk')
                my_ui.fileList.insert(END,name)
    except:
            my_ui.pathList.pop()
            return
        
def connectIP(event):
        try:
            my_ui.ftp.quit()
        except:
            print '退出'
        try:
            ip=my_ui.accessibleIP.get(my_ui.accessibleIP.curselection())
        except:
            my_ui.fileList.delete(0,END)
            return
        
        my_ui.fileList.delete(0,END)
        my_ui.ftp = FTP(ip,timeout=3)
        try:
            my_ui.ftp.login()
            for i in my_ui.ftp.nlst():
                name=i.decode('gbk')
                my_ui.fileList.insert(END,name)
        except:
            showwarning("警告", "你无法登录")
    
def ip2num(ip):
        ip = [int(x) for x in ip.split('.')]
        print ip;
        return ip[0]<<24 | ip[1] << 16 | ip[2] <<8 |ip[3]
    
def num2ip(num):
        #print num
        return '%s.%s.%s.%s' % ( (num & 0xff000000) >> 24,
                                  (num & 0x00ff0000) >> 16,
                                  (num & 0x0000ff00) >> 8,
                                  (num & 0x000000ff)
                                 )
def gen_ip(ip):
        start, end = [ip2num(x) for x  in ip.split('-')]
        return [num2ip(num) for num in range(start,end+1) if num & 0xff]
    
def printAccessibleIp(ip):
        try:
            result = FTP(ip)
            result.login(user='', passwd='', acct='')
            ui.accessibleIP.insert(END,ip)
            print ip
        except:
            pass
    
def go(begin,end):
        iprange = begin + '-' + end
        listOfIP = gen_ip(iprange)
        pool = Pool(255)
        results = pool.map(printAccessibleIp, listOfIP)
        pool.close()
        pool.join()
        print 'done'
def beginSearch(self):
            try:                
                begin = ui.firstIP.get()
                end = ui.endIP.get()
                
                if begin > end:
                    showinfo('Warning','Please input the correct scope of IP')
                    return          
                t=threading.Thread(target=go,args=(begin,end))
                t.start()
            except:
                 print 'Please input the correct scope of IP'        
        


    
class my_ui():
        ftp = FTP()
        pathList=[]
        
        
        mainFrame = Frame(root,width=480,bg='gray')
        label1 = Label(mainFrame,text='请输入IP的范围',bg='gray')
        label2 = Label(mainFrame,text='~',bg='gray')
        
        firstIP = Entry(mainFrame,width=18)
        endIP = Entry(mainFrame,width=18)
     
        
        searchButton = Button(mainFrame,text='搜索')
        searchButton.bind('<Button>',beginSearch)
        
        frame1 = Frame(root,height=500,width=150)
        frame2 = Frame(root,height=500,width=320)
        accessibleIP = Listbox(frame1,selectmode = BROWSE,height=28)
        fileList = Listbox(frame2,selectmode = BROWSE,height=26,width=43)
        accessibleIP.bind('<ButtonRelease-1>',connectIP)
        fileList.bind('<ButtonRelease-1>',openFile)
        
        sl = Scrollbar(frame1,orient=VERTICAL)
        sl1 = Scrollbar(frame2,orient=VERTICAL)
    
        
        returnBack = Button(frame2,text='返回')
       
    
        def init_ui(self):
    
            #root.attributes("-alpha",0.7)
            #root.attributes("-transparentcolor","blue")
            my_ui.mainFrame.pack(side='top')
    
            my_ui.label1.grid(row=0,column=0)
            my_ui.label2.grid(row=0,column=2)
        
            my_ui.firstIP.grid(row=0,column=1)
            my_ui.endIP.grid(row=0,column=3)
    
            my_ui.searchButton.grid(row=0,column=5)
            
            my_ui.returnBack.pack(side='bottom')
    
    
    
    
            my_ui.sl.pack(side='right',fill = Y)
            my_ui.sl1.pack(side='right',fill = Y)
            my_ui.accessibleIP.pack()
            my_ui.fileList.pack()
            my_ui.accessibleIP['yscrollcommand'] = my_ui.sl.set
            my_ui.sl['command'] = my_ui.accessibleIP.yview
            my_ui.fileList['yscrollcommand'] = my_ui.sl1.set
            my_ui.sl1['command'] = my_ui.fileList.yview
            
            my_ui.frame1.pack(side='left')
            my_ui.frame2.pack(side='right')
    
            root.mainloop()
            
ui = my_ui()
ui.init_ui()

#1.1.1.1

# 202.116.1.1
