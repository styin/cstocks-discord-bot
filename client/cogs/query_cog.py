import re
import discord
from discord.ext import commands

import os
import traceback

from dotenv import load_dotenv
load_dotenv()

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions

class Query(commands.Cog):
    def __init__(self, bot, debug=False):
        self.bot = bot
        self.debug = debug or bool(os.getenv('DEBUG'))
        self._last_member = None
        self.scraper_opts = ChromeOptions()
        self.scraper_opts.add_argument("--headless")
        self.scraper_browser = Chrome(options=self.scraper_opts)
        if self.debug:
            print("[LOG] Debugger Messages are ENABLED for query_cog")
    
    @commands.command(
        aliases=['analyse','analysis']
    )
    async def analyze(self, ctx, ticker=None):
        """This command queries for a quote of the items in the portfolio"""
        pass

    @commands.command(
        aliases=['p']
    )
    async def price(self, ctx, id=None):
        
        if ctx.author.id == int(os.getenv('styID')):
            pass
        else:
            print("[LOG] Unauthorized Use")
            embed = discord.Embed(
                title       = "Unauthorized Activity :lock:",
                description = "Insufficient Permissions! Please verify your clearance.",
                colour      = discord.Colour.from_str(os.getenv('DEFAULT_COLOUR'))
            )
            await ctx.reply(embed=embed)
        
        if not id.isdigit():
            await ctx.reply("**Error** | I can't recognize this id... :warning:\n"+\
                            "```\n{0}price <id:numeral>\n```".format(os.getenv('PREFIX')))
            return
        try:
            url = "https://buff.163.com/goods/" + id + "?from=market#tab=selling"
            self.scraper_browser.get(url)

            item_name = self.scraper_browser.find_element('class name', 'detail-cont').text
            price_list = self.scraper_browser.find_element('class name', 'scope-btns').text
            price_list = re.findall(r"\S+(?:\s\S+){2}", price_list)
            print(price_list)
            embed = discord.Embed(
                title       = id,
                description = item_name,
                colour      = discord.Colour.from_str(os.getenv('DEFAULT_COLOUR'))
            )
            for float in price_list:
                str = float.split(' ', 1)
                embed.add_field(
                    name        = str[0],
                    value       = str[1],
                    inline      = True
                )
        except Exception as e:
            print("[WARNING] price command failed")
            print("[WARNING]", traceback.format_exc())
            await ctx.reply("**Error** | The command could not be processed! :warning:\n"+\
                            "```\nUnknown Exception: [{0}]\n```".format(e))
        else:
            await ctx.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Query(bot, debug=False))

print("[COG] Loaded query features")