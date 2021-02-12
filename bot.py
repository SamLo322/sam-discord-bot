import discord
import datetime
import os

botid = 809322014660624445
pinemojiid = 809454773786771497

commontxtroom = 808193078384787487
gametxtroom = 806358409460842519
commandstxtroom = 806358409460842520
hwtxtroom = 808193962128572436
updatesroom = 809454664017641542


class MyClient(discord.Client):
    async def on_ready(self):
        print('~~~~bot is online~~~~')
        channel = self.get_channel(commandstxtroom)
        await channel.send('Hello! How can I help you?')

    async def on_member_update(self ,beforemember, aftermember):
        if beforemember.bot == False and beforemember.status != aftermember.status:
            channel = self.get_channel(updatesroom)
            await channel.send(f'{beforemember.name} has change status from {beforemember.status} to {aftermember.status}!')
    
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


client = MyClient(intents=intents)
client.run(os.getenv("DISCORD_BOT_TOKEN"))