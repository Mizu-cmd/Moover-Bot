import discord
from discord.ext import commands
import json
from decouple import config

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    return prefixes[str(message.guild.id)]

def get_channel(client, message):
    with open('channels.json', 'r') as f:
        channels = json.load(f)
    
    return channels[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)
token = config('DISCORD_BOT_TOKEN')
client.remove_command("help")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game("Mooving peoples"))
    
@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        
    with open('channels.json', 'r') as f:
        channels = json.load(f)
    
    prefixes[str(guild.id)] = '.'
    channels[str(guild.id)] = {}
    
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    with open('channels.json', 'w') as f:
        json.dump(channels, f, indent=4)
        
@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    with open('channels.json', 'r') as f:
        channels = json.load(f)
    
    prefixes.pop(str(guild.id))
    channels.pop(str(guild.id))
    
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    with open('channels.json', 'w') as f:
        json.dump(channels, f, indent=4)

@client.command()
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    prefixes[str(ctx.guild.id)] = prefix
    
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
        
    embedVar = discord.Embed(title=f"Successfully changed prefix to {prefix}", color=0x2ecc71)
    await ctx.send(embed=embedVar)

@client.command()
async def help(ctx):
    await ctx.send("Hello !!")

@client.command()
async def setchannel(ctx, game, channel):
    with open('channels.json', 'r') as f:
        channels = json.load(f)
        
    guild = ctx.guild.id
    channels[str(guild)][game] = channel

        
    with open("channels.json", "w") as file:
        json.dump(channels, file, indent=4)

    embedVar = discord.Embed(title=f"Successfully added the channel {channel} to {game}", color=0x2ecc71)
    await ctx.send(embed=embedVar)

@client.command()
async def removechannel(ctx, game):
    with open('channels.json', 'r') as f:
        channels = json.load(f)
        
    guild = ctx.guild.id
    channels[str(guild)].pop(game)

        
    with open("channels.json", "w") as file:
        json.dump(channels, file, indent=4)

    embedVar = discord.Embed(title=f"Successfully remove the channel {game}", color=0x2ecc71)
    await ctx.send(embed=embedVar)
    
@client.event
async def on_member_update(before, after):
    
    try:
        if after.voice.channel:  
            with open('channels.json', 'r') as f:     
                channels = json.load(f)
            if not str(after.activity) in channels[str(after.guild.id)]: return
            await after.move_to(client.get_channel(int(channels[str(after.guild.id)][str(after.activity)])))
    except:
        print()

client.run(token)
client.add_command(changeprefix)