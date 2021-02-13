import discord
from discord.ext import commands
import datetime
import os

botid = 809322014660624445
pinemojiid = 809454773786771497

commontxtroom = 808193078384787487
gametxtroom = 806358409460842519
commandstxtroom = 806358409460842520
hwtxtroom = 808193962128572436
updatestxtroom = 809454664017641542

class MyClient(commands.Bot):
    async def on_ready(self):
        print('~~~~bot is online~~~~')
        channel = self.get_channel(updatestxtroom)
        async for message in channel.history(limit=None):
            if message.content.find('has change status from') != -1:
                await message.delete()

    async def on_member_update(self ,beforemember, aftermember):
        if beforemember.bot == False and beforemember.status != aftermember.status:
            channel = self.get_channel(updatestxtroom)
            await channel.send(content=f'{beforemember.name} has change status from {beforemember.status} to {aftermember.status}!', delete_after=600)

    
    async def on_reaction_add(self, reaction, member):
        if reaction.emoji.id == pinemojiid:
            time = datetime.datetime.utcnow()
            await reaction.message.pin()
            msgs = await reaction.message.channel.history(after=time).flatten()
            for msg in msgs:
                if msg.type == discord.MessageType.pins_add and msg.author.id == botid:
                    await msg.delete()

    async def on_raw_reaction_remove(self, payload):
        if payload.emoji.id == pinemojiid:
            channel = discord.utils.get(self.get_all_channels(), id=payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            await msg.unpin()

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.messages = True
client = MyClient(intents=intents, command_prefix='.')

@client.command()
async def clear(ctx, args: int):
    async for msgs in ctx.history(limit=args):
        await msgs.delete()

client.run(os.getenv("DISCORD_BOT_TOKEN"))