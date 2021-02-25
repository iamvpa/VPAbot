import discord
import os
import requests
import json

client=discord.Client()

def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
@client.event
async def on_ready():
  print('We have logged in as {0.user}'
  .format(client))

@client.event 
async def on_message(message):
  if message.author == client.user: 
    return

  if message.content.startswith('vpa'):
    await message.channel.send('Hello!')

client.run(os.getenv('TOKEN'))