import discord
import os
import requests 
import json 
import random
from replit import db

from keep_alive import keep_alive

Drink_names = ["beer", "vine", "vodka", "alcohol", "booze"]



booze_lines = ["booze heads chattering again...", "You drunks are going to stink the whole server with booze!", "Not again...", "Even a glass of water would be better.", "I am out of words."]


client = discord.Client()



def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - Diona. Genshin Impact"
  return quote


def update_lines(new_line):
  if "normal_lines" in db.keys():
    normal_lines = db["normal_lines"]
    normal_lines.append(new_line)
    db["normal_lines"] = normal_lines
  else:
    db["normal_lines"] = [new_line]
  
def update_links(new_link):
  if "links" in db.keys():
    links = db["links"]
    links.append(new_link)
    db["links"] = links
  else:
    db["links"] = [new_link]

  
def delete_lines(index):
  normal_lines = db["normal_lines"]
  if len(normal_lines) > index:
    del normal_lines[index]
    db["normal_lines"] = normal_lines

def delete_links(index):
  links = db["links"]
  if len(links) > index:
    del links[index]
    db["links"] = links

@client.event
async def on_ready():
  print('logged in as {0.user}'.format(client))


@client.event
async def on_message(msg):


  if msg.author == client.user:
   return

  if msg.content.startswith('$hi Diona'):
    await msg.channel.send("Diona, bartender of the Cat's Tail! I charge a hefty fee for private events. Huh? You didn't come here for a drink? Hmm... Then I accept your invitation... I suppose...")
  if msg.content.startswith('$Diona of the field, what is your wisdom?'):
    await msg.channel.send(get_quote())

  
  if any (word in msg.content for word in Drink_names):
    await msg.channel.send(random.choice(booze_lines))


  if msg.content.startswith("$new"):
    new_line = msg.content.split("$new ",1)[1]
    if "https://" in new_line :
      update_links(new_line)
      await msg.channel.send("New link added.")
    else :  
      update_lines(new_line)
      await msg.channel.send("New line  added.")

  if msg.content.startswith("$del line "):
    normal_lines = []
    if "normal_lines" in db.keys():
      index = int(msg.content.split("$del",1)[1])
      delete_lines(index)
      normal_lines = db["normal_lines"]
    await msg.channel.send(normal_lines)
  
  if msg.content.startswith("$del link "):
    links = []
    if "links" in db.keys():
      index = int(msg.content.split("$del",1)[1])
      delete_lines(index)
      links = db["links"]
    await msg.channel.send(links)

  if msg.content.startswith('$Hey Diona, say something'):
    normal_lines = db['normal_lines']
    await msg.channel.send(random.choice(normal_lines))


  if msg.content.startswith('$Hey Diona, pass me a clip'):
    links = db['links']
    await msg.channel.send(random.choice(links))

  if msg.content.startswith("$list lines"):
    normal_lines = []
    if "normal_lines" in db.keys():
      normal_lines = db["normal_lines"]
    await msg.channel.send(normal_lines)

  if msg.content.startswith("$list lines"):
    links = []
    if "links" in db.keys():
      links = db["links"]
    await msg.channel.send(links)

keep_alive()
client.run(os.getenv('BROKEN'))