#!/bin/python3

import discord
import asyncio
import datetime

from discord.ext import commands, tasks
from dotenv import load_dotenv
from os import getenv

intents = discord.Intents.all()
intents.members = True

load_dotenv()

PREFIX = '!ws'
#
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
#
#	support
#
class WScont:
	def __init__(self):
		self.name = "Help: "+PREFIX+"?"
		self.count = 0
		self.channel = ''
		self.start = datetime.datetime.now()
		self.lasts = 6*(3600*24)
		self.role = None

def grTimeLeft():
	l = ws.lasts
	s = ws.start
	c = grGetTimeStamp()
	t = (l+s) - c
	if t < 0:
		pass
	else:
		show = ''
		dd = int( (t / 3600) / 24)
		dh = int( (t - (dd * 24 * 3600))/3600 )
		dm = int( ((t - (dh * 3600 + dd * 24 * 3600))/3600)*60 )

		if dd > 0:
			show = str(dd)+"D "
		if dh > 0:
			show = show + str(dh) + "h "
		if dm > 0:
			show = show + str(dm) + "m "
		return str(show)

def grCheckTime():
	l = ws.lasts
	s = ws.start
	c = grGetTimeStamp()
	t = (l+s) - c
	if t > 0:
		return True
	else:
		return False

def grGetTimeStamp():
	return datetime.datetime.now().timestamp()
#
#
#	Loop to update status
#
@tasks.loop(seconds=15)
async def task_loop():
	global ws
	status = ws.name
	if ws.count > 0:
		if grCheckTime() == True:
			status = ws.name + ". " + grTimeLeft()
		else:
			removerole(ws.channel,ws.role)
			await asyncio.sleep(0)
			ws = WScont()
			status = ws.name
	await bot.change_presence(activity=discord.Game(name=status))
#
#	Start
#
ws = WScont()
#
@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name=ws.name))
	task_loop.start()
#
#
#	WS Counter: SETs new game name
#
#
@bot.command(name='name')
async def wsName(ctx, *, arg=''):
#	info = ""
#	if ws.count > 0:
#		ws.start = grGetTimeStamp()
#		info = "\nGame counter restarted!"
	if ws.count > 0:
		if str(arg) == "":
			arg = ws.name
		ws.name = str(arg)
		await ctx.send("...Sets\nGame title: " + arg)
#
#
#	WS Counter: SETs date&time to current (NOW)
#
#
@bot.command(name='time')
async def wsTime(ctx, *, arg=''):
	if ws.count > 0:
		ws.start = grGetTimeStamp()
		await ctx.send("...Sets\nGame counter restarted!")
#
#
#	WS cunter: Stop
#
#
@bot.command(name='stop')
async def wsStop(ctx):
	global ws
	if ws.count > 0:
		await ctx.send("...Sets\nGame removed/cleared!")
		ws = WScont()
#
#
#	GIVE/ADD role to users
#
#	- set WS counter
#
@bot.command(name='+')
async def giverole(ctx, role: discord.Role, *users: discord.Member):
	i=0
	if users:
		u=[]
		for user in users:
			if not role in user.roles:
				await user.add_roles(role)
				u.append(user.name)
				await asyncio.sleep(0)
				i+=1

		if i > 0:
			await ctx.send("...\n" + ", ".join(u) + "\nAdded **" + str(i) + "** users to role **" + str(role) + "**!")
		else:
			await ctx.send("Role **" + str(role) + "** already given!")
	#
	#	start WS counter
	#
	x=0
	users = bot.get_all_members()
	for user in users:
		if role in user.roles:
			x+=1
	
	if ws.count != x or i > 0:
		ws.name = "WS-" + str(int(x/5)*5)
		ws.channel = ctx.message.channel.id
		ws.start = grGetTimeStamp()
		ws.role = role
		ws.count = x
		await ctx.send("Game updated: **"+ ws.name + "**, time till end: " + grTimeLeft() )
#
#
#	REMOVE role from users
#	if arg USERS is empty search in all
#
#	- clear WS counter
#
@bot.command(name='-')
async def removerole(ctx, role: discord.Role, *users: discord.Member):
	if not users:
		users = bot.get_all_members()
	
	i=0
	u=[]
	for user in users:
		if role in user.roles:
			await user.remove_roles(role)
			u.append(user.name)
			await asyncio.sleep(0)
			i+=1
	
	if i > 0:
		await ctx.send("...\n" + ", ".join(u) + "\nRemoved role **" + str(role) + "** from **" + str(i) + "** users!")
	else:
		await ctx.send("Role **" + str(role) + "** already empty!")
#
#
#	SHOW useres assigned to role
#
#	- show WS status
#
@bot.command(name='s')
async def showrole(ctx, role: discord.Role):
	users = bot.get_all_members()
	i=0
	u=[]
	for user in users:
		if role in user.roles:
			u.append(user.name)
			i+=1

	info = "\nGame slot is empty."
	if i > 0:
		u.sort(key=str.lower)
		if ws.count > 0:
			info = "\nIn game: **"+ ws.name + "**, time till end: " + grTimeLeft()
		await ctx.send("...\n" + "\n".join(u) + "\nAssigned **" + str(i) + "** users to role **" + str(role) + "**!"+info)
	else:
		await ctx.send("Role **" + str(role) + "** is empty!"+info)
#
#	HELP
#
@bot.command(name='?')
async def help(ctx):
	h = ("\n** **\n\n**Simple bot to give or remove ROLE** for selected users.\n\n" \
	+ PREFIX +"+ @ROLE @user1 @user2 ... @user11 -> will give role to users \n" \
	+ PREFIX +"+ @ROLE -> updates game status if users change\n" \
	+ PREFIX +"- @ROLE [@user1 @user2 ... @user11] -> will remove it\n" \
	+ PREFIX +"s @ROLE -> show users assigned also current counter\n" \
	+"\n**WS commands for started counter**\n" \
	+"...IF counter is set and time counter goes 0 then role will be removed from users\n" \
	+ PREFIX +"name -> change game name\n" \
	+ PREFIX +"time -> sets data&time to current (now)\n" \
	+ PREFIX +"stop -> clears game counter so now to autoremove need to be set again\n" \
	+ "\nEnjoy!\n"
	)
	await ctx.send(h)
	await asyncio.sleep(0)
#
#	RUN it
#
bot.run(getenv('TOKEN'))