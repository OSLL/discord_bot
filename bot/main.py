import discord 
from discord import utils

import config


class MyClient(discord.Client):

# Start bot log
    async def on_ready(self):
        print('Log: {0}'.format(self.user))
        for guild in client.guilds:
            if guild.name == config.GUILD:
                try:
                    channel = guild.get_channel(config.ADMIN_CHANEL_ID)
                except Exception as e:
                    print("[ERROR] Admin chanel not found")

                try:
                    guild.get_role(config.ADMIN_ROLE)
                except Exception as e:
                    print("[ERROR] Admin role not found!")
                
                try:
                    for role in config.PRIVROLES :guild.get_role(role)
                except Exception as e:
                    print("[ERROR] Privelege roles not found!")

                try:
                    new_user_role = guild.get_role(config.NEWUSERROLE_ID)
                except Exception as e:
                    print("[ERROR] New User role not found!")
                
                try:
                    for key in config.ROLES.keys() :guild.get_role(config.ROLES[key])
                except Exception as e:
                    print("[ERROR] Add roles not found!")

                try:
                    for role in config.EXCROLES :guild.get_role(role)
                except Exception as e:
                    print("[ERROR] Exc role not found!")
                
                break

        try:
            await channel.send("[INFO] BOT RUN")
            await channel.send("[INFO] For delete action send '{0} <role name>' in {1}".format(config.DELETE_COMAND, channel.name))
            await channel.send("[INFO] After JOIN user will get the role {0}".format(new_user_role.name))

        except Exception as e:
            print("[ERROR] Permission denied") 



# Delete function
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
                await channel.send("[INFO] Delete users: {0}".format(" ".join(deleted_users)))
                

# Get ROLE on member join
    async def on_member_join(self, member):
        guild = self.get_guild(member.guild.id)
        await member.add_roles(guild.get_role(config.NEWUSERROLE_ID))
        await self.get_channel(config.ADMIN_CHANEL_ID).send("[INFO Added to {0} role {1}]".format(member, guild.get_role(config.NEWUSERROLE_ID)))

# Get ROLE on memeber add reaction 
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
                    await self.get_channel(config.ADMIN_CHANEL_ID).send('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    await self.get_channel(config.ADMIN_CHANEL_ID).send('[ERROR] Too many roles for user {0.display_name}'.format(member))
            
            except KeyError as e:
                await self.get_channel(config.ADMIN_CHANEL_ID).send('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))

 # Remove ROLE on memeber remove reaction    
    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id) 
        member = utils.get(message.guild.members, id=payload.user_id) 
        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])

            await member.remove_roles(role)
            await self.get_channel(config.ADMIN_CHANEL_ID).send('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
 
        except KeyError as e:
            await self.get_channel(config.ADMIN_CHANEL_ID).sendnt('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = MyClient(intents=intents)
client.run(token=config.TOKEN)

