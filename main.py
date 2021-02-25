import discord
import os
import requests
import json
import random
from replit import db

client=discord.Client()


sad_words = ["sad","depressed","unhappy","angry","miserable","depressing","nigga","fuck"]
starter_encouragements=["Cheer up!","Hang in there","Chill","Life is beautiful","Hola"]

if "responding" not in db.keys():
  db["responding"]= True
def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys(): 
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]=encouragements
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragements(index):
  encouragements=db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index] 
    db["encouragements"]=encouragements
@client.event
async def on_ready():
  print('We have logged in as {0.user}'
  .format(client))

@client.event 
async def on_message(message):
  if message.author == client.user: 
    return
  msg=message.content
  if message.content.startswith('vpaInspire'):
    quote=get_quote()
    await message.channel.send(quote)
  if db["responding"]:
    options=starter_encouragements
    if "encouragements" in db.keys():
      options =options +db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("vpaNew"):
    encouraging_message=msg.split("vpaNew ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")
  if msg.startswith("vpaDel"):
    encouragements=[]
    if "encouragements" in db.keys():
      index=int(msg.split("vpaDel",1)[1])
      delete_encouragements(index)
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("vpaList"):
    encouragements=[]
    if "encouragements" in db.keys():
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)
  if msg.startswith("vpaHelp"):
    await message.channel.send("Available Commands")
    await message.channel.send("vpaInspire::")
    await message.channel.send("Get a random inspiring quote")
    await message.channel.send("vpaNew::")
    await message.channel.send("Add your own custom encouraging message.")
    await message.channel.send("ex: vpaNew You are amazing.")
    await message.channel.send("vpaDel::")
    await message.channel.send("Delete your custom encouraging message.")
    await message.channel.send("ex: vpaDel 1")
    await message.channel.send("vpaList::")
    await message.channel.send("Lists all your added custom encouraging messages.")
    await message.channel.send("vpaResponding::")
    await message.channel.send("Turns off/on bot's response to sad messages on the server")
    await message.channel.send("ex: vpaResponding false")
    
    
    
    
    
    
    
    
    
    
    
    
    
  if msg.startswith("vpaResponding"):
    value=msg.split("vpaResponding ",1)[1]

    if value.lower()=="true":
      db["responding"]=True
      await message.channel.send("Responding is on.")
    else:
      db["responding"]=False
      await message.channel.send("Responding is off.")
client.run(os.getenv('TOKEN'))