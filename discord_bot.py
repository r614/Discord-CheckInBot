##################################################
#  WRITTEN BY MIKE YUE                           #
#  JUNE 25TH 2018                                #
#  DISCORD BOT FOR UBC OPERATION CHICKEN DINNER  #
##################################################


import discord
import os
import asyncio
import random

global setup_already

TOKEN = ''
server_id = 460312060446638081
team_list = [] #team_list is a list that contains lists. Each sublist contains two string elements, one for team number and one for team name
better_team_list = [] #List that contains all the team names
cancer_list = [] #list of cancer spam 
team_checkin_status = {}
role_mapping_dict = {}
setup_already = False
global server



print(discord.__version__)


with open('Discord_token.txt', 'r') as token_file:
    TOKEN = token_file.read()
    print("Token is:", TOKEN)

with open("teams.txt") as textInfo:
    team_list = [line.split() for line in textInfo]
    print(team_list)


client = discord.Client()

for team in team_list:
    team_checkin_status[team[1]] = u"\U0000274C\n"
    better_team_list.append(team[1])


###########################################
#  Is this machine learning?              # 
#  Or is it just a bunch of if statements #
#  Should refactor this code later on tbh #
###########################################

@client.event
async def on_message(message):
    global team_list

    #########################################
    #  Makes sure bot can't reply to itself #
    #########################################
    if message.author == client.user:
        return

    #####################################################################################
    #  Function: Creates new Channels and Roles in the server                           #
    #            naming them after the team names provided in the team_list document    #
    #            Makes sure that the limit is 4 users per Voice Channel                 #
    #            Only works if typed into the discord-set-up channel                    #
    #  Modifies: role_mapping_dict                                                      #
    #  Returns: Nothing. Merely modifies the Discord Server                             #
    #####################################################################################
    if message.content == '.init_channels_and_roles' and message.channel.name == 'discord-set-up':
        for team in team_list:
            new_channel = await client.create_channel(server, team[1], type = discord.ChannelType.voice)
            await client.edit_channel(new_channel, user_limit = 4)
            new_role = await client.create_role(server, name = team[1])
            overwrite = discord.PermissionOverwrite()
            overwrite.connect = True
            overwrite.speak = True
            await client.edit_channel_permissions(new_channel, new_role, overwrite)

        for role in server.roles:
            role_mapping_dict[role.name] = role

        await client.send_message(message.channel, 'Voice Channels and Team Roles Created')


    #################################################################################
    #  Function: Clears all text messages from the text channel that called .clear  #
    #  Modifies: Nothing                                                            #
    #  Returns: Nothing                                                             #
    #################################################################################
    if message.content == ".clear":
        global setup_already
        logs = client.logs_from(message.channel)
        setup_already = False
        async for msg in logs:
            await client.delete_message(msg)
    
    #########################################################################################################
    #  Function: Creates dictionaries for both the newly updated roles and channels,                        #
    #            using their names as the key and associating the actual role/channel object as the value   #
    #            Compares the keys in the dictionaries with the team names in better_team_list              #
    #            And deletes any channels and roles that match the team names                               #
    #            Only works if typed into the discord-set-up channel                                        #
    #  Modifies: Nothing                                                                                    #
    #  Returns: Nothing                                                                                     #
    #########################################################################################################
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
        await client.send_message(message.channel, "Done deleting channels and roles")

    ###########################################################################################################
    #  Function: Lists all the roles in the server other than Server Admin, Tournament Admin, and @everyone   #
    #  Modifies: Nothing                                                                                      #
    #  Returns: Nothing                                                                                       #
    ###########################################################################################################
    if message.content == ".roles":
        role_names = []
        for role in server.roles:
            role_names.append(role.name)
        role_names.pop(0)
        role_names.pop(0)
        role_names.pop(0)
        await client.send_message(message.channel,role_names)

    ##############################################################################################
    #  Function: Assigns roles to people who type in messages with the format: I am: _______     #
    #            Doesn't allow them to be Tournament or Server Admin                             #
    #            Every user starts with 1 role, the @everyone role                               #
    #            Allows only one team role, plus a Team Captain role if applicable               #
    #            The V role will be manually assigned by Tournament Admins                       #
    #            Only works in the role-request channel                                          #
    #  Modifies: role_mapping_dict                                                               #
    #  Returns: Nothing                                                                          #
    ##############################################################################################
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

    #########################################################################################################
    #  Function: Prints out all the teams and their respective ready statuses                               #
    #            It does this via the dictionary team_checkin_status                                        #
    #            It associates the team name with the team's ready status, which defaults to not ready      #
    #            Then prints each dict key-value pair out                                                   #
    #            If .setup has already been called, it will not do anything                                 #
    #            Only works in the check-in channel                                                         #
    #  Modifies: team_checkin_status, setup_already                                                         #
    #  Returns: Nothing                                                                                     #
    #########################################################################################################
    if message.content == '.setup' and message.channel.name == 'check-in':
        if(setup_already == False):
            team_checkin = "Team Check-in Status\n"
            
            for team_key in list(team_checkin_status.keys()):
                team_checkin = team_checkin + team_key + ":    " + team_checkin_status[team_key]
            setup_already = True
            await client.send_message(message.channel, team_checkin)
        else:
            await client.send_message(message.channel, ".setup command has already been called")

    #########################################################################################
    #  Function: Allows team captains to checkin for their team                             #
    #            Only allows valid users to checkin for their team                          #
    #            Valid users must possess both a valid team role and a Team Captain Role    #
    #            Only if both conditions are satisifed will this command work               #
    #            Only works in the check-in channel                                         #
    #  Modifies: team_checkin_status                                                        #
    #  Returns: Nothing                                                                     #
    #########################################################################################
    if message.content == ('.checkin') and message.channel.name == 'check-in':
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
            team_checkin = 'Team Check-in Status\n'
            team_checkin_status[team_name] = u"\U00002705\n"
            logs = client.logs_from(message.channel)
            async for msg in logs:
                if u"\U0000274C\n" in msg.content or u"\U00002705\n" in msg.content:
                    edit_message = msg
            for team_key in list(team_checkin_status.keys()):
                team_checkin = team_checkin + team_key + ":    " + team_checkin_status[team_key]
            await client.edit_message(edit_message, team_checkin)
        else:
            await client.send_message(message.channel, "You are not the Captain or you do not have a team role")


    #########################################################################################
    #  Function: Allows team captains to uncheckin for their team                           #
    #            Only allows valid users to uncheckin for their team                        #
    #            Valid users must possess both a valid team role and a Team Captain Role    #
    #            Only if both conditions are satisifed will this command work               #
    #            Only works in the check-in channel                                         #
    #  Modifies: team_checkin_status                                                        #
    #  Returns: Nothing                                                                     #
    #########################################################################################
    if message.content == ('.uncheckin') and message.channel.name == 'check-in':
        is_captain = False;
        has_team = False;
        if(len(message.author.roles) != 3 and len(message.author.roles) != 4):
            print(len(message.author.roles))
            await client.send_message(message.channel, "Not authorized to uncheckin for your team")
            return
        for role in message.author.roles:
            if (role.name == 'Team Captain'):
                is_captain = True
            if (role.name in list(team_checkin_status.keys())):
                has_team = True
                team_name = role.name

        if (is_captain == True and has_team == True):
            team_checkin = 'Team Check-in Status\n'
            team_checkin_status[team_name] = u"\U0000274C\n"
            logs = client.logs_from(message.channel)
            async for msg in logs:
                if u"\U0000274C\n" in msg.content or u"\U00002705\n" in msg.content:
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
