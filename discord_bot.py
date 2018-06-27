import discord
from discord.ext import commands
import os
import asyncio


TOKEN = 'NDYwNDIyNjg2OTUxMjExMDMw.DhQUSQ.YVgN_NI0GMZ--BVBm0AkmZN9VnQ'
channel_ID = 460422215851048992

team_list = []
channel_list = []
role_list = []
global server
global team_list


bot = commands.Bot(command_prefix=',')
client = discord.Client()

"""Important - Assign teams as shown in the supporting file. Use ''-'' instead of spaces in team names, and keep one space between team number and team name """

""" on_ready reads the txt file into a 2D array team_list and prints it out into the console. """

@client.event
async def on_ready():
    with open("teams.txt") as textInfo:
        team_list = [line.split() for line in textInfo]
        print(team_list)

@client.event
async def on_message(message):
    if message.content == '.setup':
        for index in range(len(team_list[0])):
            role_name = team_list[index][1]
            server = message.channel.server
            await client.create_role(ctx.member.server, name = role_name)
            await client.send_message(message.channel, str(team_list[index][0] + ' ' + team_list[index][1]))
            await client.create_channel(server, name = role_name, type=discord.ChannelType.voice)
    if message.content == '.ready':
        member_role_list = member.roles
        team_name = member_role_list[1]
        flag = False
        for index in range(len(team_list[0])):
            if team_name == team_list[index][1]:
                flag = True
                team_list[index][2] = True
                client.say('Team' + ' ' + str(team_name) + ' '+ 'is now ready!')
                print('Team' + ' ' + str(team_name) + ' '+ 'is now ready!')
                break
            if flag == False:
                client.say('Error readying up, ask a moderator for info.')

    if message.content == ".clear":
		logs = client.logs_from(message.channel)
        async for msg in logs:
			await client.delete_message(msg)

    if message.content == '.im':
        team_name = team_list[number-1][1]
        role = discord.utils.get(member.server.roles, name = team_name)
        await client.add_roles(member, role)

bot.run(TOKEN)
