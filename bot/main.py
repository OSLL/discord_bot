import discord 
from discord import utils

import config

from dotenv import load_dotenv

# print(type(my_token))

class MyClient(discord.Client):
    async def on_ready(self):
        print('Log: {0}'.format(self.user))
        for guild in client.guilds:
            if guild.name == config.GUILD:
                break

    async def on_message(self, message):
        # print(message)
        print('Message "{0.author}": {0.content}'.format(message))


    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.POST_ID:
            channel = self.get_channel(payload.channel_id) 
            message = await channel.fetch_message(payload.message_id) 
            member = payload.member
            
            try:
                emoji = str(payload.emoji) 
                print(emoji)
                role = utils.get(message.guild.roles, id=config.ROLES[emoji])
                print(role)
                if(len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
                    await member.add_roles(role)
                    print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('[ERROR] Too many roles for user {0.display_name}'.format(member))
            
            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))
    

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token=config.TOKEN)

