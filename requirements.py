import os
import discord
from discord.ext import commands
from discord.utils import get
import openai
import time
import datetime
from time import sleep
import json
import asyncio
import requests
import random
print(f'🟢⚫⚫')
sleep(0.5)
print(f'🟢🟢⚫')
sleep(0.5)
print(f'🟢🟢🟢')
sleep(0.5)
print(f'success loading libraries')
sleep(0.5)


intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True
intents.bans = True
intents.emojis = True
intents.integrations = True
intents.webhooks = True
intents.invites = True
intents.voice_states = True
intents.presences = True
intents.reactions = True
intents.typing = True




