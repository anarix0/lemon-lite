import discord, os, tracemalloc, asyncio, random
from discord.ext import commands
from discord import app_commands

prefix = ".."

class Client(commands.Bot):

  def __init__(self):
    intents = discord.Intents.default()
    intents.message_content = True
    super().__init__(command_prefix="..", intents=intents)

  async def setup_hook(self):
    await self.tree.sync(guild=discord.Object(id=1026546107314090075))
    print("Synced!")

  async def on_ready(self):
    print("Ready!")
    await client.change_presence(activity=discord.Game(name="error*404"))
    client.loop.create_task(status_task())


async def status_task():
  servers = len(client.guilds)
  members = 0
  for guild in client.guilds:
    members += guild.member_count - 0
  while True:
    servers =  servers * 1
    members = members * 1
    await client.change_presence(activity=discord.Game(name="with the API"))
    await asyncio.sleep(10)
    await client.change_presence(activity=discord.Activity(
      type=discord.ActivityType.watching, name=f'{servers} guilds'))
    await asyncio.sleep(10)
    await client.change_presence(activity=discord.Activity(
      type=discord.ActivityType.watching, name=f'{members} users'))
    await asyncio.sleep(5)
    await client.change_presence(activity=discord.Activity(
      type=discord.ActivityType.listening, name="..data"))
    await asyncio.sleep(10)
    await client.change_presence(activity=discord.Activity(
      type=discord.ActivityType.listening, name="..cdm"))
    await asyncio.sleep(5)


client = Client()

tracemalloc.start()


@client.event
async def on_message(message):
  msg = message
  ctx = await client.get_context(message)
  if msg.content == prefix + "data":
    await ctx.channel.purge(limit=1)
    if message.author.guild_permissions.administrator:
      file = discord.File(f'data/{message.guild.id}.txt')
      await ctx.author.send(file=file)
      embed = discord.Embed(title="<:accept:1027930036659032214> Data file has been send in DM's", color=0x5865f2)
      await ctx.send(
        ephemeral=True,
        embed=embed,
        delete_after=5)
  else:
    if msg.content == prefix + "cdm":
      await ctx.channel.purge(limit=1)
      dmchannel = await ctx.author.create_dm()
      async for message in dmchannel.history(limit=100):
        if message.author == client.user:
          await message.delete()
      embed = discord.Embed(title="<:review:1027930035027460146> DM's have been cleared", color=0x5865f2)
      await ctx.send(ephemeral=True,
                     embed=embed,
                     delete_after=5)
    else:
      if message.author.id == client.user.id or message.author:
        return
      else:
        if message.content == "..data" or message.content == "..cdm":
          return
        else:
          with open("data.txt", "a") as n:
            n.write(
              f"\n{str(msg.guild.id)} , S. , {str(msg.author)} , {str(msg.created_at.strftime('%Y-%m-%d %H:%M:%S'))} : {msg.content}"
            )
          with open(f"data/{message.guild.id}.txt", "a") as n:
            n.write(
              f"\nS. , {str(msg.author)} , {str(msg.created_at.strftime('%Y-%m-%d %H:%M:%S'))} : {msg.content}"
            )


# message loggers

# on message delete
@client.event
async def on_message_delete(message):
  msg = message
  if message.author.id == client.user.id:
    return
  else:
    with open(f"data/{message.guild.id}.txt", "a") as n:
      n.write(f"\nD. , {str(msg.author)} , {str(msg.created_at.strftime('%Y-%m-%d %H:%M:%S'))} : {msg.content}")

# on message edit
@client.event
async def on_message_edit(message_before, message_after):
  msg_a = message_after
  msg_b = message_before
  if message_before.author.id == client.user.id:
    return
  else:
    with open(f"data/{msg_b.guild.id}.txt", "a") as n:
      n.write(f"\nE. , {str(msg_a.author)} , {str(msg_a.created_at.strftime('%Y-%m-%d %H:%M:%S'))} | B. : {msg_b.content} | A. : {msg_a.content}")

@client.event
async def on_guild_join(guild):
  if guild.system_channel:
    embed = discord.Embed(title=f"Thank you for adding me to {guild.name}!",
                          color=0x6470ff)
    embed.add_field(name="Main command", value="**..data**", inline=False)
    embed.add_field(name="Clear DM's", value="**..cdm**", inline=False)
    embed.add_field(name="When I get kicked",
                    value="data file resets.",
                    inline=False)
    embed.set_footer(
      text=
      "By adding me to this server you agree to have some of your server messages saved for unknown time due to nukes."
    )
    await guild.system_channel.send("", embed=embed)
    f = open(f"data/{guild.id}.txt", "w")
    with open(f"data/{guild.id}.txt", "a") as n:
      n.write("This is the start of the data file for " + guild.name)
    print(f"Created /data/{guild.id}.txt")
    file = discord.File(f'data/{guild.id}.txt')
    await guild.system_channel.send("", file=file)


@client.event
async def on_guild_remove(guild):
  os.remove(f'data/{guild.id}.txt')
  print(f"Removed /data/{guild.id}.txt")

@client.hybrid_command(name="cleardata",
                       with_app_command=True,
                       description="Clear main data info")
@app_commands.guilds(discord.Object(id=1026546107314090075))
@commands.is_owner()
async def cleardata(ctx):
  file = discord.File(f'data.txt')
  await ctx.author.send(file=file)
  filec = open(id + '.txt', 'r+')
  filec.truncate(0)
  filec.close()
  print("Cleared /" + id + ".txt")
  await ctx.send("Data file has been cleared, and the last save was sent.",
                 ephemeral=True,
                 delete_after=5)


@client.hybrid_command(name="cdm",
                       with_app_command=False,
                       description="Clear data info")
@app_commands.guilds(discord.Object(id=1026546107314090075))
@commands.is_owner()
async def cdm(ctx):
  dmchannel = await ctx.author.create_dm()
  async for message in dmchannel.history(limit=100):
    if message.author == client.user:
      await message.delete()
  await ctx.send("DM's have been cleared", ephemeral=True)


client.run('token')
