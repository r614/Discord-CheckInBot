import discord
from discord.ext import commands
import os


TOKEN = ''
channel_ID = 460422215851048992


bot = commands.Bot(command_prefix='.')
"""Important - Assign teams as shown in the supporting file. Use ''-'' instead of spaces in team names, and keep one space between team number and team name """

with open("teams.txt") as textInfo:
        team_list = [line.split() for line in textInfo]
print(team_list)

@bot.event
async def on_ready():
    await bot.say('Bot is ready')

@bot.command(pass_context = True)
async def setup(ctx,message,team_list):
    for index in range(len(list)):
        role_name = team_list[index][1]
        await bot.create_role(ctx.message.server, name = role_name)
        await bot.send_message(ctx.message.channel, str(team_list[index][0] + ' ' + team_list[index][1]))
        await bot.create_channel(ctx.message.server, name = role_name, type=discord.ChannelType.voice)


@bot.command(pass_context = True)
async def im(ctx,member, number, team_list):
    team_name = team_list[number-1][1]
    role = discord.utils.get(member.server.roles, name = team_name)
    await bot.add_roles(member, role)


bot.run(TOKEN)
