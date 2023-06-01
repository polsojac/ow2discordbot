# bot.py
import os
import requests
from dotenv import load_dotenv
import discord
from discord import File
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command(name='ow2', help='format !ow2 <your battle.net tag here>')
async def ow2(ctx, arg1='', arg2=''):
    params = {'gamemode': 'competitive'}
    tank_heroes = ['dva', 'doomfist', 'junker-queen', 'orisa', 'ramattra', 'reinhardt', 'roadhog', 
                'sigma', 'winston', 'wrecking-ball', 'zarya']
    dmg_heroes = ['ashe', 'bastion', 'cassidy', 'echo', 'genji', 'hanzo', 'junkrat', 'mei', 'pharah', 
                'reaper', 'sojourn', 'soldier-76', 'sombra', 'symmetra', 'torbjorn', 'tracer', 'widowmaker']
    supp_heroes = ['ana', 'baptiste', 'brigitte', 'kiriko', 'lifeweaver', 'lucio', 'mercy', 'moira', 'zenyatta']
    hero_stats = False
    if arg2 in tank_heroes or arg2 in dmg_heroes or arg2 in supp_heroes:
        hero_stats = True
    if arg1 == '':
        await ctx.send('Must enter valid battle.net account (input is case-sensitive)')
    else:
        username = arg1
        username = username.replace('#', '-')
        career_stats = requests.get(url='https://overfast-api.tekrop.fr/players/' + username + '/stats/career', 
        params=params)
        stats_summary = requests.get(url='https://overfast-api.tekrop.fr/players/' + username + '/stats/summary', 
        params=params)
        if career_stats.status_code != 200 or stats_summary.status_code != 200:
            await ctx.send('Must enter valid battle.net account (input is case-sensitive)')
        else:
            summary_data = stats_summary.json()
            career_data = career_stats.json()
            if summary_data == {} or career_data == {}:
                await ctx.send('This account is currently set to private')
            else:
                tank_dicts = []
                dmg_dicts = []
                supp_dicts = []

                for i in range(len(tank_heroes)):
                    tank_data = {}
                    tank_data['hero'] = tank_heroes[i]
                    tank_data['image'] = tank_heroes[i] + '.png'
                    try: 
                        tank_data['games_played'] = career_data[tank_heroes[i]]['game']['games_played']
                    except:
                        tank_data['games_played'] = 0
                    try:
                        tank_data['deaths_per_10'] = career_data[tank_heroes[i]]['average']['deaths_avg_per_10_min']
                    except:
                        tank_data['deaths_per_10'] = 0
                    try:
                        tank_data['hero_dmg_per_10'] = career_data[tank_heroes[i]]['average']['hero_damage_done_avg_per_10_min']
                    except:
                        tank_data['hero_dmg_per_10'] = 0
                    try:
                        tank_data['obj_kills_per_10'] = career_data[tank_heroes[i]]['average']['objective_kills_avg_per_10_min']
                    except:
                        tank_data['obj_kills_per_10'] = 0
                    try:
                        tank_data['elims_per_10'] = career_data[tank_heroes[i]]['average']['eliminations_avg_per_10_min']
                    except:
                        tank_data['elims_per_10'] = 0
                        
                    if tank_data['games_played'] > 1:
                        tank_data['winrate'] = summary_data['heroes'][tank_heroes[i]]['winrate']
                    else:
                        tank_data['winrate'] = 0
                    if arg2 == tank_heroes[i]:
                        await ctx.send('Your ' + arg2 + ' advanced stats:\n'
                                    + 'Games played - '+ str(tank_data['games_played']) +'\n'
                                    + 'Deaths/10 min - ' + str(tank_data['deaths_per_10']) + '\n'
                                    + 'Hero damage/10 min - ' + str(tank_data['hero_dmg_per_10']) + '\n'
                                    + 'Obj kills/10 min - ' + str(tank_data['obj_kills_per_10']) + '\n'
                                    + 'Elims/10 min - ' + str(tank_data['elims_per_10']) + '\n'
                                    + 'Winrate - ' + str(tank_data['winrate']) + '%', file=File('hero_images/' + tank_data['image']))
                    tank_dicts.append(tank_data)

                sorted_tank_dicts = sorted(tank_dicts, key=lambda x:x['winrate'], reverse=True)

                for i in range(len(dmg_heroes)):
                    dmg_data = {}
                    dmg_data['hero'] = dmg_heroes[i]
                    dmg_data['image'] = dmg_heroes[i] + '.png'
                    try:
                        dmg_data['games_played'] = career_data[dmg_heroes[i]]['game']['games_played']
                    except:
                        dmg_data['games_played'] = 0
                    try:
                        dmg_data['deaths_per_10'] = career_data[dmg_heroes[i]]['average']['deaths_avg_per_10_min']
                    except:
                        dmg_data['deaths_per_10'] = 0
                    try:
                        dmg_data['hero_dmg_per_10'] = career_data[dmg_heroes[i]]['average']['hero_damage_done_avg_per_10_min']
                    except:
                        dmg_data['hero_dmg_per_10'] = 0
                    try:
                        dmg_data['elims_per_10'] = career_data[dmg_heroes[i]]['average']['eliminations_avg_per_10_min']
                    except:
                        dmg_data['elims_per_10'] = 0
                    try:
                        dmg_data['final_blows_per_10'] = career_data[dmg_heroes[i]]['average']['final_blows_avg_per_10_min']
                    except:
                        dmg_data['final_blows_per_10'] = 0

                    if dmg_data['games_played'] > 1:
                        dmg_data['winrate'] = summary_data['heroes'][dmg_heroes[i]]['winrate']
                    else:
                        dmg_data['winrate'] = 0
                    if arg2 == dmg_heroes[i]:
                        await ctx.send('Your ' + arg2 + ' advanced stats:\n'
                                    + 'Games played - '+ str(dmg_data['games_played']) +'\n'
                                    + 'Deaths/10 min - ' + str(dmg_data['deaths_per_10']) + '\n'
                                    + 'Hero damage/10 min - ' + str(dmg_data['hero_dmg_per_10']) + '\n'
                                    + 'Final blows/10 min - ' + str(dmg_data['final_blows_per_10']) + '\n'
                                    + 'Elims/10 min - ' + str(dmg_data['elims_per_10']) + '\n'
                                    + 'Winrate - ' + str(dmg_data['winrate']) + '%', file=File('hero_images/' + dmg_data['image']))
                    dmg_dicts.append(dmg_data)

                sorted_dmg_dicts = sorted(dmg_dicts, key=lambda x:x['winrate'], reverse=True)
                for i in range(len(supp_heroes)):
                    supp_data = {}
                    supp_data['hero'] = supp_heroes[i]
                    supp_data['image'] = supp_heroes[i] + '.png'
                    try:
                        supp_data['games_played'] = career_data[supp_heroes[i]]['game']['games_played']
                    except:
                        supp_data['games_played'] = 0
                    try:
                        supp_data['deaths_per_10'] = career_data[supp_heroes[i]]['average']['deaths_avg_per_10_min']
                    except:
                        supp_data['deaths_per_10'] = 0
                    try:
                        supp_data['hero_dmg_per_10'] = career_data[supp_heroes[i]]['average']['hero_damage_done_avg_per_10_min']
                    except:
                        supp_data['hero_dmg_per_10'] = 0
                    try:
                        supp_data['elims_per_10'] = career_data[supp_heroes[i]]['average']['eliminations_avg_per_10_min']
                    except:
                        supp_data['elims_per_10'] = 0
                    try:
                        supp_data['healing_per_10'] = career_data[supp_heroes[i]]['average']['healing_done_avg_per_10_min']

                    except:
                        supp_data['healing_per_10'] = 0

                    if supp_data['games_played'] > 1:
                        supp_data['winrate'] = summary_data['heroes'][supp_heroes[i]]['winrate']
                    else:
                        supp_data['winrate'] = 0
                    if arg2 == supp_heroes[i]:
                        await ctx.send('Your ' + arg2 + ' advanced stats:\n'
                                    + 'Games played - '+ str(supp_data['games_played']) +'\n'
                                    + 'Deaths/10 min - ' + str(supp_data['deaths_per_10']) + '\n'
                                    + 'Hero damage/10 min - ' + str(supp_data['hero_dmg_per_10']) + '\n'
                                    + 'Healing/10 min - ' + str(supp_data['healing_per_10']) + '\n'
                                    + 'Elims/10 min - ' + str(supp_data['elims_per_10']) + '\n'
                                    + 'Winrate - ' + str(supp_data['winrate']) + '%', file=File('hero_images/' + supp_data['image']))
                    supp_dicts.append(supp_data)
                sorted_supp_dicts = sorted(supp_dicts, key=lambda x:x['winrate'], reverse=True)
                if not hero_stats:
                    await ctx.send('Your top 3 tanks in competitive this season: \n' + sorted_tank_dicts[0]['hero'] + ' - ' + str(sorted_tank_dicts[0]['winrate']) + '% winrate in ' 
                    + str(sorted_tank_dicts[0]['games_played']) + ' games played\n', files=[File('hero_images/' + sorted_tank_dicts[0]['image'])])
                    await ctx.send(sorted_tank_dicts[1]['hero'] + ' - ' + str(sorted_tank_dicts[1]['winrate']) + '% winrate in '
                    + str(sorted_tank_dicts[1]['games_played']) + ' games played\n', file=File('hero_images/' + sorted_tank_dicts[1]['image']))
                    await ctx.send(sorted_tank_dicts[2]['hero'] + ' - ' + str(sorted_tank_dicts[2]['winrate']) + '% winrate in '
                    + str(sorted_tank_dicts[2]['games_played']) + ' games played\n ', file=File('hero_images/' + sorted_tank_dicts[2]['image']))
                    await ctx.send('Your top 3 dps in competitive this season: \n' + sorted_dmg_dicts[0]['hero'] + ' - ' + str(sorted_dmg_dicts[0]['winrate']) + '% winrate in ' 
                    + str(sorted_dmg_dicts[0]['games_played']) + ' games played\n', file=File('hero_images/' + sorted_dmg_dicts[0]['image']))
                    await ctx.send(sorted_dmg_dicts[1]['hero'] + ' - ' + str(sorted_dmg_dicts[1]['winrate']) + '% winrate in '
                    + str(sorted_dmg_dicts[1]['games_played']) + ' games played\n', file=File('hero_images/' + sorted_dmg_dicts[1]['image']))
                    await ctx.send(sorted_dmg_dicts[2]['hero'] + ' - ' + str(sorted_dmg_dicts[2]['winrate']) + '% winrate in '
                    + str(sorted_dmg_dicts[2]['games_played']) + ' games played\n', file=File('hero_images/' + sorted_dmg_dicts[2]['image']))
                    await ctx.send('Your top 3 supports in competitive this season: \n' + sorted_supp_dicts[0]['hero'] + ' - ' + str(sorted_supp_dicts[0]['winrate']) + '% winrate in ' 
                    + str(sorted_supp_dicts[0]['games_played']) + ' games played\n' , file=File('hero_images/' + sorted_supp_dicts[0]['image']))
                    await ctx.send(sorted_supp_dicts[1]['hero'] + ' - ' + str(sorted_supp_dicts[1]['winrate']) + '% winrate in '
                    + str(sorted_supp_dicts[1]['games_played']) + ' games played\n', file=File('hero_images/' + sorted_supp_dicts[1]['image']))
                    await ctx.send(sorted_supp_dicts[2]['hero'] + ' - ' + str(sorted_supp_dicts[2]['winrate']) + '% winrate in '
                    + str(sorted_supp_dicts[2]['games_played']) + ' games played.', file=File('hero_images/' + sorted_supp_dicts[2]['image']))


bot.run(TOKEN)
