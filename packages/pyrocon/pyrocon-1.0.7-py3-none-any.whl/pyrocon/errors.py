from pyrogram.types import ForceReply
import asyncio
import logging

class errors:
   class timeout:
     code,text,anon,cancel,unknown,cquery,basic = 100,None,False,False,False,False,False 
     timeout = error = "[100] Time Out!"
   class anon:
     code,text,timeout,cancel,unknown,cquery,basic = 101,None,False,False,False,False,False 
     anon = error = "[101] Anonymous users can't be used this module...!"
   class cancel:
     code,text,timeout,anon,unknown,cquery,basic = 102,None,False,False,False,False,False 
     cancel = error = "[102] Listening cancelled...!"
   class unknown:
     code,text,timeout,anon,cancel,cquery,basic = 103,None,False,False,False,False,False 
     error = unknown = "[103] Unknown Error...!"
   class cquery:
     code,text,timeout,anon,cancel,unknown,basic = 104,None,False,False,False,False,False 
     error = cquery = "[104] Expected a callback query...!"
   class basic:
      error = basic = "Parameter type Invalid check again...!"
      code,text,timeout,anon,cancel,cquery,unknown = 105,None,False,False,False,False,False
         