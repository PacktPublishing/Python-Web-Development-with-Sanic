from nextcord.client import Client
from nextcord.message import Message

client = Client()


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")
