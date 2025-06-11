import os
from dotenv import load_dotenv
from pathlib import Path

#Load environment variables
load_dotenv()

#Project paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR/"data"
RAW_DATA_DIR = DATA_DIR/"raw"
PROCESSED_DATA_DIR = DATA_DIR/"processed"

#API Configuration
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

#Data collection settings
GAMES_TO_TRACK = [
    #Current/Recent games to analyze
    "Helldivers 2",
    "Palworld",
    "Lethal Company",
    "Pizza Tower",
    "Balatro",
    "Content Warning",
    "Buckshot Roulette",

    #Control group(established games)
    "Minecraft",
    "Fortnite",
    "League of Legends"
]

SIGNAL_THRESHOLDS = {
    'twitch_growth_rate': 0.5,
    'discord_emoji_rate': 10,
    'tiktok_audio_uses': 1000,
    'speed_submissions': 5,
}
