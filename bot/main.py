import discord 
from discord import utils

import config

# print(type(my_token))

class MyClient(discord.Client):
    async def on_ready(self):
        print('Log: {0}'.format(self.user))
        for guild in client.guilds:
            if guild.name == config.GUILD:
                break

    async def on_message(self, message):
        if message.channel.id == config.ADMIN_CHANEL_ID:
            channel = self.get_channel(message.channel.id) 
            message = await channel.fetch_message(message.id) 
            member = utils.get(message.guild.members, id=message.author.id)

            deleted_users = []

            if(len([i for i in member.roles if i.id in config.PRIVROLES]) >= 1):
                words = [i for i in message.content.split(' ') if i != '']
                if( words[0] == config.DELETE_COMAND and len(words) >= 0): 
                    for guild_member in message.guild.members:
                        #Check that user is not Admin
                        if(len([i for i in guild_member.roles if i.id in config.PRIVROLES]) == 0):
                            #Check user's roles
                            if(len([i for i in guild_member.roles if i.name in words[1:]])):
                                #Delete user
                                deleted_users.append(guild_member.name)
                                await guild_member.kick()
            print("[INFO] Delete users: {0}".format(" ".join(deleted_users)))
                


    async def on_member_join(self, member):
        guild = self.get_guild(member.guild.id)
        await member.add_roles(guild.get_role(config.NEWUSERROLE_ID))
        print("[INFO Added to {0} role {1}]".format(member, guild.get_role(config.NEWUSERROLE_ID)))

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.POST_ID:
            channel = self.get_channel(payload.channel_id) 
            message = await channel.fetch_message(payload.message_id) 
            member = utils.get(message.guild.members, id=payload.user_id)
            try:
                emoji = str(payload.emoji) 
                role = utils.get(message.guild.roles, id=config.ROLES[emoji])
                if(len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER or len([i for i in member.roles if i.id == config.ADMIN_ROLE]) == 1):
                    await member.add_roles(role)
                    print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('[ERROR] Too many roles for user {0.display_name}'.format(member))
            
            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))
    
    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id) # получаем объект канала
        message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
        member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
        try:
            emoji = str(payload.emoji) # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)

            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
 
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = MyClient(intents=intents)
client.run(token=config.TOKEN)

