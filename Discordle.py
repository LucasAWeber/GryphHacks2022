import discord
import os 
from keep_alive import keep_alive
from discord.ext import commands
import time
#import random


#opens file and saves words to discordle_words
file = open("DiscordleWordList.txt", "r")
discordle_words = file.readlines()
file.close()

daily_word_num = 0
      
my_secret = os.environ['TOKEN']
client = commands.Bot(command_prefix="!")#may change this to "Guess" or something****

# saves secret word which changes daily
# secretWord = discordle_words[random.randrange(1, len(discordle_words))]
secretWord = discordle_words[daily_word_num]
if (daily_word_num < len(discordle_words)-1):
  daily_word_num += 1
else:
  daily_word_num = 0

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.command()
async def embed(ctx):
  embedVar=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
  await ctx.channel.send(embed = embedVar)

#For wordle guesses
@client.event
async def on_message(message):
  list = []
  correctness = 0
  returnString = ''
  if message.author == client.user:
    return
  if(not message.content.startswith("!")):
    return
  string = message.content.lstrip();
  if(len(string) != len(secretWord)):
    await message.channel.send('Invalid guess : Wrong Length')
    return
  #if string is not in valid word string list

  #compare each character
  for i in range(len(string)):
    if(secretWord[i] == string[0]):
      list.append(':green_square: ')
      correctness+=1
    else:
      list.append(':black_large_square: ')
 

  #see if any character from message is in the secret word
  for i in range(len(string)):
    for j in range(len(string)):
      if(secretWord[i] == string[j]):
         if(not list[i] == ':green_square: '):
            list[i] == ':yellow_square: '
  
  returnString = ''.join(list)
  #if (correctness = len(string)):
    
  await message.channel.send(returnString)


#LEADERBOARD
@client.command()
async def add(ctx, *, newword):
  #ADD NEW PERSON TO LEADER BOARD
  server = ctx.guild.name.strip(' ')
  file = f'{server}_words.txt'
  f = open(file, "r+")
  Lines = f.readlines()
  for line in Lines:
    if(line[:-3] == newword):
      line[-1] = int(line[-1]) + 1
      f.close()
      return
  f.close()
  print(newword)
  f = open(file, "a")
  f.write(newword.strip())
  f.write('\n')
  f.close()
  newword.strip()
  await ctx.channel.send('Word added')
  return
