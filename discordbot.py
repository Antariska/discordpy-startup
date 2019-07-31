import discord, asyncio, ast
from collections import defaultdict

import os
import traceback


client = discord.Client()
token = os.environ['DISCORD_BOT_TOKEN']


# on bot ready
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    
# at command input
@client.event
async def on_message(message):
    if message.content.startswith('/boshu'):
        
        # dict to save user reaction info - move elsewhere ###############
        user_reaction_dic = defaultdict(dict)
    
        # creating the bot message
    
        # define custom emojis
        ra_x = discord.utils.get(message.guild.emojis, name='05ra_x')
        ra_spl = discord.utils.get(message.guild.emojis, name='04ra_spl')
        ra_s = discord.utils.get(message.guild.emojis, name='03ra_s')
        ra_a = discord.utils.get(message.guild.emojis, name='02ra_a')
        ra_b = discord.utils.get(message.guild.emojis, name='01ra_b')
    
        # create fields for reacted users
        embed_body = discord.Embed(title='募集',colour=0x728bd3)
        embed_body.add_field(name=f"{ra_x} 0人 なう\n", value="\u200b", inline=True)
        embed_body.add_field(name=f"{ra_spl} 0人 なう\n", value="\u200b", inline=True)
        embed_body.add_field(name=f"{ra_s} 0人 なう\n", value="\u200b", inline=True)
        embed_body.add_field(name=f"{ra_a} 0人 なう\n", value="\u200b", inline=True)
        embed_body.add_field(name=f"{ra_b} 0人 なう\n", value="\u200b", inline=True)
        embed_body.add_field(name=f"🈴 全部で ０人 なう\n", value="\u200b", inline=True)
        embed_body.set_footer(text=f"ウデマエ (Ｘ/Ｓ+/Ｓ/Ａ/Ｂ) をリアクション追加で参加　↩で取消　🚫で中止　✖で削除")
    
        
        #get the channel command was sent to and send the bot message
        channel = message.channel
        msg = await channel.send(embed=embed_body)
        
        # add reaction to the bot message as button - modify! ############
        await msg.add_reaction('↩')
        
        with open(f"/content/sample_data/{msg.id}.txt", 'w') as file:
            pass

        
@client.event
async def on_reaction_add(reaction, user):
    if user.bot == True:
        pass
    #elif message.id 
    else:
        channel.send(user)
        
        
# run the bot    
client.run(token)
