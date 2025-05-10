from keep_alive import keep_alive

import discord
from discord.ext import commands

from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("DISCORD_TOKEN")
print(f"token: {bot_token}")
if bot_token is None:
    raise ValueError("Token non trovato. Assicurati di averlo impostato correttamente.")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Inserisci qui gli ID numerici dei canali
WELCOME_CHANNEL_ID = 1184799804421832778  # Sostituisci con il vero ID del canale welcome
ROLE_CHANNEL_ID = 1366500772090740923     # Sostituisci con il vero ID del canale dei ruoli

EMOJI_ROLE_MAP = {
    "🇨🇳": 1363678563265679390,
    "🇪🇸": 1363678270511513690,
    "🇬🇧": 1363678414808158228,
    "🇮🇹": 1363678105461461153,
}

role_message_id = None

@bot.event
async def on_ready():
    print(f"Bot avviato come {bot.user}(event on_ready)")
    channel = bot.get_channel(ROLE_CHANNEL_ID)   # tra virgolette id channel , in caso non funzione toglierle.
    if channel:
        # message = await channel.send(
        #     "**What language do you speak?**\n"
        #     "🇨🇳 中文\n"
        #     "🇪🇸 Español\n"
        #     "🇬🇧 English\n"
        #     "🇮🇹 Italiano"
        # )
        global role_message_id
        # role_message_id = message.id
        role_message_id = 1369437952257818704
        # for emoji in EMOJI_ROLE_MAP.keys():
        #     await message.add_reaction(emoji)

@bot.event
async def on_member_join(member):
    print("avvio event on_member_join")
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    print(f"channel: {channel}")
    print(f"member: {member}")
    if channel:
        embed = discord.Embed(
            title="欢迎来到小欣的小睡屋🍓",
            description=f"{member.mention} 欢迎光临～",
            color=discord.Color.pink()
        )
        embed.set_image(url="https://i.imgur.com/VyxMRLB.jpeg")  # Sostituisci con la tua immagine
        await channel.send(embed=embed)

@bot.event
async def on_raw_reaction_add(payload): #(aggiunge i ruoli quando qualcuno li clicca)
    print("avvio event on_raw_reaction_add")
    global role_message_id
    if payload.message_id != role_message_id or payload.user_id == bot.user.id:
        return
    guild = bot.get_guild(payload.guild_id)
    role_id = EMOJI_ROLE_MAP.get(str(payload.emoji))
    if role_id:
        role = guild.get_role(role_id)
        member = guild.get_member(payload.user_id)
        if role and member:
            await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    print("avvio event on_raw_reaction_remove")
    global role_message_id
    if payload.message_id != role_message_id:
        return
    guild = bot.get_guild(payload.guild_id)
    role_id = EMOJI_ROLE_MAP.get(str(payload.emoji))
    if role_id:
        role = guild.get_role(role_id)
        member = guild.get_member(payload.user_id)
        if role and member:
            await member.remove_roles(role)

# Inserisci qui il tuo token in modo sicuro (meglio tramite variabile d'ambiente)
bot.run(f"{bot_token}")
print("avvio bot.run")