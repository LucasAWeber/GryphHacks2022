import os
import discord
from discord.ext import commands
from discord.ext import tasks
TOKEN = ('OTc3MzU2MDk1ODYzNTMzNjU4.GmtZ4z.tkzsNvqioKhr61AeUm8IwbGg_bYEs0WLcR3HNI')

client = discord.Client()
client = commands.Bot(command_prefix=".")

# opens file and saves words to discordle_words
file = open("DiscordleWordList.txt", "r")
discordle_words = file.read().splitlines()
file.close()

daily_word_num = 0
solved = False
secretWord = 'hello'
solver = None

# should loop every 24 hours and send msg plus change word hopefully
@tasks.loop(hours=0.1)
async def new_word():
    # saves secret word which changes daily
    # secretWord = discordle_words[random.randrange(1, len(discordle_words))]
    global solved
    global secretWord
    global daily_word_num
    global discordle_words
    solved = False
    secretWord = discordle_words[daily_word_num]
    if (daily_word_num < len(discordle_words) - 1):
        daily_word_num += 1
    else:
        daily_word_num = 0

    list = []

    for i in range(len(secretWord)):
        list.append(':black_large_square: ')

    returnString = ''.join(list)

    channel = client.get_channel(918946892002492426)
    await channel.send(f'New daily Discordle today has {len(secretWord)} letters')
    await channel.send(f'{returnString} ')


@client.event
async def on_ready():
    new_word.start()
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    present = False
    global solved
    global secretWord
    global solver
    list = []
    returnString = ''
    if message.author == client.user:
        return
    if (not message.content.startswith("!")):
        return
    if (message.content == "!leaderboard"):
        server = message.guild.name.strip(' ')
        lines = open(f'{server}_leaderboard.txt', 'r').readlines()
        loop = 10
        if (len(lines) < 10):
            loop = len(lines)
        for i in range(loop):
            returnString = returnString + f'{i+1}. {lines[i]}'
        await message.channel.send(f'```{returnString}```')
        return
    if solved:
        await message.channel.send(f'Today\'s Discordle has already been solved by {solver} :tada:')
        return
    string = message.content[1:]
    await message.channel.send(string)
    print(f'{string} is the guessed word\n{secretWord} is the secret word\n')
    if (len(string) != len(secretWord)):
        await message.channel.send('Invalid guess : Wrong Length')
        return
    # if string is not in valid word string list

    # compare each character
    for i in range(len(string)):
        if (secretWord[i] == string[i]):
            list.append(':green_square: ')
        else:
            list.append(':black_large_square: ')

    # see if any character from message is in the secret word
    for i in range(len(string)):
        for j in range(len(string)):
            if (secretWord[j] == string[i]):
                if (list[i] != ':green_square: '):
                    list[i] = ':yellow_square: '

    for k in range(len(string)):
        countS = 0
        countSW = 0
        if (list[k] == ':yellow_square: '):
            for l in range(len(string)):
                if (string[k] == secretWord[l]):
                    countSW = countSW + 1
                if (string[k] == string[l] and list[l] != ':black_large_square: '):
                    countS = countS + 1
        if (countS > countSW):
            list[k] = ':black_large_square: '
    returnString = ''.join(list)
    await message.channel.send(returnString)
    counter = 0
    for i in list:
        if (i == ':green_square: '):
            counter = counter + 1
    if (counter == len(string)):
        solver = message.author.name
        await message.channel.send(f'Today\'s Discordle has been solved by {message.author.mention} :tada:')
        solved = True
        lineNum = -1
        server = message.guild.name.strip(' ')
        file = f'{server}_leaderboard.txt'
        f = open(file, "r+")
        Lines = f.readlines()
        f.close()
        for line in Lines:
            lineNum = lineNum + 1
            if (line[:-3] == message.author.name):
                print(f"{line[:-3]} = {message.author.name}")
                replace_line(file, lineNum, f"{line[:-2]}{int(line[-2]) + 1}\n")
                present = True
                return
        if (not present):
            f = open(file, 'a')
            f.write(f"{message.author.name} {1}\n")
            f.close()


def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


# LEADERBOARD
@client.command()
async def add(ctx, *, newword):
    # ADD NEW PERSON TO LEADER BOARD
    server = ctx.guild.name.strip(' ')
    file = f'{server}_words.txt'
    f = open(file, "r+")
    Lines = f.readlines()
    for line in Lines:
        if (line[:-3] == newword):
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


client.run(TOKEN)
