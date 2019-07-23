import discord
from discord.ext import commands

import os
import traceback

client = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']



# 各ユーザのリアクション(スタンプ)を保存して置くためのdict
from collections import defaultdict
user_reaction_dic = defaultdict(dict)
print(user_reaction_dic)

x_reaction_dic = defaultdict(dict)
spl_reaction_dic = defaultdict(dict)
s_reaction_dic = defaultdict(dict)
a_reaction_dic = defaultdict(dict)
b_reaction_dic = defaultdict(dict)

# リアクションしたメンバーリストの作成
x_user_reaction = []
spl_user_reaction = []
s_user_reaction = []
a_user_reaction = []
b_user_reaction = []
total_user_reaction = []


# 新しいEvent loop
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(asyncio.new_event_loop())
print('stated new event loop')


# 起動時の処理
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# コマンド入力時の処理
@client.command()
async def boshu(ctx, about = "募集"):
    
    # カスタム絵文字の定義
    ra_x = client.get_emoji(598318118762446852)
    ra_spl = client.get_emoji(598318135774412800)
    ra_s = client.get_emoji(598318154707370012)    
    ra_a = client.get_emoji(598318180762517515)
    ra_b = client.get_emoji(598318202577092609)
    
    # リアクションしたメンバーの欄作成
    embed_body = discord.Embed(title=about,colour=0x6699ff)
    embed_body.add_field(name=f"{ra_x} {len(x_reaction_dic)}人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"{ra_spl} {len(spl_reaction_dic)}人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"{ra_s} {len(s_reaction_dic)}人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"{ra_a} {len(a_reaction_dic)}人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"{ra_b} {len(b_reaction_dic)}人 なう\n", value="\u200b", inline=True)
    embed_body.add_field(name=f"🈴 全部で{len(user_reaction_dic)}人 なう\n", value="\u200b", inline=True)
    
    message = await ctx.send(embed=embed_body)
    message_id = message.id
    print(message_id)
    
    # リアクションの追加
    await message.add_reaction(ra_x)
    await message.add_reaction(ra_spl)
    await message.add_reaction(ra_s)
    await message.add_reaction(ra_a)
    await message.add_reaction(ra_b)
    
    # 合計人数の更新の定義
    async def total_update():
        total_user_reaction.append(user.id)
        embed_body.set_field_at(5, name=f"🈴 全部で{len(user_reaction_dic)}人 なう\n", value="\u200b", inline=True)
        await message.edit(embed=embed_body)
        print(total_user_reaction)
    
    async def total_update_fake():
        embed_body.set_field_at(5, name=f"🈴 全部で{len(user_reaction_dic)}人 なう\n", value="\u200b", inline=True)
        await message.edit(embed=embed_body)


    # ユーザーとリアクションのチェック
    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # botは無視
            pass
        else:
            return emoji == f"{ra_x}" or \
                emoji == f"{ra_spl}" or \
                emoji == f"{ra_s}" or \
                emoji == f"{ra_a}" or \
                emoji == f"{ra_b}" or \
                emoji == '↩' or \
                emoji == '🚫' or \
                emoji == '✖'
        
    #　動作内容
    while not client.is_closed():
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=None, check=check)
        except asyncio.TimeoutError:
            pass
            
        else:
                 
            await total_update_fake()    #なぜかこれがないと人数が更新されない
                
                
            if str(reaction.emoji) == f"{ra_x}":
                x_user_reaction.append(user.nick)
                
                if user.nick in spl_user_reaction:
                    print('x_user_reactionに名前あり')
                else:
                    print('x_user_reactionに名前なし')
            
            elif str(reaction.emoji) == f"{ra_spl}":
                spl_user_reaction.append(user.nick)
            
            elif str(reaction.emoji) == f"{ra_s}":
                s_user_reaction.append(user.nick)
            
            elif str(reaction.emoji) == f"{ra_a}":
                a_user_reaction.append(user.nick)
                
            elif str(reaction.emoji) == f"{ra_b}":
                b_user_reaction.append(user.nick)
                        
            else:
                pass
            
            embed_body.set_field_at(0, name=f"{ra_x} {len(x_reaction_dic)}人 なう\n", value='\n'.join(x_user_reaction), inline=True)
            embed_body.set_field_at(1, name=f"{ra_spl} {len(spl_reaction_dic)}人 なう\n", value='\n'.join(spl_user_reaction), inline=True)
            embed_body.set_field_at(2, name=f"{ra_s} {len(s_reaction_dic)}人 なう\n", value='\n'.join(s_user_reaction), inline=True)
            embed_body.set_field_at(3, name=f"{ra_a} {len(a_reaction_dic)}人 なう\n", value='\n'.join(a_user_reaction), inline=True)
            embed_body.set_field_at(4, name=f"{ra_b} {len(b_reaction_dic)}人 なう\n", value='\n'.join(b_user_reaction), inline=True)
            await message.edit(embed=embed_body)
            await total_update()
        
# リアクションが追加された時の処理
@client.event
async def on_reaction_add(reaction, user):
    
    # カスタム絵文字の定義
    ra_x = client.get_emoji(598318118762446852)
    ra_spl = client.get_emoji(598318135774412800)
    ra_s = client.get_emoji(598318154707370012)    
    ra_a = client.get_emoji(598318180762517515)
    ra_b = client.get_emoji(598318202577092609)
    
    if user.bot == True:
        pass
    
    else:
        print('reaction added')
        # リアクションが追加されたメッセージの取得
        message = reaction.message
    
        # この投稿に対してこれまでにリアクションしたかを判定
        if message.id not in user_reaction_dic[user.id]:
            print('new reaction')
            # 新しく登録された絵文字なので情報を保存しておく
            user_reaction_dic[user.id][message.id] = reaction.emoji            
            print(user_reaction_dic)
            
            if str(reaction.emoji) == f"{ra_x}":
                x_reaction_dic[user.id][message.id] = reaction.emoji
                print(x_reaction_dic)
            elif str(reaction.emoji) == f"{ra_spl}":
                spl_reaction_dic[user.id][message.id] = reaction.emoji
                print(spl_reaction_dic)
            elif str(reaction.emoji) == f"{ra_s}":
                s_reaction_dic[user.id][message.id] = reaction.emoji
                print(s_reaction_dic)
            elif str(reaction.emoji) == f"{ra_a}":
                a_reaction_dic[user.id][message.id] = reaction.emoji
                print(a_reaction_dic)
            elif str(reaction.emoji) == f"{ra_b}":
                b_reaction_dic[user.id][message.id] = reaction.emoji
                print(b_reaction_dic)
                
        else:
            print('duplicated reaction')
            # 前回の絵文字を削除して更新する
            await message.remove_reaction(user_reaction_dic[user.id][message.id], user)
            user_reaction_dic[user.id][message.id] = reaction.emoji
            print(user_reaction_dic)
            
            if str(reaction.emoji) == f"{ra_x}":
                x_reaction_dic[user.id][message.id] = reaction.emoji
                print(x_reaction_dic)
                if message.id in spl_reaction_dic[user.id]:
                    print('removing saved reaction info spl')
                    del spl_reaction_dic[user.id][message.id]
                    print(spl_reaction_dic)
                elif message.id in s_reaction_dic[user.id]:
                    print('removing saved reaction info s')
                    del s_reaction_dic[user.id][message.id]
                    print(s_reaction_dic)
                elif message.id in a_reaction_dic[user.id]:
                    print('removing saved reaction info a')
                    del a_reaction_dic[user.id][message.id]
                    print(a_reaction_dic)
                elif message.id in b_reaction_dic[user.id]:
                    print('removing saved reaction info b')
                    del b_reaction_dic[user.id][message.id]
                    print(b_reaction_dic)
            elif str(reaction.emoji) == f"{ra_spl}":
                spl_reaction_dic[user.id][message.id] = reaction.emoji
                print(spl_reaction_dic)
                if message.id in x_reaction_dic[user.id]:
                    print('removing saved reaction info x')
                    del x_reaction_dic[user.id][message.id]
                    print(x_reaction_dic)
                elif message.id in s_reaction_dic[user.id]:
                    print('removing saved reaction info s')
                    del s_reaction_dic[user.id][message.id]
                    print(s_reaction_dic)
                elif message.id in a_reaction_dic[user.id]:
                    print('removing saved reaction info a')
                    del a_reaction_dic[user.id][message.id]
                    print(a_reaction_dic)
                elif message.id in b_reaction_dic[user.id]:
                    print('removing saved reaction info b')
                    del b_reaction_dic[user.id][message.id]
                    print(b_reaction_dic)
            elif str(reaction.emoji) == f"{ra_s}":
                s_reaction_dic[user.id][message.id] = reaction.emoji
                print(s_reaction_dic)
                if message.id in x_reaction_dic[user.id]:
                    print('removing saved reaction info x')
                    del x_reaction_dic[user.id][message.id]
                    print(x_reaction_dic)
                elif message.id in spl_reaction_dic[user.id]:
                    print('removing saved reaction info spl')
                    del s_reaction_dic[user.id][message.id]
                    print(spl_reaction_dic)
                elif message.id in a_reaction_dic[user.id]:
                    print('removing saved reaction info a')
                    del a_reaction_dic[user.id][message.id]
                    print(a_reaction_dic)
                elif message.id in b_reaction_dic[user.id]:
                    print('removing saved reaction info b')
                    del b_reaction_dic[user.id][message.id]
                    print(b_reaction_dic)
            elif str(reaction.emoji) == f"{ra_a}":
                a_reaction_dic[user.id][message.id] = reaction.emoji
                print(a_reaction_dic)
                if message.id in x_reaction_dic[user.id]:
                    print('removing saved reaction info x')
                    del x_reaction_dic[user.id][message.id]
                    print(x_reaction_dic)
                elif message.id in spl_reaction_dic[user.id]:
                    print('removing saved reaction info spl')
                    del s_reaction_dic[user.id][message.id]
                    print(spl_reaction_dic)
                elif message.id in s_reaction_dic[user.id]:
                    print('removing saved reaction info s')
                    del s_reaction_dic[user.id][message.id]
                    print(s_reaction_dic)
                elif message.id in b_reaction_dic[user.id]:
                    print('removing saved reaction info b')
                    del b_reaction_dic[user.id][message.id]
                    print(b_reaction_dic)
            elif str(reaction.emoji) == f"{ra_b}":
                b_reaction_dic[user.id][message.id] = reaction.emoji
                print(b_reaction_dic)
                if message.id in x_reaction_dic[user.id]:
                    print('removing saved reaction info x')
                    del x_reaction_dic[user.id][message.id]
                    print(x_reaction_dic)
                elif message.id in spl_reaction_dic[user.id]:
                    print('removing saved reaction info spl')
                    del s_reaction_dic[user.id][message.id]
                    print(spl_reaction_dic)
                elif message.id in s_reaction_dic[user.id]:
                    print('removing saved reaction info s')
                    del s_reaction_dic[user.id][message.id]
                    print(s_reaction_dic)
                elif message.id in a_reaction_dic[user.id]:
                    print('removing saved reaction info a')
                    del a_reaction_dic[user.id][message.id]
                    print(a_reaction_dic)
        
# リアクションが削除された時の処理
@client.event
async def on_reaction_remove(reaction, user):
    print('reaction removed')
    
    # カスタム絵文字の定義
    ra_x = client.get_emoji(598318118762446852)
    ra_spl = client.get_emoji(598318135774412800)
    ra_s = client.get_emoji(598318154707370012)    
    ra_a = client.get_emoji(598318180762517515)
    ra_b = client.get_emoji(598318202577092609)
    
    # リアクションが追加されたメッセージの取得
    message = reaction.message
    
    # 保存してあるリアクション情報と一致したらそれを削除しておく
    if user_reaction_dic[user.id][message.id] == reaction.emoji:
        print('removing saved reaction info')
        del user_reaction_dic[user.id][message.id]
        print(user_reaction_dic)
        

# BOTを実行
client.run(token)
