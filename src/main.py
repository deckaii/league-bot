import discord
from discord.ext import commands
import ws_opgg

token = open("src/token.txt", "r").read()

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def info(ctx, *, arg):
    names = arg.split(",")
    for name in names:
        data = ws_opgg.get_data(f'https://euw.op.gg/summoners/euw/{name}')
        embed = discord.Embed(
            title="Op.gg Link",
            url=f'https://euw.op.gg/summoners/euw/{name}',
            color=discord.Color.blue()
        )
        embed.set_thumbnail(
            url='https://s-lol-web.op.gg/images/reverse.rectangle.png')
        embed.set_author(name=name, icon_url=data['profimg'])

        embed.add_field(name="Level", value=data['level'], inline=True)
        embed.add_field(
            name="Rank", value=data['rank'].title() + "\n", inline=True)
        # embed.add_field(
        #     name="Win/Lose", value=data['win-lose'] + "\n", inline=True)

        for char, info in data['chars_played'].items():
            embed.add_field(
                name=char, value=f'᲼**CS** ᲼᲼᲼᲼᲼{info["cs"]}\n᲼**KDA**᲼᲼᲼᲼{info["kda"]}\n᲼**Winrate**᲼{info["win_rate"]}%\n᲼**Games**᲼᲼{info["games_played"]}', inline=False)

        embed.set_footer()
        await ctx.send(embed=embed)


bot.run(token)
