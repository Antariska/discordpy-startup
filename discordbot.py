import discord, asyncio, datetime, re
from discord.ext import commands
from queue import Queue

import os
import traceback

# new event loop - DELETE LATER
loop = asyncio.new_event_loop()
asyncio.set_event_loop(asyncio.new_event_loop())


client = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


q = Queue()
edit_check = False


# on_ready
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    
    # define cutsom emojis
    global ra_x, ra_spl, ra_s, ra_a, ra_b
    ra_x = discord.utils.get(client.guilds[0].emojis, name='05ra_x')
    ra_spl = discord.utils.get(client.guilds[0].emojis, name='04ra_spl')
    ra_s = discord.utils.get(client.guilds[0].emojis, name='03ra_s')
    ra_a = discord.utils.get(client.guilds[0].emojis, name='02ra_a')
    ra_b = discord.utils.get(client.guilds[0].emojis, name='01ra_b')
    
    # define rank reactions
    global reactions_rank
    reactions_rank = (f"{ra_x}", f"{ra_spl}", f"{ra_s}", f"{ra_a}", f"{ra_b}")
    
    # runs timeout checks
    path = '/boshu_files'
    files = []
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            files.append(filename)
    timeout_files = []
    regex = re.compile(r'(_timeout.txt)$')
    for name in files:
        if regex.search(name):
            timeout_files.append(name)
    for timeout_file in timeout_files:
        with open(f"{path}/{timeout_file}") as open_timeout_file:
            raw_data = open_timeout_file.read()
        channel_id = int(raw_data[1: 19])
        channel = client.get_channel(channel_id)
        msg = await channel.fetch_message(int(timeout_file.strip('_timeout.txt')))
        timeout = datetime.datetime.strptime(raw_data[22: -2], '%Y-%m-%d %H:%M:%S.%f')
            
        if datetime.datetime.now() > timeout:
            await msg.add_reaction('🚫')
            

# on command
@client.command()
async def boshu(ctx, about = "募集", settime = 1):    # settime 24h, EDIT LATER
    settime = int(settime)
    
    # create an embed for the reaction list
    embed_body = discord.Embed(title=about, colour=0x728bd3)    # EDIT COLOUR LATER
    for reaction_rank in reactions_rank:
        embed_body.add_field(name=f"{reaction_rank} 0人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"🈴 全部で ０人 なう\n", value="\u200b", inline=True)
    embed_body.set_footer(text=f"ウデマエ (Ｘ/Ｓ+/Ｓ/Ａ/Ｂ) をリアクション追加で参加　🚫で中止　✖で削除　\
    \n⚠名前が反映されない場合はリアクションを付け直して下さい")    
    
    # bot sends the message
    msg = await ctx.send(embed=embed_body)
    
    # define cutsom emojis - UNNECESSARY?
    global ra_x, ra_spl, ra_s, ra_a, ra_b
    ra_x = discord.utils.get(msg.guild.emojis, name='05ra_x')
    ra_spl = discord.utils.get(msg.guild.emojis, name='04ra_spl')
    ra_s = discord.utils.get(msg.guild.emojis, name='03ra_s')
    ra_a = discord.utils.get(msg.guild.emojis, name='02ra_a')
    ra_b = discord.utils.get(msg.guild.emojis, name='01ra_b')
    
    # define rank reactions - UNNECESSARY?
    global reactions_rank
    reactions_rank = (f"{ra_x}", f"{ra_spl}", f"{ra_s}", f"{ra_a}", f"{ra_b}")
    
    # create a file with message.id as file name and message author.id as content
    with open(f"/boshu_files/{msg.id}.txt", 'w') as file:
        file.write(str(ctx.author.id))
    
    # create a file with timeout info
    with open(f"/boshu_files/{msg.id}_timeout.txt", 'w') as file:
        dic = {}
        dic[msg.channel.id] = str(datetime.datetime.now() + datetime.timedelta(days=settime))
        file.write(str(dic))


# on reaction add (raw)
@client.event
async def on_raw_reaction_add(payload):
    
    # define msg
    channel = client.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    
    # define cutsom emojis
    global ra_x, ra_spl, ra_s, ra_a, ra_b
    ra_x = discord.utils.get(msg.guild.emojis, name='05ra_x')
    ra_spl = discord.utils.get(msg.guild.emojis, name='04ra_spl')
    ra_s = discord.utils.get(msg.guild.emojis, name='03ra_s')
    ra_a = discord.utils.get(msg.guild.emojis, name='02ra_a')
    ra_b = discord.utils.get(msg.guild.emojis, name='01ra_b')
    
    # define rank reactions
    global reactions_rank
    reactions_rank = (f"{ra_x}", f"{ra_spl}", f"{ra_s}", f"{ra_a}", f"{ra_b}")
    
    # if the message is by bot and is active
    if msg.author.id == client.user.id and '🚫' in msg.embeds[0].footer.text:
        
        # define user
        user = client.get_user(payload.user_id)
        
        # define embed_body
        embed_body = msg.embeds[0]
        
        # if the added reaction is a rank
        if str(payload.emoji) in reactions_rank:
            
            # get index no for the field of the reactioned rank
            def index_no():
                if payload.emoji == ra_x:
                    return 0
                if payload.emoji == ra_spl:
                    return 1
                if payload.emoji == ra_s:
                    return 2
                if payload.emoji == ra_a:
                    return 3
                if payload.emoji == ra_b:
                    return 4
            
            async def r_add():
                
                global edit_check
                edit_check = True
                msg = await channel.fetch_message(payload.message_id)
                embed_body = msg.embeds[0]
                
                # add the user.name to the embed field - ERROR IF MULTIPLE REACTIONS AT THE SAME TIME
                if user.name in msg.embeds[0].fields[index_no()].value:
                    pass
                else:
                    if msg.embeds[0].fields[index_no()].value == "\u200b":
                        embed_body.set_field_at(index_no(), name=f"{payload.emoji} {len(msg.embeds[0].fields[index_no()].value.split())}人 なう\n", \
                                                value=str(msg.embeds[0].fields[index_no()].value + user.name), inline=True)
                    else:
                        embed_body.set_field_at(index_no(), name=f"{payload.emoji} {len(msg.embeds[0].fields[index_no()].value.split()) + 1}人 なう\n", \
                                                value=str(msg.embeds[0].fields[index_no()].value + f"\n{user.name}"), inline=True)
            
                # update the total field
                total = 0
                for ii in range(len(msg.reactions)):
                    total += msg.reactions[ii].count
                embed_body.set_field_at(5, name=f"🈴 全部で {total}人 なう\n", value="\u200b", inline=True)
            
                await msg.edit(embed=embed_body)
                edit_check = False
            
            global q, edit_check
            q.put(r_add())
            
            if edit_check == True:
                original_payload = payload
                try:
                    payload = await client.wait_for('raw_message_edit', check=lambda payload: payload.message_id == msg.id, timeout=1)
                except:
                    pass
                payload = original_payload
            else:
                pass
                
            await q.get()
            
            # remove all previous reactions by the user except the current reaction
            for i in range(len(msg.reactions)):
                users = await msg.reactions[i].users().flatten()
                if user.name in str(users) and msg.reactions[i].emoji != payload.emoji:
                    await msg.remove_reaction(msg.reactions[i].emoji, user)
        
        elif str(payload.emoji) == '🚫':
            
            # get command author
            file_path = str(f"/boshu_files/{payload.message_id}.txt")
            with open(file_path) as open_file:
                command_author_id = open_file.read()
                
            # stop vote function if command author
            if str(payload.user_id) == command_author_id or payload.user_id == client.user.id:
                
                await msg.clear_reactions()
                embed_body.set_footer(text="＝＝＝＝＝＝募集を中止しました＝＝＝＝＝＝")
                await msg.edit(embed=embed_body)
                os.remove(file_path)
                file_path_timeout = str(f"/boshu_files/{payload.message_id}_timeout.txt")
                os.remove(file_path_timeout)
                    
            else:
                pass
        
        elif str(payload.emoji) == '✖':
            
            # get command author
            file_path = str(f"/boshu_files/{payload.message_id}.txt")
            with open(file_path) as open_file:
                command_author_id = open_file.read()
                
            # delete msg if command author
            if str(payload.user_id) == command_author_id:
                    
                await msg.delete()
                os.remove(file_path)
                file_path_timeout = str(f"/boshu_files/{payload.message_id}_timeout.txt")
                os.remove(file_path_timeout)
                    
            else:
                pass
        
        else:
            
            # remove the reaction if not specified above 
            await msg.remove_reaction(payload.emoji, user)
        
    else:
        pass


# on reaction remove (raw)
@client.event
async def on_raw_reaction_remove(payload):
    
    # define msg
    channel = client.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    
    # define cutsom emojis
    global ra_x, ra_spl, ra_s, ra_a, ra_b
    ra_x = discord.utils.get(msg.guild.emojis, name='05ra_x')
    ra_spl = discord.utils.get(msg.guild.emojis, name='04ra_spl')
    ra_s = discord.utils.get(msg.guild.emojis, name='03ra_s')
    ra_a = discord.utils.get(msg.guild.emojis, name='02ra_a')
    ra_b = discord.utils.get(msg.guild.emojis, name='01ra_b')
    
    # define rank reactions
    global reactions_rank
    reactions_rank = (f"{ra_x}", f"{ra_spl}", f"{ra_s}", f"{ra_a}", f"{ra_b}")
    
    # if the message is by bot and is active
    if msg.author.id == client.user.id and '🚫' in msg.embeds[0].footer.text:
        
        # if the removed reaction is a rank
        if str(payload.emoji) in reactions_rank:
            
            # define user
            user = client.get_user(payload.user_id)
        
            # define embed_body
            embed_body = msg.embeds[0]
            
            # get index no for the field of the reactioned rank
            def index_no():
                if payload.emoji == ra_x:
                    return 0
                if payload.emoji == ra_spl:
                    return 1
                if payload.emoji == ra_s:
                    return 2
                if payload.emoji == ra_a:
                    return 3
                if payload.emoji == ra_b:
                    return 4
            
            async def r_remove():
                
                global edit_check
                edit_check = True
                msg = await channel.fetch_message(payload.message_id)
                embed_body = msg.embeds[0]
                
                # delete the user.name from the field - ERROR IF MULTIPLE REACTIONS AT THE SAME TIME
                if f"\n{user.name}" in msg.embeds[0].fields[index_no()].value:
                    embed_body.set_field_at(index_no(), name=f"{payload.emoji} {len(msg.embeds[0].fields[index_no()].value.split()) - 1}人 なう\n", \
                                            value=str(msg.embeds[0].fields[index_no()].value.replace(f"\n{user.name}", "")), inline=True)
                else:
                    if f"{user.name}\n" in msg.embeds[0].fields[index_no()].value:
                        embed_body.set_field_at(index_no(), name=f"{payload.emoji} {len(msg.embeds[0].fields[index_no()].value.split()) - 1}人 なう\n", \
                                                value=str(msg.embeds[0].fields[index_no()].value.replace(f"{user.name}\n", "")), inline=True)
                    else:
                        if user.name in msg.embeds[0].fields[index_no()].value:
                            embed_body.set_field_at(index_no(), name=f"{payload.emoji} {len(msg.embeds[0].fields[index_no()].value.split()) - 1}人 なう\n", \
                                                    value=str(msg.embeds[0].fields[index_no()].value.replace(user.name, "")), inline=True)        
                        else:
                            pass
            
                # update the total field
                total = 0
                for ii in range(len(msg.reactions)):
                    total += msg.reactions[ii].count
                embed_body.set_field_at(5, name=f"🈴 全部で {total}人 なう\n", value="\u200b", inline=True)
            
                await msg.edit(embed=embed_body)
                edit_check = False
            
            global q, edit_check
            q.put(r_remove())
            
            if edit_check == True:
                original_payload = payload
                try:
                    payload = await client.wait_for('raw_message_edit', check=lambda payload: payload.message_id == msg.id, timeout=1)
                except:
                    pass
                payload = original_payload
                    
            else:
                pass
                
            await q.get()
        
        else: 
            pass
    
    else:
        pass


# run the bot    
client.run(token)
