import discord
import requests

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if "hello" in message.content.lower():
        await message.channel.send("Hi")

@client.event
async def on_message(message):
    if "are you live?" in message.content.lower():
        await message.channel.send("Yep! I'm ")

@client.event
async def on_message(message):
    if "/pokemon_stats" in message.content.lower():
        pokemon = message.content.split(" ")[1]
        url = f'http://pokeapi.co/api/v1/pokemon/{pokemon}/'
        try:
            response = requests.get(url)
            pokeinfo = response.json()
            text = ""
            for stat in pokeinfo['stats']:
                text += stat['stat']['name'] + ": " + str(stat['base_stat']) + "\n"
            await message.channel.send(text)
        except:
            await message.channel.send("Pokemon não encontrado.")

@client.event
async def on_message(message):
    if "obrigado" in message.content.lower():
        await message.channel.send("Disponha! Quando precisar é só chamar! 👋")

client.run("<--YOUR_TOKEN-->")