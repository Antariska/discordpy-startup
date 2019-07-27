import discord, asyncio, ast
from discord.ext import commands
from collections import defaultdict

import os
import traceback


client = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


# on bot ready
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


# at command input
@client.command()
async def boshu(ctx, about = "募集"):
    
    # dict to save user reaction info
    user_reaction_dic = defaultdict(dict)
    
    # creating the bot message
    
    # define custom emojis
    ra_x = discord.utils.get(ctx.guild.emojis, name='05ra_x')
    ra_spl = discord.utils.get(ctx.guild.emojis, name='04ra_spl')
    ra_s = discord.utils.get(ctx.guild.emojis, name='03ra_s')
    ra_a = discord.utils.get(ctx.guild.emojis, name='02ra_a')
    ra_b = discord.utils.get(ctx.guild.emojis, name='01ra_b')
    
    # create fields for reacted users
    embed_body = discord.Embed(title=about,colour=0x6699ff)
    embed_body.add_field(name=f"{ra_x} 0人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"{ra_spl} 0人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"{ra_s} 0人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"{ra_a} 0人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"{ra_b} 0人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"🈴 全部で ０人 なう\n", value="\u200b", inline=True)
    embed_body.set_footer(text=f"ウデマエ (Ｘ/Ｓ+/Ｓ/Ａ/Ｂ) をリアクション追加で参加　↩で取消　🚫で中止　✖で削除")
    
    message = await ctx.send(embed=embed_body)
    
    # add reaction as button
    await message.add_reaction('↩')
    

    # check reactions and users to message
    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # ignore bots
            pass
        elif message.id != reaction.message.id:    # ignore reactions to other messages
            pass
        else:    # return true to specific emojis
            return emoji == f"{ra_x}" or \
                emoji == f"{ra_spl}" or \
                emoji == f"{ra_s}" or \
                emoji == f"{ra_a}" or \
                emoji == f"{ra_b}" or \
                emoji == '↩' or \
                emoji == '🚫' or \
                emoji == '✖'
    
    
    # defining the function to return saved emoji info
    def previous_emoji():
        if str(user_reaction_dic[message.id][user.id]) == '05ra_x':
            return ra_x
        elif str(user_reaction_dic[message.id][user.id]) == '04ra_spl':
            return ra_spl
        elif str(user_reaction_dic[message.id][user.id]) == '03ra_s':
            return ra_s
        elif str(user_reaction_dic[message.id][user.id]) == '02ra_a':
            return ra_a
        elif str(user_reaction_dic[message.id][user.id]) == '01ra_b':
            return ra_b
            
            
    # update fields for reacted users
    async def update_field():
        
        # get index no per rank
        def index_no():
            if rank_to_update == ra_x:
                return 0
            if rank_to_update == ra_spl:
                return 1
            if rank_to_update == ra_s:
                return 2
            if rank_to_update == ra_a:
                return 3
            if rank_to_update == ra_b:
                return 4
        
        
        # convert user_reaction_dic
        converted_user_reaction_str = str(dict(user_reaction_dic))[21:-1]    # convert defaultdict to dict format without message.id
        converted_user_reaction_dic = ast.literal_eval(converted_user_reaction_str)    # convert str to dict
        
        # define function to swap dict keys and values
        def swap_dict():
            r = defaultdict(list)
            for k, v in converted_user_reaction_dic.items():
                r[v].append(k)
            return dict(r)
        
        swapped_user_reaction_dic = swap_dict()    # swap keys and values in dict
        
        # update users racted per rank
        try:
            # update user.name list per rank
            user_id_list = swapped_user_reaction_dic[str(rank_to_update.name)]    # get user.ids per rank
            
            user_list = []
            user_list.clear()    # empty the list each time - necessary?
        
            # define function to convert user.id to user.name 
            def convert_id_to_name():
                #for user_id in user_id_list:
                l = []
                for user_id in user_id_list:
                    users_on_list = client.get_user(user_id).name
                    l.append(users_on_list)
                return l
        
            user_list = convert_id_to_name()    # convert user.ids to user.names
            
            # update the field per rank
            count = len(user_list)    # getting no of reacted users per rank
            embed_body.set_field_at(index_no(), name=f"{rank_to_update} {count}人 なう\n", value='\n'.join(user_list), inline=True)
        
        except:    # if no one left on the list
            embed_body.set_field_at(index_no(), name=f"{rank_to_update} 0人 なう\n", value="\u200b", inline=True)
            
        # update no of total reacted users
        embed_body.set_field_at(5, name=f"🈴 全部で {len(user_reaction_dic[message.id])}人 なう\n", value="\u200b", inline=True)
        
        await message.edit(embed=embed_body)
        
    
    #　main function
    while not client.is_closed():
        try:    # wait for reactions that fulills check
            reaction, user = await client.wait_for('reaction_add', timeout=None, check=check)
        except asyncio.TimeoutError:    # ignore timeout
            pass
            
        else:    # when specified reaction added
            
            if str(reaction.emoji) not in ['↩', '🚫', '✖']:    # if reaction is a rank
                
                # check if user reacted to the message before
                if user.id not in user_reaction_dic[message.id]:    # user hasn't reacted to the message
                    
                    # save message.id and user.id with emoji info to dict
                    user_reaction_dic[message.id][user.id] = reaction.emoji.name
                    
                    rank_to_update = reaction.emoji    # set to update reacted rank
                    await update_field()

                else:    # user has reacted to the message before
                    
                    # replace emoji info
                    rank_to_update = previous_emoji()    # set to update previous rank first - important!
                    
                    user_reaction_dic[message.id][user.id] = reaction.emoji.name    # update saved reaction info
                    
                    await update_field()    # update the field for the previous rank

                    rank_to_update = reaction.emoji   # set to update reacted rank
                    await update_field()
                    
            else:
                if str(reaction.emoji) == '↩':
                    
                    # delete saved info if found in the dict
                    if user.id in user_reaction_dic[message.id]:    # if user has reacted to the message before
                        rank_to_update = previous_emoji()    # set to update previous rank first - important!
                        del user_reaction_dic[message.id][user.id]    # delete saved reaction info
                        
                        # remove user.name from the field
                        await update_field()
                        
                elif str(reaction.emoji) == '🚫':
                    
                    #stop the function and notify 
                    await message.remove_reaction('↩', client.user)
                    embed_body.set_footer(text="＝＝＝＝募集は終了しました＝＝＝＝")
                    await message.edit(embed=embed_body)
                    break
                
                elif str(reaction.emoji) == '✖':
                    await message.delete()
                    break
            
            await message.remove_reaction(reaction.emoji, user)


# run the bot    
client.run(token)
