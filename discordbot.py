import discord
from discord.ext import commands
import asyncio
import time

import os
import traceback

# 新しいEvent loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(asyncio.new_event_loop())


client = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command()
async def rect(ctx, about = "募集", settime = 86400):
    settime = float(settime)

    
    # カスタム絵文字の定義
    ra_x = client.get_emoji(598318118762446852)
    ra_spl = client.get_emoji(598318135774412800)
    ra_s = client.get_emoji(598318154707370012)    
    ra_a = client.get_emoji(598318180762517515)
    ra_b = client.get_emoji(598318202577092609)
    
    # 募集の欄
    reaction_members_x = ['>>>']
    reaction_members_spl = ['>>>']
    reaction_members_s = ['>>>']
    reaction_members_a = ['>>>']
    reaction_members_b = ['>>>']
    reaction_members_all = []
    
    mbr_cnt_x = len(reaction_members_x) - 1
    mbr_cnt_spl = len(reaction_members_spl) - 1
    mbr_cnt_s = len(reaction_members_s) - 1
    mbr_cnt_a = len(reaction_members_a) - 1
    mbr_cnt_b = len(reaction_members_b) - 1
    
    embed_body = discord.Embed(title=about,colour=0x1e90ff)
    embed_body.add_field(name=f"{ra_x} {len(reaction_members_x) - 1}人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"{ra_spl} {len(reaction_members_spl) - 1}人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"{ra_s} {len(reaction_members_s) - 1}人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"{ra_a} {len(reaction_members_a) - 1}人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"{ra_b} {len(reaction_members_b) - 1}人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"🈴 全部で{len(reaction_members_all)}人 なう\n", value="\u200b", inline=True)
    
    msg = await ctx.send(embed=embed_body)
    
    # 投票の欄
    vote_list = (
        ra_x,
        ra_spl,
        ra_s,
        ra_a,
        ra_b,
        '↩',
        )
    for vote in vote_list:
        await msg.add_reaction(vote)
        
    # 合計人数欄更新
    async def total_update():        
            reaction_members_all = reaction_members_x + \
            reaction_members_spl + \
            reaction_members_s + \
            reaction_members_a + \
            reaction_members_b
            mbr_total = len(reaction_members_all) - 5
            embed_body.set_field_at(5, name=f"🈴 全部で{mbr_total}人 なう\n", value="\u200b", inline=True)
            await msg.edit(embed=embed_body)
            print('投票結果更新')

    # 動作内容
    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # botは無視
            pass
        #elif user.nick in reaction_members_all:    # 重複は無視
            # リアクション消す。メッセージ管理権限がないとForbidden:エラーが出ます。
            #msg.remove_reaction(str(reaction.emoji), user)
            #pass
        else:
            return emoji == f"{ra_x}" or \
                emoji == f"{ra_spl}" or \
                emoji == f"{ra_s}" or \
                emoji == f"{ra_a}" or \
                emoji == f"{ra_b}" or \
                emoji == '↩' or \
                emoji == '🚫' or \
                emoji == '✖'
        
    # 時間制限
    timeout_start = time.time()
    timeout = 60
    if timeout > settime:
        timeout = settime
    
    print('準備完了')
    
    while time.time() < timeout_start + settime:
        try:
            print('リアクション待ちなう')
            reaction, user = await client.wait_for('reaction_add', timeout=timeout, check=check)
            print('リアクション来た')
        except asyncio.TimeoutError:            
            print('時間切れでループ')
            pass
            
        else:
            if str(reaction.emoji) == f"{ra_x}":
                reaction_members_x.append(user.nick)
                embed_body.set_field_at(0, name=f"{ra_x} {len(reaction_members_x) - 1}人 なう\n", value='\n'.join(reaction_members_x), inline=True)
                await msg.edit(embed=embed_body) 
                await total_update()
            
            elif str(reaction.emoji) == f"{ra_spl}":
                reaction_members_spl.append(user.nick)
                embed_body.set_field_at(1, name=f"{ra_spl} {len(reaction_members_spl) - 1}人 なう\n", value='\n'.join(reaction_members_spl), inline=True)
                await msg.edit(embed=embed_body)
                await total_update()
            
            elif str(reaction.emoji) == f"{ra_s}":
                reaction_members_s.append(user.nick)
                embed_body.set_field_at(2, name=f"{ra_s} {len(reaction_members_s) - 1}人 なう\n", value='\n'.join(reaction_members_s), inline=True)
                await msg.edit(embed=embed_body)
                await total_update()
            
            elif str(reaction.emoji) == f"{ra_a}":
                reaction_members_a.append(user.nick)
                embed_body.set_field_at(3, name=f"{ra_a} {len(reaction_members_a) - 1}人 なう\n", value='\n'.join(reaction_members_a), inline=True)
                await msg.edit(embed=embed_body)
                await total_update()
            
            elif str(reaction.emoji) == f"{ra_b}":
                reaction_members_b.append(user.nick)
                embed_body.set_field_at(4, name=f"{ra_b} {len(reaction_members_b) - 1}人 なう\n", value='\n'.join(reaction_members_b), inline=True)
                await msg.edit(embed=embed_body)
                await total_update()

                
            elif str(reaction.emoji) == '↩':                    
                if user.nick in reaction_members_x:
                    reaction_members_x.remove(user.nick)
                    embed_body.set_field_at(0, name=f"{ra_x} {len(reaction_members_x) - 1}人 なう\n", value='\n'.join(reaction_members_x), inline=True)
                    await msg.edit(embed=embed_body)
                    await total_update()
                    
                elif user.nick in reaction_members_spl:
                    reaction_members_spl.remove(user.nick)
                    embed_body.set_field_at(1, name=f"{ra_spl} {len(reaction_members_spl) - 1}人 なう\n", value='\n'.join(reaction_members_spl), inline=True)
                    await msg.edit(embed=embed_body)
                    await total_update()
                    
                elif user.nick in reaction_members_s:
                    reaction_members_s.remove(user.nick)
                    embed_body.set_field_at(2, name=f"{ra_s} {len(reaction_members_s) - 1}人 なう\n", value='\n'.join(reaction_members_s), inline=True)
                    await msg.edit(embed=embed_body)
                    await total_update()
                    
                elif user.nick in reaction_members_a:
                    reaction_members_a.remove(user.nick)
                    embed_body.set_field_at(3, name=f"{ra_a} {len(reaction_members_a) - 1}人 なう\n", value='\n'.join(reaction_members_a), inline=True)
                    await msg.edit(embed=embed_body)
                    await total_update()
                    
                elif user.nick in reaction_members_b:
                    reaction_members_b.remove(user.nick)
                    embed_body.set_field_at(4, name=f"{ra_b} {len(reaction_members_b) - 1}人 なう\n", value='\n'.join(reaction_members_b), inline=True)
                    await msg.edit(embed=embed_body)
                    await total_update()

                
                else:
                    print('投票されてなかった')
                    pass
                
                                                    
            elif str(reaction.emoji) == '🚫':
                for vote in vote_list:
                    await msg.remove_reaction(vote, client.user)
                embed_body.set_footer(text="＝＝＝＝募集は終了しました＝＝＝＝")
                await msg.edit(embed=embed_body)
                print('中止した')
                break
                
            elif str(reaction.emoji) == '✖':
                await msg.delete()
                print('削除した')
                break
                
            else:
                print('これ何？')
                pass
            
                
            # リアクション消す。メッセージ管理権限がないとForbidden:エラーが出ます。
            await msg.remove_reaction(str(reaction.emoji), user)
            print('リアクション消した')

    else:
        for vote in vote_list:
            await msg.remove_reaction(vote, client.user)
        embed_body.set_footer(text="＝＝＝＝募集は終了しました＝＝＝＝")
        await msg.edit(embed=embed_body)
        print('時間切れで中止')
        
            
client.run(token)
