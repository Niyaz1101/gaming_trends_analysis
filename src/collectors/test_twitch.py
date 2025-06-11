"""
Test script: Check if Twitch collector is working properly

"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.collectors.twitch_collector import TwitchCollector
import json

def test_single_game():
    #Test collecting data for one game
    print("=== Testing Single Game Collection === \n")

    collector = TwitchCollector()

    game = "Fortnite"
    print(f"Collecting data for: {game}")

    result = collector.collect_game_data(game)

    print(f"\n Results for {game}:")
    print(f" Total Viewers: {result['total_viewers']:,}")
    print(f" Active Streams: {result['average_viewers_per_stream']}")
    print(f" Top Streamer: {result['top_streamer']}({result['top_stream_viewers']:,}viewers)")

def test_batch_collection():
    """Test collecting data for multiple games"""
    print("=== Testing Batch Collection === \n")

    collector = TwitchCollector()

    games = ["Balatro", "Palworld", "Helldivers 2", "Clair Obscur: Expedition 33", "Animal Well"]
    print(f"Collecting data for: {', '.join(games)}")

    results = collector.collect_batch(games, max_workers=3)

    #Show Results
    print("\nBatch Results: ")
    for result in results:
        print(f"\n{result['game_name']}:")
        print(f" Viewers: {result['total_viewers']:,}")
        print(f" Streams: {result['stream_count']}")


def test_trending_games():
    """Test collecting trending games"""
    print("=== Testing Trending Games Collection === \n")

    collector = TwitchCollector()
    trending = collector.get_trending_games(limit=10)

    print("Top 10 Games on Twitch Right Now:")
    for i, game in enumerate(trending, 1):
        print(f"{i}. {game['name']}")


if __name__ == "__main__":
    test_single_game()
    test_batch_collection()
    test_trending_games()