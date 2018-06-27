##################################################
#  WRITTEN BY MIKE YUE                           #
#  JUNE 25TH 2018                                #
#  DISCORD BOT FOR UBC OPERATION CHICKEN DINNER  #
##################################################


import discord
from discord.ext import commands
import os
import asyncio
import random

TOKEN = ''
server_id = 460312060446638081
team_list = [] #team_list is a list that contains lists. Each sublist contains two string elements, one for team number and one for team name
better_team_list = []
role_list = [] #list of role objects
channel_list = [] #list of newly created channels
cancer_list = [] #list of cancer spam 
team_checkin_status = {}
role_mapping_dict = {}
global server

fidget_spinner_cancer = 'if my girl👧😍and fidget spinner߷ both dying😱and I can only save one 😤😬catch me at her funeral 😔👻🌹spinning ߷ through ߷ the ߷ pain ߷ 💯 😎'
breed_cancer = '😍Guys😍, I’m 😲shaking😲. I’m fucking😲 shaking😲. I never wanted to 👉👌🍆🍑breed 🍑🍆👉👌with anyone more than I want to with 🎃👻Halloween 👻✝️Mercy.✝️🎃️ That 💯perfect,💯 ⏳curvy ⏳😍body.😍 Those 😍bountiful😍 🍈breasts🍈. The 👪child 👪bearing😍 hips😍 of a 🖼️💐literal goddess💐🖼️. It honestly fucking 😳😳hurts😳😳 knowing that I’ll never❤👅💋mate ❤👅💋with her, ⬆pass⬆ my 👖genes👖 through her, and have her 👑birth👑 a set of 👪💯perfect offspring.💯👪 I’d do fucking💰💰💰 ANYTHING 💰💰'
fish_cancer = ' Do✋ not 😰 eat 👌 fish 🐟 after 😶 u 😯 drink water 🍺 bc 😰 it can 👻 swim in 🏊 ur stomach 😮 and u will 😲 feel 😕 gulugulu in ur stomach 😓😳😼'
dank_cancer = '🔊🔊🚨🚨WARNING🔊🚨🚨WARNING🚨🚨🔊THIS IS A 🐸DANK 👽MEME❗❗ 🐸ALERT. INCOMING 🐸DANK 👽MEME🐸 👐👌HEADING STRAIGHT 🚀🚀YOUR WAY. 🔜👆👆👆PLEASE TAKE ANY PRECAUTIONS🚧🚧 NECESSARY TO PREPARE YOURSELF FOR THIS 🐸DANK 👽MEME❗❗ 🐸 🌋🌋🌋 .BUCKLE UP♿♿♿ THEM SEATBELTS👮👮,PUT THEM CELLPHONES ON SILENT📵📵 AND LOOSEN THAT ANUS👅👅🍑🍑🍑🍩🍩💩💩 CUZ THIS MEME JUST CAME STRAIGHT OUT OF THE 🚬🚬 🍁🏭🍁🏭🍁🚬🚬DANK FACTORY.'

cancer_list.append(fidget_spinner_cancer)
cancer_list.append(breed_cancer)
cancer_list.append(fish_cancer)
cancer_list.append(dank_cancer)

print(discord.__version__)
with open('Discord_token.txt', 'r') as token_file:
	TOKEN = token_file.read()
	print("Token is:", TOKEN)

with open("teams.txt") as textInfo:
	team_list = [line.split() for line in textInfo]
	print(team_list)


client = discord.Client()

bot = commands.Bot(command_prefix='.')

for team in team_list:
	team_checkin_status[team[1]] = u"\U0000274C\n"
	better_team_list.append(team[1])
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

	#Creates new Channels and Roles in the server, naming them after the team names provided in the team_list document
	#Modifies: role_list, channel_list
	if message.content == '.init_channels_and_roles' and message.channel.name == 'discord-set-up':
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

		for role in server.roles:
			role_mapping_dict[role.name] = role

		await client.send_message(message.channel, 'Voice Channels Created')

	#Clears all text messages from the text channel that called .clear
	if message.content == ".clear":
		logs = client.logs_from(message.channel)
		async for msg in logs:
			await client.delete_message(msg)
	
	#Creates dictionaries for both the newly updated roles and channels, using their names as the key and associating the actual role/channel object as the value
	#Better_team_list is the list of all teams from the txt file
	#If a team name present in the better_team_list matches a role/channel name, then that role/channel gets deleted
	if message.content == ".delete_channels_and_roles" and message.channel.name == 'discord-set-up':
		channel_dict = {}
		role_dict = {}
		channels = server.channels
		roles = server.roles
		for channel in channels:
			channel_dict[channel.name] = channel
		for role in roles:
			role_dict[role.name] = role
		for team in better_team_list:
			if (team in list(channel_dict.keys())):
				await client.delete_channel(channel_dict[team])
				await client.delete_role(server, role_dict[team])
		await client.send_message(message.channel, "Done deleting channels")

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
	# Allows only one team role, plus a Team Captain role if applicable
	# The V role will be manually assigned by Tournament Admins
	if message.content.lower().startswith("i am:") and message.channel.name == 'role-request':
		split_entry = message.content.split(":")
		role_to_add = split_entry[1].strip()
		print(role_to_add)
		print(message.author)
		if(role_to_add == 'Server Admin' or role_to_add == 'Tournament Admin' or role_to_add == 'v'):
			await client.send_message(message.channel,'Not Allowed to access these roles')
			return

		if(len(message.author.roles) >= 2):
			if(role_to_add == 'Team Captain'):
				if(len(message.author.roles) == 2):
					await client.add_roles(message.author, role_mapping_dict[role_to_add])
					await client.send_message(message.channel,'You have been added to your role')
					return
			if(len(message.author.roles) == 2):
				if(message.author.roles[1].name == 'Team Captain'):
					await client.add_roles(message.author, role_mapping_dict[role_to_add])
					await client.send_message(message.channel,'You have been added to your role')
					return					
			await client.send_message(message.channel,'I cannot do that. Beep Boop')
			return
		#print(server.roles)

		if role_to_add in list(role_mapping_dict.keys()):
			await client.add_roles(message.author, role_mapping_dict[role_to_add])
			await client.send_message(message.channel,'You have been added to your role')
		else:
			await client.send_message(message.channel,'That role does not exist')

	if message.content == '.setup' and message.channel.name == 'check-in':
		team_checkin = ""
		
		for team_key in list(team_checkin_status.keys()):
			team_checkin = team_checkin + team_key + ":    " + team_checkin_status[team_key]
		await client.send_message(message.channel, team_checkin)

	if message.content == ".cancer":
		index = random.randint(0, 3)
		await client.send_message(message.channel, cancer_list[index])

	if message.content.startswith('.checkin') and message.channel.name == 'check-in':
		is_captain = False;
		has_team = False;
		if(len(message.author.roles) != 3 and len(message.author.roles) != 4):
			print(len(message.author.roles))
			await client.send_message(message.channel, "Not authorized to checkin for your team")
			return
		for role in message.author.roles:
			if (role.name == 'Team Captain'):
				is_captain = True
			if (role.name in list(team_checkin_status.keys())):
				has_team = True
				team_name = role.name

		if (is_captain == True and has_team == True):
			team_checkin = ''
			team_checkin_status[team_name] = u"\U00002705\n"
			logs = client.logs_from(message.channel)
			async for msg in logs:
				if u"\U0000274C\n" in msg.content:
					edit_message = msg
			for team_key in list(team_checkin_status.keys()):
				team_checkin = team_checkin + team_key + ":    " + team_checkin_status[team_key]
			await client.edit_message(edit_message, team_checkin)
		else:
			await client.send_message(message.channel, "You are not the Captain or you do not have a team role")


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