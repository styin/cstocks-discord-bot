import discord
from discord.ext import commands

import os
import traceback
from datetime import date, datetime

from dotenv import load_dotenv
load_dotenv()

class Utils(commands.Cog):
    def __init__(self, bot, debug=False):
        self.bot = bot
        self.debug = debug or bool(os.getenv('DEBUG'))
        self._last_member = None
        if self.debug:
            print("[LOG] Debugger Messages are ENABLED for utils_cog")
    
    # Greetings and Information
    @commands.command(
        aliases=['hi','info']
    )
    async def hello(self, ctx, *, member: discord.Member = None):
        """This command prompts bot to return some basic information"""
        try:
            member = member or ctx.author
            # title message
            if self._last_member is None or self._last_member.id != member.id:
                title_msg = "Hello {0.name}~ :sparkles:".format(member)
            else:
                title_msg = "Hello {0.name}... Don't I know you already...?".format(member)
            self._last_member = member
            # message embed
            embed = discord.Embed(
                title       = title_msg,
                description = "I am **the CStocks Bot**. I can help\
                    you to track the price of csgo items  :money_with_wings:\
                    \n\n:warning:\n*prices for reference only; do your own due diligence*"
                    .format(os.getenv('PREFIX')),
                colour      = discord.Colour.from_str(os.getenv('DEFAULT_COLOUR'))
            )
            embed.add_field(
                name        = "prefix",
                value       = self.bot.command_prefix,
                inline      = True
            )
            embed.add_field(
                name        = "developed by",
                value       = "sty -2023",
                inline      = True
            )
            embed.add_field(
                name        = "version",
                value       = os.getenv('VERSION'),
                inline      = True
            )
            # response
            await ctx.channel.send(embed=embed)
        except Exception as e:
            print("[WARNING] hello_command failed")
            print("[WARNING]", traceback.format_exc())
            await ctx.reply("**Error** | The command could not be processed! :warning:\n"+\
                            "```\nUnknown Exception: [{0}]\n```".format(e))
    
    # Safe Logout
    @commands.command(
        aliases=['exit','quit','shutdown']
    )
    async def logout(self, ctx):
        """This command safely logs out the bot"""
        if ctx.author.id == int(os.getenv('styID')):
            print("[LOG] Scheduled Shutdown Initiated")
            embed = discord.Embed(
                title       = "Safely shutting down... :white_check_mark:",
                description = "A scheduled shutdown has been initiated, and the bot is logging off.",
                colour      = discord.Colour.from_str(os.getenv('DEFAULT_COLOUR'))
            )
            await ctx.reply(embed=embed)
            await self.bot.close()
        else:
            print("[LOG] Unauthorized Logout")
            embed = discord.Embed(
                title       = "Unauthorized Activity :lock:",
                description = "Insufficient Permissions! Please verify your clearance.",
                colour      = discord.Colour.from_str(os.getenv('DEFAULT_COLOUR'))
            )
            await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Utils(bot, debug=False))

print("[COG] Loaded utility features")