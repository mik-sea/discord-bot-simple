# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands, tasks
import random
import config
import platform,os,asyncio
import datetime

description = '''Just Simple bot Sea'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=str(config.prefix), description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    status_task.start()
    print("Presence start")
    print("-------------------")

@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Setup the game status task of the bot.
    """
    statuses = ["with you!", "with Her!", "with GF!"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

@bot.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix

    :param message: The message that was sent.
    """
    if message.author == bot.user or message.author.bot:
        return

    if message.content.startswith('!hello'):
        await message.reply('Hai!', mention_author=True)
    if message.content.startswith('!editme'):
        msg = await message.channel.send('10')
        await asyncio.sleep(3.0)
        await msg.edit(content='40')

    await bot.process_commands(message)

async def on_message_edit(self, before, after):
    msg = f'**{before.author}** edited their message:\n{before.content} -> {after.content}'
    await before.channel.send(msg)

@bot.event
async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'Welcome {member.mention} to {guild.name}!'
    await guild.system_channel.send(to_send)


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


# @bot.command()
# async def joined(ctx, member: discord.Member):
#     """Says when a member joined."""
#     await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

# @bot.command(aliases=["info"])
# async def about(self, ctx):
#     """ About the bot """
#     # ramUsage = self.process.memory_full_info().rss / 1024**2
#     # avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)

#     embedColour = None
#     # current_date = datetime.date.today()

#     print(self)
#     if hasattr(self, "guild") and self.guild is not None:
#         embedColour = self.me.top_role.colour

#         embed = discord.Embed(colour=embedColour)
#         embed.set_thumbnail(url=self.bot.user.avatar)
#         embed.add_field(
#             name="Last boot",
#             value= "str(current_date)"
#         )
#         embed.add_field(
#             name="Developer",
#             value=str(self.bot.get_user(
#                 self.bot.config.discord_owner_id
#             ))
#         )
#         # embed.add_field(name="Library", value="discord.py")
#         # embed.add_field(name="Servers", value=f"{len(self.bot.guilds)} ( avg: {avgmembers:,.2f} users/server )")
#         # embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]))
#         # embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB")

#         await ctx.send(content=f"i About **{self.bot.user}**", embed=embed)


bot.run(config.botToken)