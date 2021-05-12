import aiofiles
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio


intents = discord.Intents.default()
intents.members = True

token = ('ODM2OTUxNTE2ODMzMTIwMjg4.YIld1w.ESI_JgQPx9F5ABKoqtpHHFffVUE')

Bot = commands.Bot(command_prefix="/", intents=intents)
Bot.remove_command('help')


@Bot.event
async def on_member_join(ctx):
    role = discord.utils.get(ctx.guild.roles, name = "Игрок") 
    await ctx.add_roles(role)

@Bot.event
async def on_ready():
    print("Бот запущен")
    await Bot.change_presence(status=discord.Status.idle,activity=discord.Game("/help"))
    
    
@Bot.command()
async def help(ctx):
    emb = discord.Embed(title='Список команд',color=0xff0000)
    dsmoder = discord.utils.get(ctx.guild.roles, id=842120173187760141)
    emb.add_field(name="{}userinfo".format("/"),value="Информация о пользователе", inline=False)
    emb.add_field(name="Примечание: Все, ниже описанные команды, созданы исключиельно для",value=dsmoder.mention, inline=False)
    emb.add_field(name="{}mute".format("/"),value="Мут человека", inline=False)
    emb.add_field(name="{}unmute".format("/"),value="Размут человека", inline=False)
    emb.add_field(name="{}ban".format("/"),value="Бан", inline=False)
    emb.add_field(name="{}kick".format("/"),value="Кик", inline=False)
    emb.add_field(name="{}clear".format("/"),value="Очистка чата", inline=False)
    await ctx.send(embed = emb)


@Bot.command()
async def userinfo(ctx,member:discord.Member):
    emb = discord.Embed(title='Информация о пользователе',color=0xff0000)
    emb.add_field(name="Имя: ",value=member.display_name,inline=False)
    emb.add_field(name="Дата вступления: ",value=member.joined_at,inline=False)
    emb.add_field(name="Аккаунт создан: ",value=member.created_at.strftime("%#d %B %Y"),inline=False)
    emb.set_thumbnail(url=member.avatar_url) 
    emb.set_footer(text=f"Вызвано: {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed = emb)


@Bot.command()
@commands.has_permissions(view_audit_log=True)
async def mute(ctx,member:discord.Member,time:int,reason):
    channel = Bot.get_channel(842120173220790315)
    muterole = discord.utils.get(ctx.guild.roles,id=842120173141360761)
    emb = discord.Embed(title='Мут',color=0xff0000)
    emb.add_field(name='Модератор: ',value=ctx.message.author.mention,inline=False)
    emb.add_field(name='Нарушитель: ',value=member.mention,inline=False)
    emb.add_field(name='Причина:',value=reason,inline=False)
    emb.add_field(name="Время: ",value=time,inline=False)
    emb1 = discord.Embed(title='Вы получили мут',color=0xff0000)
    emb1.add_field(name='Модератор: ',value=ctx.message.author.mention,inline=False)
    emb1.add_field(name='Причина:',value=reason,inline=False)
    emb1.add_field(name="Время: ",value=time,inline=False)
    await member.add_roles(muterole)
    await ctx.send("Успешно выполнено!")
    await member.send(embed = emb1)
    await channel.send(embed = emb)
    await asyncio.sleep(time)
    await member.remove_roles(muterole)

@Bot.command()
@commands.has_permissions(view_audit_log=True)
async def unmute(ctx,member:discord.Member):
    channel = Bot.get_channel(842120173220790315)
    muterole = discord.utils.get(ctx.guild.roles,id=837354408974090260)
    emb = discord.Embed(title='Размут',color=0xff0000)
    emb.add_field(name='Модератор: ',value=ctx.message.author.mention,inline=False)
    emb.add_field(name='Нарушитель: ',value=member.mention,inline=False)
    await channel.send(embed = emb)
    await ctx.send("Успешно выполнено!")
    await member.remove_roles(muterole)


@Bot.command()
@commands.has_permissions(view_audit_log=True)
async def kick(ctx,member:discord.Member,reason):
    channel = Bot.get_channel(842120173220790315)
    emb = discord.Embed(title='Кик',color=0xff0000)
    emb.add_field(name='Модератор: ',value=ctx.message.author.mention,inline=False)
    emb.add_field(name='Нарушитель: ',value=member.mention,inline=False)
    emb.add_field(name='Причина:',value=reason,inline=False)
    emb1 = discord.Embed(title='Вы были выгнаны с сервера',color=0xff0000)
    emb1.add_field(name='Модератор: ',value=ctx.message.author.mention,inline=False)
    emb1.add_field(name='Причина:',value=reason,inline=False)
    await member.send(embed = emb1)
    await channel.send(embed = emb)
    await ctx.send("Успешно выполнено!")
    await member.kick()

@Bot.command()
@commands.has_permissions(view_audit_log=True)
async def ban(ctx,member:discord.Member,reason):
    channel = Bot.get_channel(842120173220790315)
    emb = discord.Embed(title='Бан',color=0xff0000)
    emb.add_field(name='Модератор: ',value=ctx.message.author.mention,inline=False)
    emb.add_field(name='Нарушитель: ',value=member.mention,inline=False)
    emb.add_field(name='Причина:',value=reason,inline=False)
    emb1 = discord.Embed(title='Вы были забанены на сервере',color=0xff0000)
    emb1.add_field(name='Модератор: ',value=ctx.message.author.mention,inline=False)
    emb1.add_field(name='Причина:',value=reason,inline=False)
    await channel.send(embed = emb)
    await member.send(embed = emb1)
    await ctx.send("Успешно выполнено!")
    await member.ban()

@Bot.command()
@commands.has_permissions(view_audit_log=True)
async def clear(ctx,amount=100):
    channel = Bot.get_channel(842120173220790315)
    deleted = await ctx.message.channel.purge(limit=amount + 1)
    emb = discord.Embed(title='Очистка',color=0xff0000)
    emb.add_field(name='Модератор: ',value=ctx.message.author.mention,inline=False)
    emb.add_field(name='Очищено: ',value=amount)
    await channel.send(embed = emb)




Bot.run(token)