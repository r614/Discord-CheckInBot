import discord
from discord.ext import commands
import os
import asyncio


TOKEN = ''
channel_ID = 460312060446638083
team_list = []

print(discord.__version__)
with open('Discord_token.txt', 'r') as token_file:
	TOKEN = token_file.read()
	print("Token is:", TOKEN)

with open("teams.txt") as textInfo:
	team_list = [line.split() for line in textInfo]

client = discord.Client()
bot = commands.Bot(command_prefix='.')
"""Important - Assign teams as shown in the supporting file. Use ''-'' instead of spaces in team names, and keep one space between team number and team name """

""" on_ready reads the txt file into a 2D array team_list and prints it out into the console. """

@client.event
async def on_message(message):
	global team_list
	if message.author == client.user:
		return
	if message.content == '.test':
		print(team_list)
		await client.send_message(message.channel,'Team List Loaded')
	if message.content == "who's the best":
		await client.send_message(message.channel,'ZerO is the best oniichan! oWo')
	if message.content == '.setup':
		for index in range(len(team_list)):
			role_name = team_list[index][1]
			await bot.create_role(ctx.message.server, name = role_name)
			await bot.send_message(ctx.message.channel, str(team_list[index][0] + ' ' + team_list[index][1]))
			await bot.create_channel(ctx.message.server, name = role_name, type=discord.ChannelType.voice)
		print('Done')
	if message.content == '.permission':
		channels = client.get_all_channels()
		await client.send_message(message.channel, channels)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)