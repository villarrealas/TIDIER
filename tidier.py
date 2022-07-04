
# bot.py
import os
import discord
import json
import logging

from dotenv import load_dotenv
from moves import get_moves
from parse import mad_parse
from command_handler import plain_command_handler, embed_command_handler
from config_interactions import get_dicedisplay
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO) #set logging level to INFO, DEBUG if we want the full dump
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a') #open log file in append mode
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
logger.info (TOKEN)
client = discord.Client()

@client.event
async def on_ready():
    logger.info(f'{client.user} has connected to Discord!')
    servers = list(client.guilds)
    logger.info("Connected on "+str(len(client.guilds))+" servers:")
    for x in range(len(servers)):
        logger.info('   ' + servers[x-1].name)

def msg_log_line(message):
    if message.guild is not None:
        return message.guild.name + "|" + message.channel.name + "|" + message.author.name + "|" + message.content
    else:
        return "[Direct Message]" + "|" + message.author.name + "|" + message.content

#Listen for messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # handle help and all of the playbook interactions
    if message.content.startswith("!"):
        response = plain_command_handler(message)

        if response:
            log_line = msg_log_line(message)
            logger.info(log_line)
            await message.channel.send(response)
            return

        response = embed_command_handler(message)

        if response:
            log_line = msg_log_line(message)
            logger.info(log_line)
            await message.channel.send(embed=response)
            return

    #answer a call for help
    if message.content.startswith("!help"):
        log_line = msg_log_line(message)
        logger.info(log_line)
        help_file = open("help", "r")
        response = help_file.read()

        await message.author.send(response)
        await message.channel.send("I have sent help to your PMs.")

    #list moves#
    if message.content.startswith("!"):
        move_list = get_moves(message)
        if move_list:
            await message.channel.send(move_list)
        #remember generic ! should always be last in the tree#
        else:
            log_line = msg_log_line(message)
            logger.info(log_line)
            response = mad_parse(message)
            if response:
                logger.info(response)
                (response, addendum) = response
#            if addendum is not None:  ##testing if going first made a difference
#                await message.channel.send(content = addendum)
                await message.channel.send(embed=response)
                if addendum is not None:
                    await message.channel.send(content = addendum)
            else : logger.info('no match found for '+message.content)

client.run(TOKEN)
