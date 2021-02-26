import discord
import os
import requests
import json
from random import choice
from replit import db
from keep_alive import keep_alive
from discord.ext import commands,tasks
import youtube_dl

client=discord.Client()


sad_words = ["sad","depressed","unhappy","angry","miserable","depressing","bitter", "dismal", "heartbroken" ,"melancholy" ,"mournful", "pessimistic" ,"somber", "sorrowful" ,"sorry" ,"wistful", "bereaved" ,"blue" ,"cheerless" ,"dejected", "despairing", "despondent", "disconsolate", "distressed" ,"doleful", "down", "down in dumps" ,"down in mouth", "downcast", "forlorn", "gloomy", "glum", "grief-stricken", "grieved" ,"heartsick", "heavyhearted", "hurting", "in doldrums" ,"in grief", "in the dumps" ,"languishing" ,"low", "low-spirited" ,"lugubrious", "morbid" ,"morose", "out of sorts" ,"pensive" ,"sick at heart", "troubled" ,"weeping" ,"woebegone","abasement", "abjection", "blahs" ,"bleakness" ,"bummer", "cheerlessness" ,"dejection", "desolation" ,"desperation" ,"despondency", "discouragement" ,"dispiritedness" ,"distress" ,"dole" ,"dolefulness" ,"dolor" ,"downheartedness" ,"dreariness", "dullness" ,"dumps", "ennui", "gloom", "gloominess" ,"heavyheartedness", "hopelessness" ,"lowness" ,"melancholia", "melancholy" ,"misery" ,"mortification" ,"qualm", "sadness", "sorrow" ,"trouble" ,"unhappiness", "vapors", "woefulness" ,"worry", "abjectness", "blue funk", "disconsolation" ,"heaviness of heart" ,"lugubriosity" ,"the blues"]
starter_encouragements=["Cheer up!","Hang in there","Chill","Life is beautiful","Hola","You got this.","Good luck today! I know you’ll do great.","Sending major good vibes your way.","I know this won’t be easy, but I also know you’ve got what it takes to get through it.","Hope you’re doing awesome!","Keep on keeping on!","Sending you good thoughts—and hoping you believe in yourself just as much as I believe in you.","Know how often I think of you? Always.","Lifting you up in prayer and hoping you have a better day today.","Keeping you close in my thoughts.","I’m thinking of you. And I’m just a text or phone call away.","I hope you don’t feel alone as you go through this time. My heartfelt thoughts and prayers are with you all the way.","Be good to yourself. And let others be good to you, too","This is what you’re going through, not who you are.","I hope you are surrounded by people who are good for your spirit.","You are amazing for facing this with so much courage and hope.","Wishing you healing around the next corner.","The most important thing right now is to focus on getting better… everything else can wait.","You’re doing exactly what you should be doing. Hang in there","You’re being so strong—and patient. Keep the faith. Things are going to start looking up soon","I know you’re body has definitely felt better, but how are your spirits holding up? I’ll be in touch to see if you want to talk, vent, rant, whatever.","I hope you feel your inner strength building day by day.","Life is tough, but you’re tougher.","I’m proud of you for walking this road, for doing what’s right for you.","You’re making a big change, and that’s a really big deal.","I know what you’re going through is hard, but I’m rooting for you every minute of every day.","Even when you might not feel it, you’ve got the strength to get through.","I can’t imagine how you feel. But I can listen when you need to talk.","Take everything one day at a time. And on the harder days, give me a call.","You’re being incredibly brave. I’m proud of you.","It takes serious courage to get on this path and stay on it. Good on you.","Stay strong and remember how many people care about you. (I’m one of them!)","Thinking of you—and trusting that this is just a stepping stone along the path to something better.","There’s no doubt in my mind that you’ll succeed in whatever path you choose next","With your brains and talent, I just know you’ll make a positive contribution wherever you go.","The next chapter of your life is gonna be so amazing.","Hearts take time to heal. Be gentle with yourself.","This totally sucks, but you totally don’t suck.","You are completely and unconditionally loved.","It’s okay not to be okay.","Your pain is valid. I’m here if you need someone to listen.","No wise words or advice here. Just me. Thinking of you. Hoping for you. Wishing you better days ahead.","I’m so sorry you’re experiencing a setback. I don’t know what to say, except that care about you, and I’m here for you.","We’ve got friends for our happiest days and saddest moments. I hope you know I’m your friend now just as much as ever.","If you ever need to talk, or just cry, I’m your gal.","Just wanted to send you a smile today.","I’m here. And I have wine.","If this didn’t make you smile, let me know, and I will send you my senior yearbook picture instead.","You can get through this. Take it from me. I’m very wise and stuff.","Sorry things are crappy. If you need somebody to binge-watch a whole season of something with you, I’m there.","This, too, shall pass. And hopefully not like a kidney stone.","I believe in you! And unicorns. But mostly you!","All this can be a lot to take on. I’m here to help, if you need it.","What’s especially challenging right now? We’d like to find a way to help with that.","I’m never more than a text or call away. Don’t hesitate to reach out. (I plan to check in on you, too.)","If you want company, I’m there.","I’m here for you no matter what—to talk, to run errands, to clean up, whatever is helpful","It’s okay to feel hurt, angry, scared, or however you’re feeling. It might seem impossible, but you won’t always feel the way you feel right now. And for now, I want to do whatever I can to help.","You may have lost the game, but you never gave up. That makes you a winner in my book."]

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
  change_status.start()
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
    embed=discord.Embed(colour=discord.Colour.orange())
    embed.set_author(name='Available Commands')
    embed.add_field(name='vpaInspire',value='Get a random inspiring quote!',inline=False)
    embed.add_field(name='vpaNew',value='Add your own custom encouraging message.\nex: vpaNew You are amazing.',inline=False)
    embed.add_field(name='vpaDel',value='Delete your custom encouraging message.\nex: vpaDel 1',inline=False)
    embed.add_field(name='vpaList',value='Lists all your added custom encouraging messages.',inline=False)
    embed.add_field(name='vpaResponding',value='Turns off/on bot\'s response to sad messages on the server \n ex: vpaResponding false',inline=False)
   
    await message.channel.send(embed=embed)
    
        
    
  if msg.startswith("vpaResponding"):
    value=msg.split("vpaResponding ",1)[1]

    if value.lower()=="true":
      db["responding"]=True
      await message.channel.send("Responding is on.")
    else:
      db["responding"]=False
      await message.channel.send("Responding is off.")
players={}
client1=commands.Bot(command_prefix='?')
status=['Music!','PUBG!','CSGO!','Apex Legends!','Fortnite!','Minecraft!','nothing|vpaHelp ']

  
@tasks.loop(seconds=20)
async def change_status():
  await client.change_presence(activity=discord.Game(choice(status)))
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to Overklock NITuk LTD. server!'
    )


keep_alive()
client.run(os.getenv('TOKEN'))