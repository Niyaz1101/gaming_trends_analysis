import os 
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import (
    TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET,
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

)

import requests
import praw

def test_twitch_connection():
    """Test Twitch API connection"""
    print("Testing Twitch API...")
    
    # Get OAuth token
    auth_url = "https://id.twitch.tv/oauth2/token"
    auth_params = {
        'client_id': TWITCH_CLIENT_ID,
        'client_secret': TWITCH_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    
    try:
        response = requests.post(auth_url, params=auth_params)
        response.raise_for_status()
        
        # Parse JSON first!
        data = response.json()
        token = data['access_token']
        print("Twitch authentication successful!")
        
        # Test API call - get top games
        headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': TWITCH_CLIENT_ID
        }
        
        games_response = requests.get(
            "https://api.twitch.tv/helix/games/top",
            headers=headers,
            params={'first': 5}
        )
        
        if games_response.status_code == 200:
            games = games_response.json()['data']
            print(f"✅ Retrieved {len(games)} top games:")
            for game in games:
                print(f"   - {game['name']}")
        else:
            print(f"Games API error: {games_response.status_code}")
            
    except Exception as e:
        print(f"Twitch API error: {e}")

def test_reddit_connection():
    """Test Reddit API connection"""
    print("\nTesting Reddit API...")

    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )

        # Test by getting hot posts from r/gaming
        subreddit = reddit.subreddit('gaming')
        posts = list(subreddit.hot(limit =5))

        print("Reddit authentication successful")
        print(f"Retrieved {len(posts)} hot posts from r/gaming:")
        for post in posts:
            print(f"  - {post.title[:50]}...")

    except Exception as e:
        print(f"Reddit API error: {e}")

if __name__ == "__main__":
    print("=== Testing API Connections ===\n")
    test_twitch_connection()
    test_reddit_connection()
    print("\n=== Tests Complete ===")