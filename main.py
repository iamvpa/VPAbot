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
    await message.channel.send("Available Commands:
    vpaInspire::
    Get a random inspiring quote
    vpaNew::
    Add your own cuustom encouraging message.
    ex: vpaNew You are amazing.
    vpaDel::
    Delete your custom encouraging message.
    ex: vpaDel 1
    vpaList::
    Lists all your added custom encouraging messages.
    vpaResponding::
    Turns off/on bot's response to sad messages on the server
    ex: vpaResponding false")
  if msg.startswith("vpaResponding"):
    value=msg.split("vpaResponding ",1)[1]

    if value.lower()=="true":
      db["responding"]=True
      await message.channel.send("Responding is on.")
    else:
      db["responding"]=False
      await message.channel.send("Responding is off.")
client.run(os.getenv('TOKEN'))