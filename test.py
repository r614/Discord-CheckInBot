##################################################
#  WRITTEN BY MIKE YUE                           #
#  JUNE 25TH 2018                                #
#  DISCORD BOT FOR UBC OPERATION CHICKEN DINNER  #
##################################################


import discord
from discord.ext import commands
import os
import asyncio


TOKEN = ''
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


###########################################
#  Is this machine learning?              # 
#  Or is it just a bunch of if statements #
#  Should refactor this code later on tbh #
###########################################

@client.event
async def on_message(message):
	global team_list
	#Makes sure bot can't reply to itself
	if message.author == client.user:
		return

	#Testing purposes, no longer required
	if message.content == '.test':
		print(team_list)
		await client.send_message(message.channel,'Team List Loaded')

	#Bot LucidiT is a weeb
	if message.content == "who's the best":
		await client.send_message(message.channel,'ZerO is the best oniichan! oWo')


	#Roshan's code. IDK what it's supposed to do but it doesn't work
	if message.content == '.setup':
		for index in range(len(team_list)):
			role_name = team_list[index][1]
			await bot.create_role(ctx.message.server, name = role_name)
			await bot.send_message(ctx.message.channel, str(team_list[index][0] + ' ' + team_list[index][1]))
			await bot.create_channel(ctx.message.server, name = role_name, type=discord.ChannelType.voice)
		print('Done')

	#Creates new Channels and Roles in the server, naming them after the team names provided in the team_list document
	#Modifies: role_list, channel_list
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

	#Clears all text messages from the text channel that called .clear
	if message.content == ".clear":
		logs = client.logs_from(message.channel)
		async for msg in logs:
			await client.delete_message(msg)
	
	#Deletes all Channels and Roles in the role_list and channel_list, but doesn't modify the lists themselves
	#Make sure to call .test1 to populate channel_list and role_list before you call this function, otherwise it won't work
	#In other words, if you want to delete the roles and channels fast, make sure your bot doesn't DC or quit in between creating and deleting the channels/roles
	if message.content == ".delete_channels":
		for channel in channel_list:
			await client.delete_channel(channel)
		for role in role_list:
			await client.delete_role(server, role)


	#Lists all the roles in the server other than Server Admin, Tournament Admin, and @everyone 
	if message.content == ".roles":
		role_names = []
		for role in server.roles:
			role_names.append(role.name)
		role_names.pop(0)
		role_names.pop(0)
		role_names.pop(0)
		await client.send_message(message.channel,role_names)

	#Assigns roles to people who type in messages with the format: I am: _______
	# Doesn't allow them to be Tournament or Server Admin
	# Every user starts with 1 role, the @everyone role
	# Currently only accepts one other role, need to change that cuz that's outdated
	if message.content.lower().startswith("i am:"):
		role_mapping_dict = {}
		split_entry = message.content.split(":")
		role_to_add = split_entry[1].strip()
		print(role_to_add)
		print(message.author)
		if(role_to_add == 'Server Admin' or role_to_add == 'Tournament Admin' or role_to_add == 'v'):
			await client.send_message(message.channel,'Not Allowed to access these roles')
			return
		for role in server.roles:
			role_mapping_dict[role.name] = role

		if(len(message.author.roles) >= 2):
			print(len(message.author.roles))
			if(role_to_add == 'Team Captain'):
				if(len(message.author.roles) == 2):
					await client.add_roles(message.author, role_mapping_dict[role_to_add])
					await client.send_message(message.channel,'You have been added to your role')
					return
			await client.send_message(message.channel,'Cannot have more than 2 roles')
			return
		#print(server.roles)

		print(role_mapping_dict)
		if role_to_add in list(role_mapping_dict.keys()):
			await client.add_roles(message.author, role_mapping_dict[role_to_add])
			await client.send_message(message.channel,'You have been added to your role')
		else:
			await client.send_message(message.channel,'That role does not exist')




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