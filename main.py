import discord
import os
import requests
import json
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
token = os.getenv("DISCORD_TOKEN")
weather_token = os.getenv("WEATHER_API_KEY")
bot = commands.Bot(command_prefix="/", intents=intents)

def make_a_string(data):
    weather_string = f'''Getting weather for {data['location']['name']}, {data['location']['country']}\n
Temperature: {data['current']['temp_f']}°F / {data['current']['temp_c']}°C
Condition: {data['current']['condition']['text']}
                      '''
    return weather_string, data['current']['condition']['icon']

def get_weather(city):
    response=requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={weather_token}&q={city}&days=1&aqi=no")
    data = response.json()
    return make_a_string(data)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 
    if message.content.startswith('/get'):
        parts = message.content.split()
        city = '+'.join(name for name in parts[1:])
        weather, image = get_weather(city)
        await message.channel.send(weather)
        await message.channel.send(f"https:{image}")

bot.run(token)