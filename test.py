import discord
from discord.ext import commands
import os
import asyncio


TOKEN = ''
channel_ID = 460312060446638083
server_id = 460312060446638081
team_list = [] #team_list is a list that contains lists. Each sublist contains two string elements, one for team number and one for team name
role_list = [] #list of role objects
channel_list = [] #list of newly created channels
global server

print(discord.__version__)
with open('Discord_token.txt', 'r') as token_file:
	TOKEN = token_file.read()
	print("Token is:", TOKEN)

with open("teams.txt") as textInfo:
	team_list = [line.split() for line in textInfo]
	print(team_list)


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
	if message.content == '.test1':
		for team in team_list:
			new_channel = await client.create_channel(server, team[1], type = discord.ChannelType.voice)
			await client.edit_channel(new_channel, user_limit = 4)
			channel_list.append(new_channel)
			new_role = await client.create_role(server, name = team[1])
			role_list.append(new_role)
			overwrite = discord.PermissionOverwrite()
			overwrite.connect = True
			overwrite.speak = True
			await client.edit_channel_permissions(new_channel, new_role, overwrite)

		await client.send_message(message.channel, 'Voice Channels Created')
	if message.content == ".clear":
		logs = client.logs_from(message.channel)
		async for msg in logs:
			await client.delete_message(msg)
	if message.content == ".permissiontest":
		for role in server.roles:
			print (role.name)
		channel = client.get_channel(str(461255128788238356))
	if message.content == ".delete_channels":
		for channel in channel_list:
			await client.delete_channel(channel)
		for role in role_list:
			await client.delete_role(server, role)



@client.event
async def on_ready():
	global server
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	server = client.get_server(str(460312060446638081))
	print(server)



client.run(TOKEN)