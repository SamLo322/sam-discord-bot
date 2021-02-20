import discord
from discord.ext import commands
import datetime
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request

botid = 809322014660624445
pinemojiid = 809454773786771497
commontxtroom = 808193078384787487
gametxtroom = 806358409460842519
commandstxtroom = 806358409460842520
hwtxtroom = 808193962128572436
updatestxtroom = 809454664017641542

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")
chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome"
driver = webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver", options=chrome_options)
driver.set_window_size(1920, 1080)


class MyClient(commands.Bot):
    async def on_ready(self):
        print('~~~~bot is online~~~~')
        channel = self.get_channel(updatestxtroom)
        async for message in channel.history(limit=None):
            if message.content.find('has change status from') != -1 and message.author.id == botid:
                await message.delete()

    async def on_member_update(self, beforemember, aftermember):
        if beforemember.bot == False and beforemember.status != aftermember.status:
            channel = self.get_channel(updatestxtroom)
            await channel.send(
                content=f'{beforemember.name} has change status from {beforemember.status} to {aftermember.status}!',
                delete_after=300)

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
    await ctx.message.delete()
    if args > 100:
        await ctx.send('you cannot clear more than 100 messages in a role.')
    else:
        list = []
        async for msg in ctx.history(limit=args):
            list.append(msg)
        await ctx.channel.delete_messages(list)


@client.command()
async def send(ctx, args: int):
    for i in range(1, args + 1):
        await ctx.send(i)


@client.command()
async def lol(ctx, args):
    await ctx.message.delete()
    async with ctx.typing():
        soup = BeautifulSoup(requests.get('https://tw.op.gg/champion/statistics').text, 'html.parser')
        mainlist = ['top', 'jg', 'ap', 'ad', 'sup']
        champlist = []
        for name in soup.findAll('div', class_='champion-index__champion-item__name'):
            champlist.append(name.string)
        if args.lower() in mainlist:
            role = soup.findAll('tbody')[mainlist.index(args)]
            embed = discord.Embed(title=args.upper() + ' champs (request by ' + ctx.author.name + ')', color=0x03f8fc,
                                  timestamp=ctx.message.created_at)
            checkindex = -1
            for champ in role.findAll('tr'):
                name = champ.findNext('div', class_='champion-index-table__name').string
                rank = champ.findNext('td', class_='champion-index-table__cell--rank').string
                wrate = champ.findNext('td', class_='champion-index-table__cell--value').string
                prate = champ.findAll('td', class_='champion-index-table__cell--value')[1].string
                tier = champ.findAll('img')[1]['src'][-5]
                link = champ.findNext('a')['href']
                embed.add_field(name=f'**{name}**',
                                value=f'> Rank: {rank} Tier: {tier}\n> Winrate: {wrate}\n> Pickrate: {prate}\n> [{name}\'s details](https://tw.op.gg{link})',
                                inline=True)
                checkindex += 1
                if (len(embed) > 6000 or checkindex == 24):
                    embed.remove_field(checkindex)
                    await ctx.send(embed=embed, delete_after=1200)
                    embed.clear_fields()
                    embed.add_field(name=f'**{name}**',
                                    value=f'> Rank: {rank} Tier: {tier}\n> Winrate: {wrate}\n> Pickrate: {prate}\n> [{name}\'s details](https://tw.op.gg{link})',
                                    inline=True)
                    checkindex = 0
            await ctx.send(embed=embed, delete_after=1200)

        elif args.capitalize() in champlist:
            name = args.lower()
            driver.get('https://tw.op.gg/champion/' + name + '/statistics/')
            imgurl = 'https://samlo-discord-request.herokuapp.com/sam_discord/img/' + name
            urllib.request.urlretrieve(imgurl, "items.png")
            driver.execute_script("document.querySelector(\".sc-fznyAO.cWTQXI.BeaconFabButtonFrame\").outerHTML = \"\"")
            ele = driver.find_element(By.CSS_SELECTOR,
                                      '.champion-overview__table.champion-overview__table--summonerspell')
            ele.screenshot('spells.png')
            ele = driver.find_elements_by_css_selector('.tabWrap._recognized')[2]
            ele.screenshot('runes.png')
            await ctx.send(name + '\'s statistics request by ' + ctx.author.name, delete_after=1200)
            await ctx.send(file=discord.File('spells.png'), delete_after=1200)
            await ctx.send(file=discord.File('items.png'), delete_after=1200)
            await ctx.send(file=discord.File('runes.png'), delete_after=1200)

        else:
            await ctx.send('pls type [top/ jg/ ap/ ad/ sup] after \'lol\' to clarify your role.', delete_after=60)


client.run(os.getenv("DISCORD_BOT_TOKEN"))
