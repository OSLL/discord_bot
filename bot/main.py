import discord 
import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD = os.getenv("GUILD")

# print(type(my_token))

class MyClient(discord.Client):
    async def on_ready(self):
        print('Log: {0}'.format(self.user))
        for guild in client.guilds:
            if guild.name == GUILD:
                break

    async def on_message(self, message):
        # print(message)
        print('Message "{0.author}": {0.content}'.format(message))


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token=TOKEN)

