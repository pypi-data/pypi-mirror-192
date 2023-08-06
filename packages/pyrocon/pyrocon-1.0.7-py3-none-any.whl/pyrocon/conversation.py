from pyrogram.types import ForceReply
import asyncio
import logging
from .errors import errors
from pyrogram import Client
from pyrogram.types import Message

class quiz:
  async def ask(client,update,ask,timeout=30,cquery=False,stop_cmd = "/cancel",placeholder = "Send required information...",msg_limit=80):
     if not str(type(client)) == """<class 'pyrogram.client.Client'>""":
        print("First parameter/c must be pyrogram Client object")
        return errors.basic
     if not str(type(cquery)) == """<class 'bool'>""":
        print("Fifth parameter/cquery must be Boolean (True or False)")
        return errors.basic
     if ((not cquery) and (not str(type(update)) == """<class 'pyrogram.types.messages_and_media.message.Message'>""")) or (cquery and (not str(type(update)) == """<class 'pyrogram.types.bots_and_keyboards.callback_query.CallbackQuery'>""")):
        if cquery:
         print("Second parameter/msg must be CallbackQuery object")
         return errors.basic
        else:
         print("Second parameter/msg must be Message object")
         return errors.basic      
     if not str(type(ask)) == """<class 'str'>""":
        print("Third parameter/ask must be str")
        return errors.basic
     if not str(type(timeout)) == """<class 'int'>""":
        print("Fourth parameter/timeout must be Integer")
        return errors.basic
     if not str(type(stop_cmd)) == """<class 'str'>""":
        print("Sixth parameter/stop_cmd must be str")
        return errors.basic
     if not str(type(placeholder)) == """<class 'str'>""":
        print("Seventh parameter/placeholder must be str")
        return errors.basic     
     try:
      ans = await asyncio.wait_for(quiz.wait(client,update,ask,placeholder,msg_limit,stop_cmd,cquery),timeout= timeout)
     except Exception as e:
      logging.info("Time Out!")
      ans = errors.timeout
     return ans      
  async def wait(c,msg,ask,placeholder,msg_limit,stop_cmd,cquery):
   try:
     user_id = msg.from_user.id    
   except Exception as e:
     logging.info(e)
     user_id = None
   if user_id:
    if cquery:
     uv = await c.send_message(msg.message.chat.id,ask,reply_markup=ForceReply(selective=True, placeholder=placeholder))
    else:
     uv = await msg.reply(ask,reply_to_message_id = msg.id,reply_markup=ForceReply(selective=True, placeholder=placeholder))
    while True:
     try:
      ids = [uv.id+x for x in range(msg_limit)]
      for ans in (await c.get_messages(uv.chat.id,ids)):
        ans.error = errors.unknown
        try:
          user_id2 = ans.from_user.id
        except:
         user_id2 = "Nonne"
        if ans and (not ans.empty) and (ans.text == stop_cmd) and (user_id2 == user_id):
           ans = errors.cancel
           break
        if ans and (not ans.empty) and ans.text and (user_id2 == user_id):
           ans.error = ans.cancel = ans.timeout = ans.anon = ans.unknown= False
           break
      if (not ans.error) or (ans == errors.cancel):
       break
     except Exception as e:
      logging.info(e)
      break
    return ans
   else:
    return errors.anon