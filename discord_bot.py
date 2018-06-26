import discord
from discord.ext import commands
import os
import asyncio


TOKEN = ''
channel_ID = 460312060446638083
team_list = []
with open('Discord_token.txt', 'r') as token_file:
	TOKEN = token_file.read()
	print("Token is:", TOKEN)
with open("teams.txt") as textInfo:
    team_list = [line.split() for line in textInfo]

bot = commands.Bot(command_prefix='.')
"""Important - Assign teams as shown in the supporting file. Use ''-'' instead of spaces in team names, and keep one space between team number and team name """

""" on_ready reads the txt file into a 2D array team_list and prints it out into the console. """

@bot.event
async def on_ready():
    print(team_list)
    await bot.say('Team List Loaded')

""" setup reads the name of a team, creates a role and channel in the discord for that team. It does this for all the teams in the list. Also prints the team list with numbers in order."""

@bot.command(pass_context = True)
async def setup(ctx,message,team_list):
    for index in range(len(team_list)):
        role_name = team_list[index][1]
        await bot.create_role(ctx.message.server, name = role_name)
        await bot.send_message(ctx.message.channel, str(team_list[index][0] + ' ' + team_list[index][1]))
        await bot.create_channel(ctx.message.server, name = role_name, type=discord.ChannelType.voice)

""" im takes the member name and team number as input and assigns the member to the role corresponding to the team number given in setup."""

@bot.command(pass_context = True)
async def im(ctx,member, number, team_list):
    team_name = team_list[number-1][1]
    role = discord.utils.get(member.server.roles, name = team_name)
    await bot.add_roles(member, role)


bot.run(TOKEN)
