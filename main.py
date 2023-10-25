# by "@cobias."
# https://discord.com/users/588667852190515201

import time
import asyncio
import discord
from discord.ext import commands
import pnwkit
import requests
kit = pnwkit.QueryKit("api key") # pnw api key (doesnt have to be whitelisted)
aaid = 11880
useridallowed = [] # user ids of ppl that can execute commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix="$", intents=intents)
client.remove_command('help')
def isfloat(num):
	try:
		float(num)
		return True
	except ValueError:
		return False

@client.event
async def on_message(message):
	if "A wild countryball appeared" in message.content:
		if str(message.author) == "Ballsdex#0677":
			await message.channel.send("<@&1158019786568122470>")
	elif "A wild empire appeared" in message.content:
		if str(message.author) == "Empireballs#1336":
			await message.channel.send("<@&1158595025811292160>")
	elif "A wild cityball appeared" in message.content:
		if str(message.author) == "Citydex#9632":
			await message.channel.send("<@&1161628102334627941>")
	await client.process_commands(message)

@client.command(name='help')
async def help(ctx):
	embed=discord.Embed(title="Available commands")
	embed.add_field(name="", value="", inline=False)
	embed.add_field(name="checkmmr *", value="Perform a MMR audit alliance-wide. Usage example: '$checkmmr 0251'", inline=False)
	embed.add_field(name="checknationmmr *", value="Perform a MMR audit on a nation. Usage example: '$checknationmmr 0251 Confederation of Australia'", inline=False)
	embed.add_field(name="checkwarchest *", value="Perform a Warchest audit alliance-wide (requirements are preset, updated as of 22nd Oct 23). Usage example: '$checkwarchest'", inline=False)
	embed.add_field(name="checkwarchestlegacy *", value="Perform a Warchest audit alliance-wide (using a fixed requirement). Arguments: '[cash×million] [uranium×1,000] [food×10,000] [allu×1,000] [gas×1,000] [munitions×1,000] [steel×1,000]' Usage example: '$checkwarchestlegacy 5 0.8 3 7 7.5 7.5 6.25'", inline=False)
	embed.add_field(name="checkspies *", value="Perform a spy audit alliance-wide. Usage example: '$checkspies'", inline=False)
	embed.add_field(name="checkcolor *", value="Perform a color bloc audit. Will check if any members aren't on Red or Beige and will (try to) ping them. Usage example: '$checkcolor'", inline=False)
	#embed.add_field(name="shutdown *", value="Shutdown the bot. Usage example: '$shutdown'", inline=False)
	embed.set_footer(text="\n* Command only available to whitelisted individuals")
	await ctx.send(embed=embed)

@client.command(name='checkmmr')
async def checkmmr(ctx, arg=None):
	if arg is None:
		await ctx.send("Argument is required.")
		return
	if arg.isnumeric() and len(arg) == 4:
		pass
	else:
		await ctx.send("Incorrect argument! Example: 'checkmmr 2451'")
		return
	matchh = False
	for z in range(len(useridallowed)):
		if int(ctx.author.id) == useridallowed[z]:
			matchh = True
	if not useridallowed:
		matchh = True
	if not matchh:
		await ctx.send("You are not authorised to execute this command. Contact '@cobias.' to get whitelisted.")
		return
	query = kit.query("nations", {"alliance_id": aaid, "first": 500, "orderBy": pnwkit.OrderBy("score", pnwkit.Order.DESC)}, "nation_name", "discord", "num_cities", pnwkit.Field("cities",{},"barracks","factory","hangar","drydock"))
	await ctx.send("Fetching, please wait... (approx. 5 secs)")
	result = query.get()
	time.sleep(5)
	passs = False
	totall = 0
	failedd = 0
	final = ""
	SOL_MMR = int(str(arg[0]))
	TNK_MMR = int(str(arg[1]))
	AFT_MMR = int(str(arg[2]))
	SHP_MMR = int(str(arg[3]))
	await ctx.send(f"Showing {int(str(arg[0]))}/{int(str(arg[1]))}/{int(str(arg[2]))}/{int(str(arg[3]))} MMR compliance for AA{aaid}:")
	for x in range(len(result.nations)):
		passs = True
		totall += 1
		#print(f"{result.nations[x].nation_name} num {result.nations[x].num_cities}")
		for y in range(int(result.nations[x].num_cities)):
			#print(f"{result.nations[x].cities[y].barracks} {result.nations[x].cities[y].factory} {result.nations[x].cities[y].hangar} {result.nations[x].cities[y].drydock}")
			if result.nations[x].cities[y].barracks < SOL_MMR:
				passs = False
				break
			if result.nations[x].cities[y].factory < TNK_MMR:
				passs = False
				break
			if result.nations[x].cities[y].hangar < AFT_MMR:
				passs = False
				break
			if result.nations[x].cities[y].drydock < SHP_MMR:
				passs = False
				break
		if passs:
			final += str(f"✓ {result.nations[x].nation_name} ({result.nations[x].discord})\n")
		else:
			final += str(f"**✘ {result.nations[x].nation_name} ({result.nations[x].discord})**\n")
			failedd += 1
	final += f"\n{totall-failedd}/{totall} nations in compliance."
	await ctx.send(final)

@client.command(name='checknationmmr')
async def checknationmmr(ctx, arg1=None , *, arg2=None):
	if arg1 == None:
		await ctx.send("Argument is required.")
		return
	if arg2 == None:
		await ctx.send("Argument is required.")
		return
	if arg1.isnumeric() and len(arg1) == 4:
		pass
	else:
		await ctx.send("Incorrect argument! Example: 'checknationmmr 2451 Confederation of Australia'")
		return
	matchh = False
	if useridallowed == []:
		matchh = True
	for z in range(len(useridallowed)):
		if int(ctx.author.id) == useridallowed[z]:
			matchh = True
	if not matchh:
		await ctx.send("You are not authorised to execute this command. Contact '@cobias.' to get whitelisted.")
		return
	query = kit.query("nations", {"alliance_id": aaid, "first": 500}, "nation_name", "discord", "num_cities", pnwkit.Field("cities",{},"name","barracks","factory","hangar","drydock"))
	await ctx.send("Fetching, please wait... (approx. 5 secs)")
	result = query.get()
	time.sleep(5)
	e = False
	passs = False
	permfail = 0
	final = ""
	SOL_MMR = int(str(arg1[0]))
	TNK_MMR = int(str(arg1[1]))
	AFT_MMR = int(str(arg1[2]))
	SHP_MMR = int(str(arg1[3]))
	for x in range(len(result.nations)):
		if (result.nations[x].nation_name).lower() == (arg2).lower():
			e = x
			break
	if e == False:
		await ctx.send(f"Nation does not exist (in AA{aaid} at least)")
		return
	await ctx.send(f"Showing {int(str(arg1[0]))}/{int(str(arg1[1]))}/{int(str(arg1[2]))}/{int(str(arg1[3]))} MMR compliance by city for {result.nations[e].nation_name}")
	for y in range(result.nations[e].num_cities):
		passs = True
		if result.nations[e].cities[y].barracks < SOL_MMR:
			passs = False
		if result.nations[e].cities[y].factory < TNK_MMR:
			passs = False
		if result.nations[e].cities[y].hangar < AFT_MMR:
			passs = False
		if result.nations[e].cities[y].drydock < SHP_MMR:
			passs = False
		if passs == True:
			final += f"✓ {result.nations[e].cities[y].name}: {result.nations[e].cities[y].barracks}/{result.nations[e].cities[y].factory}/{result.nations[e].cities[y].hangar}/{result.nations[e].cities[y].drydock}\n"
		if passs == False:
			final += f"**✘ {result.nations[e].cities[y].name}: {result.nations[e].cities[y].barracks}/{result.nations[e].cities[y].factory}/{result.nations[e].cities[y].hangar}/{result.nations[e].cities[y].drydock}**\n"
			permfail += 1
	if permfail > 0:
		final += "\nNation is **NOT** in compliance with MMR.\n"
	elif permfail == 0:
		final += "\nNation is in compliance with MMR.\n"
	final += f"{result.nations[e].num_cities-permfail}/{result.nations[e].num_cities} cities in compliance."
	await ctx.send(final)
 
@client.command(name='checkwarchest')
async def checkwarchest(ctx):
	req = [
	None,None,None,None,None,None,None,None,None,
	{
		"city": 10,
		"cash": "5,000,000",
		"ura": 800,
		"food": "30,000",
		"allu": "7,000",
		"gas": "7,500",
		"mun": "7,500",
		"steel": "6,250"
	},
	{
		"city": 11,
		"cash": "5,500,000",
		"ura": 880,
		"food": "33,000",
		"allu": "7,700",
		"gas": "8,250",
		"mun": "8,250",
		"steel": "6,875"
	},
	{
		"city": 12,
		"cash": "6,000,000",
		"ura": 960,
		"food": "36,000",
		"allu": "8,400",
		"gas": "9,000",
		"mun": "9,000",
		"steel": "7,500"
	},
	{
		"city": 13,
		"cash": "6,500,000",
		"ura": "1,040",
		"food": "39,000",
		"allu": "9,100",
		"gas": "9,750",
		"mun": "9,750",
		"steel": "8,125"
	},
	{
		"city": 14,
		"cash": "7,000,000",
		"ura": "1,120",
		"food": "42,000",
		"allu": "9,800",
		"gas": "10,500",
		"mun": "10,500",
		"steel": "8,750"
	},
	{
		"city": 15,
		"cash": "7,500,000",
		"ura": "1,200",
		"food": "45,000",
		"allu": "10,500",
		"gas": "11,250",
		"mun": "11,250",
		"steel": "9,375"
	},
	{
		"city": 16,
		"cash": "8,000,000",
		"ura": "1,280",
		"food": "48,000",
		"allu": "22,400",
		"gas": "24,000",
		"mun": "24,000",
		"steel": "20,000"
	},
	{
		"city": 17,
		"cash": "8,500,000",
		"ura": "1,360",
		"food": "51,000",
		"allu": "23,800",
		"gas": "25,500",
		"mun": "25,500",
		"steel": "21,250"
	},
	{
		"city": 18,
		"cash": "9,000,000",
		"ura": "1,440",
		"food": "54,000",
		"allu": "25,200",
		"gas": "27,000",
		"mun": "27,000",
		"steel": "22,500"
	},
	{
		"city": 19,
		"cash": "9,500,000",
		"ura": "1,520",
		"food": "57,000",
		"allu": "26,600",
		"gas": "28,500",
		"mun": "28,500",
		"steel": "23,750"
	},
	{
		"city": 20,
		"cash": "10,000,000",
		"ura": "1,600",
		"food": "60,000",
		"allu": "28,000",
		"gas": "30,000",
		"mun": "30,000",
		"steel": "25,000"
	},
	{
		"city": 21,
		"cash": "10,500,000",
		"ura": "1,680",
		"food": "63,000",
		"allu": "29,400",
		"gas": "31,500",
		"mun": "31,500",
		"steel": "26,250"
	},
	{
		"city": 22,
		"cash": "11,000,000",
		"ura": "1,760",
		"food": "66,000",
		"allu": "30,800",
		"gas": "33,000",
		"mun": "33,000",
		"steel": "27,500"
	},
	{
		"city": 23,
		"cash": "11,500,000",
		"ura": "1,840",
		"food": "69,000",
		"allu": "32,200",
		"gas": "34,500",
		"mun": "34,500",
		"steel": "28,750"
	},
	{
		"city": 24,
		"cash": "12,000,000",
		"ura": "1,920",
		"food": "72,000",
		"allu": "33,600",
		"gas": "36,000",
		"mun": "36,000",
		"steel": "30,000"
	},
	{
		"city": 25,
		"cash": "12,500,000",
		"ura": "2,000",
		"food": "75,000",
		"allu": "35,000",
		"gas": "37,500",
		"mun": "37,500",
		"steel": "31,250"
	},
	{
		"city": 26,
		"cash": "13,000,000",
		"ura": "2,080",
		"food": "78,000",
		"allu": "36,400",
		"gas": "39,000",
		"mun": "39,000",
		"steel": "32,500"
	},
	{
		"city": 27,
		"cash": "13,500,000",
		"ura": "2,160",
		"food": "81,000",
		"allu": "37,800",
		"gas": "40,500",
		"mun": "40,500",
		"steel": "33,750"
	},
	{
		"city": 28,
		"cash": "14,000,000",
		"ura": "2,240",
		"food": "84,000",
		"allu": "39,200",
		"gas": "42,000",
		"mun": "42,000",
		"steel": "35,000"
	},
	{
		"city": 29,
		"cash": "14,500,000",
		"ura": "2,320",
		"food": "87,000",
		"allu": "40,600",
		"gas": "43,500",
		"mun": "43,500",
		"steel": "36,250"
	},
	{
		"city": 30,
		"cash": "15,000,000",
		"ura": "2,400",
		"food": "90,000",
		"allu": "42,000",
		"gas": "45,000",
		"mun": "45,000",
		"steel": "37,500"
	},
	{
		"city": 31,
		"cash": "15,500,000",
		"ura": "2,480",
		"food": "93,000",
		"allu": "43,400",
		"gas": "46,500",
		"mun": "46,500",
		"steel": "38,750"
	},
	{
		"city": 32,
		"cash": "16,000,000",
		"ura": "2,560",
		"food": "96,000",
		"allu": "44,800",
		"gas": "48,000",
		"mun": "48,000",
		"steel": "40,000"
	}
	]
	matchh = False
	for z in useridallowed:
		if int(ctx.author.id) == z:
			matchh = True
	if not useridallowed:
		matchh = True
	if not matchh:
		await ctx.send("You are not authorised to execute this command. Contact '@cobias.' to get whitelisted.")
		return
	query = kit.query("nations", {"alliance_id": aaid, "first": 500, "orderBy": pnwkit.OrderBy("score", pnwkit.Order.DESC)}, "nation_name", "discord", "num_cities", "aluminum", "steel", "gasoline", "munitions","money","uranium","food")
	await ctx.send("Fetching, please wait... (approx. 5 secs)")
	result = query.get()
	time.sleep(5)
	passs = False
	totall = 0
	failedd = 0
	final = ""
	await ctx.send(f"Showing warchest compliance for AA{aaid}:")
	for x in range(len(result.nations)):
		passs = True
		totall += 1
		if result.nations[x].num_cities <= 9:
			passs = "unreq"
		else:
			if result.nations[x].money < int(str((req[(result.nations[x].num_cities)-1]["cash"])).replace(",","")):
				if passs is True:
					passs = ""
				passs += " ✘Cash"
			if result.nations[x].uranium < int(str((req[(result.nations[x].num_cities)-1]["ura"])).replace(",","")):
				if passs is True:
					passs = ""
				passs += " ✘Ura"
			if result.nations[x].food < int(str((req[(result.nations[x].num_cities)-1]["food"])).replace(",","")):
				if passs is True:
					passs = ""
				passs += " ✘Food"
			if result.nations[x].aluminum < int(str((req[(result.nations[x].num_cities)-1]["allu"])).replace(",","")):
				if passs is True:
					passs = ""
				passs += " ✘Allu"
			if result.nations[x].gasoline < int(str((req[(result.nations[x].num_cities)-1]["gas"])).replace(",","")):
				if passs is True:
					passs = ""
				passs += " ✘Gas"
			if result.nations[x].munitions < int(str((req[(result.nations[x].num_cities)-1]["mun"])).replace(",","")):
				if passs is True:
					passs = ""
				passs += " ✘Mun"
			if result.nations[x].steel < int(str((req[(result.nations[x].num_cities)-1]["steel"])).replace(",","")):
				if passs is True:
					passs = ""
				passs += " ✘Steel"
		if passs is True:
			final += str(f"✓ {result.nations[x].nation_name} ({result.nations[x].discord})\n")
		elif passs == "unreq":
			final += str(f"✓ {result.nations[x].nation_name} ({result.nations[x].discord}) - NO REQUIREMENT\n")
		else:
			final += str(f"**✘ {result.nations[x].nation_name} ({result.nations[x].discord}) -{passs}**\n")
			failedd += 1
	final += f"\n{totall-failedd}/{totall} nations in compliance."
	await ctx.send(final)

@client.command(name='checkwarchestlegacy')
async def checkwarchestlegacy(ctx,arg1=None,arg2=None,arg3=None,arg4=None,arg5=None,arg6=None,arg7=None):
	args = [arg1,arg2,arg3,arg4,arg5,arg6,arg7]
	for i in args:
		if i is None:
			await ctx.send("All arguments are required.")
			return
	for w in args:
		if not isfloat(w):
			await ctx.send("Incorrect argument(s)! See '$help' for more info.")
			return
	matchh = False
	for z in range(len(useridallowed)):
		if int(ctx.author.id) == useridallowed[z]:
			matchh = True
	if not useridallowed:
		matchh = True
	if not matchh:
		await ctx.send("You are not authorised to execute this command. Contact '@cobias.' to get whitelisted.")
		return
	query = kit.query("nations", {"alliance_id": aaid, "first": 500, "orderBy": pnwkit.OrderBy("score", pnwkit.Order.DESC)}, "nation_name", "discord", "num_cities", "aluminum", "steel", "gasoline", "munitions","food","money","uranium")
	await ctx.send("Fetching, please wait... (approx. 5 secs)")
	result = query.get()
	time.sleep(5)
	passs = False
	totall = 0
	failedd = 0
	final = ""
	await ctx.send(f"Showing warchest compliance for AA{aaid} with fixed requirement:")
	for x in range(len(result.nations)):
		passs = True
		totall += 1
		if int(result.nations[x].money) < float(args[0])*1000000:
			if passs is True:
				passs = ""
			passs += " ✘Cash"
		if int(result.nations[x].uranium) < float(args[1])*1000:
			if passs is True:
				passs = ""
			passs += " ✘Ura"
		if int(result.nations[x].food) < float(args[2])*10000:
			if passs is True:
				passs = ""
			passs += " ✘Food"
		if int(result.nations[x].aluminum) < float(args[3])*1000:
			if passs is True:
				passs = ""
			passs += " ✘Allu"
		if int(result.nations[x].gasoline) < float(args[4])*1000:
			if passs is True:
				passs = ""
			passs += " ✘Gas"
		if int(result.nations[x].munitions) < float(args[5])*1000:
			if passs is True:
				passs = ""
			passs += " ✘Mun"
		if int(result.nations[x].steel) < float(args[6])*1000:
			if passs is True:
				passs = ""
			passs += " ✘Steel"
		if passs is True:
			final += str(f"✓ {result.nations[x].nation_name} ({result.nations[x].discord})\n")
		else:
			final += str(f"**✘ {result.nations[x].nation_name} ({result.nations[x].discord}) -{passs}**\n")
			failedd += 1
	final += f"\n{totall-failedd}/{totall} nations in compliance."
	await ctx.send(final)

@client.command(name='checkspies')
async def checkspies(ctx):
	for z in range(len(useridallowed)):
		if int(ctx.author.id) == useridallowed[z]:
			matchh = True
	if not useridallowed:
		matchh = True
	if not matchh:
		await ctx.send("You are not authorised to execute this command. Contact '@cobias.' to get whitelisted.")
		return
	query = kit.query("nations", {"alliance_id": aaid, "first": 500, "orderBy": pnwkit.OrderBy("score", pnwkit.Order.DESC)}, "nation_name", "discord", "spies", "central_intelligence_agency")
	await ctx.send("Fetching, please wait... (approx. 5 secs)")
	result = query.get()
	time.sleep(5)
	final = ""
	passs = 0
	total = 0
	await ctx.send(f"Showing spies for AA{aaid}:")
	for x in range(len(result.nations)):
		CIA = ""
		total += 1
		if result.nations[x].central_intelligence_agency is True:
			CIA = " - Has CIA"
		if result.nations[x].spies >= 50:
			final += str(f"✓ {result.nations[x].spies} spies - {result.nations[x].nation_name} ({result.nations[x].discord}){CIA}\n")
			passs += 1
		else:
			final += str(f"**✘ {result.nations[x].spies} spies - {result.nations[x].nation_name} ({result.nations[x].discord}){CIA}**\n")
	final += f"\n{passs}/{total} nations in compliance (50 or more spies)."
	await ctx.send(final)

def usrtoid(user:discord.Member):
	return user.id

@client.command(name='checkcolor')
async def checkcolor(ctx):
	for z in range(len(useridallowed)):
		if int(ctx.author.id) == useridallowed[z]:
			matchh = True
	if useridallowed == []:
		matchh = True
	if not matchh:
		await ctx.send("You are not authorised to execute this command. Contact '@cobias.' to get whitelisted.")
		return
	query = kit.query("nations", {"alliance_id": aaid, "first": 500, "orderBy": pnwkit.OrderBy("score", pnwkit.Order.DESC)}, "nation_name", "discord_id", "color", "discord")
	await ctx.send("Fetching, please wait... (approx. 5 secs)")
	result = query.get()
	time.sleep(5)
	response = "All members either in red or beige color blocs."
	for x in result.nations:
		if x.color not in ("red","beige"):
			if response == "All members either in red or beige color blocs.":
				response = "Please switch to **RED** color bloc.\n"
			if x.discord in (None,""):
				response += f"{x.nation_name} (No discord username set ingame)\n"
			elif x.discord_id is None:
				response += f"@{x.discord} - ({x.nation_name})\n"
			else:
				response += f"<@{x.discord_id}>\n"
	await ctx.send(response)

@client.command(name='shutdown')
async def shutdown(ctx):
	if ctx.author.id != 588667852190515201: # my user id
		await ctx.send("Only the bot owner (@cobias.) can execute this command.")
		return
	else:
		await ctx.send("cya")
		await client.close()

client.run("token") # discord bot token
print("shutdown occured")