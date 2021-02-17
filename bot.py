import discord
from discord.ext import commands
import datetime
import os
import requests
from bs4 import BeautifulSoup

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
            if message.content.find('has change status from') != -1 and message.author.id == botid:
                await message.delete()

    async def on_member_update(self ,beforemember, aftermember):
        if beforemember.bot == False and beforemember.status != aftermember.status:
            channel = self.get_channel(updatestxtroom)
            await channel.send(content=f'{beforemember.name} has change status from {beforemember.status} to {aftermember.status}!', delete_after=300)

    
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.id == pinemojiid:
            time = datetime.datetime.utcnow()
            channel = discord.utils.get(self.get_all_channels(), id=payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            await msg.pin()
            msgs = await channel.history(after=time).flatten()
            for msgloop in msgs:
                if msgloop.type == discord.MessageType.pins_add and msgloop.author.id == botid:
                    await msgloop.delete()

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
    if args > 100:
        await ctx.send('you cannot clear more than 100 messages in a role.')
    else:
        list = []
        async for msg in ctx.history(limit=args+1):
            list.append(msg)
        await ctx.channel.delete_messages(list)

@client.command()
async def send(ctx, args: int):
    for i in range(1, args+1):
        await ctx.send(i)

@client.command()
async def lol(ctx, args):
    mainlist=['top', 'jg', 'ap', 'ad', 'sup']
    if args in mainlist:
        all = requests.get('https://na.op.gg/champion/statistics')
        soup = BeautifulSoup(all.text, 'html.parser')
        if args == mainlist[0]:
            role = soup.findAll('tbody')[0]
            embed = discord.Embed(title=mainlist[0] + ' champs', color=0x03f8fc, timestamp= ctx.message.created_at)
        elif args == mainlist[1]:
            role = soup.findAll('tbody')[1]
            embed = discord.Embed(title=mainlist[1] + ' champs', color=0x03f8fc, timestamp= ctx.message.created_at)
        elif args == mainlist[2]:
            role = soup.findAll('tbody')[2]
            embed = discord.Embed(title=mainlist[2] + ' champs', color=0x03f8fc, timestamp= ctx.message.created_at)
        elif args == mainlist[3]:
            role = soup.findAll('tbody')[3]
            embed = discord.Embed(title=mainlist[3] + ' champs', color=0x03f8fc, timestamp= ctx.message.created_at)
        elif args == mainlist[4]:
            role = soup.findAll('tbody')[4]
            embed = discord.Embed(title=mainlist[4] + ' champs', color=0x03f8fc, timestamp= ctx.message.created_at)            
        count = 0
        list=[]
        for i in role.findAll('tr'):
            champ = role.findAll('tr')[count]
            rank = champ.findAll('td', class_='champion-index-table__cell champion-index-table__cell--rank')[0]
            finalrank = rank.string
            name = champ.findAll('div', class_='champion-index-table__name')[0]
            finalname = name.string
            wrate = champ.findAll('td', class_='champion-index-table__cell champion-index-table__cell--value')[0]
            finalwrate = wrate.string
            prate = champ.findAll('td', class_='champion-index-table__cell champion-index-table__cell--value')[1]
            finalprate = prate.string
            tmp = champ.findAll('img')[1]
            tier = tmp['src']
            finaltier = tier[-5]
            list.append((finalname, finalrank, finalwrate, finalprate, finaltier))
            count += 1
        for finalname, finalrank, finalwrate, finalprate, finaltier in list:
                embed.add_field(name=f'**{finalname}**', value=f'> rank: {finalrank}\n> winrate: {finalwrate}\n> pickrate: {finalprate}\n> tier: {finaltier}',inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('pls type [top/ jg/ ap/ ad/ sup] after \'lol\' to clarify your role.')

client.run(os.getenv("DISCORD_BOT_TOKEN"))