from pyrogram.types import ForceReply
import asyncio
import logging

class pyrocon:
  async def ask(c,msg,ask,timeout=30,stop_cmd = "/cancel",placeholder = "Send required information...",msg_limit=150):
     try:
      ans = await asyncio.wait_for(pyrocon.wait(c,msg,ask,placeholder,msg_limit,stop_cmd),timeout= timeout)
     except Exception as e:
      logging.info("Time Out!")
      ans = pyrocon.serrors.timeout
     return ans
  class serrors:
     class timeout:
       code,text,anon,cancel = 100,None,False,False
       timeout = error = "[100] Time Out!"
     class anon:
       code,text,timeout,cancel = 101,None,False,False
       anon = error = "[101] Anonymous users can't be used this module...!"
     class cancel:
       code,text,timeout,anon = 102,None,False,False
       cancel = error = "[102] Listening cancelled...!"
      
  async def wait(c,msg,ask,placeholder,msg_limit,stop_cmd):
   try:
     user_id = msg.from_user.id
   except Exception as e:
     logging.info(e)
     user_id = None
   if user_id:
    uv = await msg.reply(ask,reply_to_message_id = msg.id,reply_markup=ForceReply(selective=True, placeholder=placeholder))
    while True:
     try:
      ids = [uv.id+x for x in range(msg_limit)]
      for ans in (await c.get_messages(uv.chat.id,ids)):
        ans.error = True
        try:
          user_id2 = ans.from_user.id
        except:
         user_id2 = "Nonne"
        if ans and (not ans.empty) and (ans.text == stop_cmd) and ans.reply_to_message and (user_id2 == user_id) and (ans.reply_to_message.id == uv.id) and ans.reply_to_message.reply_markup and ans.reply_to_message.reply_markup.placeholder and (ans.reply_to_message.reply_markup.placeholder == placeholder):
         ans = pyrocon.serrors.cancel
         break
        if ans and (not ans.empty) and ans.text and ans.reply_to_message and (user_id2 == user_id) and (ans.reply_to_message.id == uv.id) and ans.reply_to_message.reply_markup and ans.reply_to_message.reply_markup.placeholder and (ans.reply_to_message.reply_markup.placeholder == placeholder):
         ans.error = ans.cancel = ans.timeout = ans.anon = False
         break
      if (not ans.error) or (ans == pyrocon.serrors.cancel):
       break
     except Exception as e:
      logging.info(e)
      break
    return ans
   else:
    return pyrocon.serrors.anon 
