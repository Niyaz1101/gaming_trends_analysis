import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from base_collector import BaseCollector
from config.settings import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET

class TwitchCollector(BaseCollector):
    
    #Class-level caches
    _game_id_cache: Dict[str, str] = {}
    _token: Optional[str] = None
    _token_expiry: Optional[datetime] = None
    _headers: Optional[Dict] = None

    def __init__(self):
        super().__init__('twitch')
        self.base_url = "https://api.twitch.tv/helix"
        self.max_retries = 3
        self.timeout = 10 #seconds
        self.headers = None 

    def _authenticate(self):
        """Get permission to use Twitch API (with caching and retry)"""
        #Use cached token if still valid
        if(self._token and self._token_expiry and
            datetime.now() < self._token_expiry):
            self.token = self._token
            self.headers = self._headers
            return
        
        auth_url = "https://id.twitch.tv/oauth2/token"
        params = {
            'client_id': TWITCH_CLIENT_ID,
            'client_secret': TWITCH_CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(auth_url, params=params, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()

                TwitchCollector._token = data["access_token"]
                TwitchCollector._token_expiry = datetime.now() + timedelta(seconds=data["expires_in"])
                TwitchCollector._headers = {
                    'Authorization': f"Bearer {data['access_token']}",
                    'Client-id':TWITCH_CLIENT_ID
                }

                self.token = self._token
                self.headers = self._headers
                break

            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed to authenticate after {self.max_retries} attempts:{e}")
                self.logger.warning(f"Auth attempt {attempt +1} failed, everything...")

    def collect_game_data(self, game_name: str) -> dict:
        """Collect game data from Twitch API (with caching and retry)"""
        try:

            if not self.headers:
                self._authenticate()
            
            game_id = self._get_game_id(game_name)
            if not game_id:
                self.logger.warning(f"Game '{game_name}' not found on Twitch")
                return self._empty_result(game_name)
            
            streams_data = self._get_streams(game_id)

            if not streams_data:
                return self._empty_result(game_name)
        
            viewer_counts = [s['viewer_count'] for s in streams_data]
            total_viewers = sum(viewer_counts)
            stream_count = len(streams_data)
            avg_viewers = total_viewers/stream_count

            top_stream = max(streams_data, key=lambda x: x['viewer_count'])

            result = {
                'game_name' : game_name,
                'timestamp' : datetime.now(),
                'total_viewers' : total_viewers,
                'stream_count' : stream_count,
                'average_viewers_per_stream' : round(avg_viewers, 2),
                'top_streamer' : top_stream['user_name'],
                'top_stream_viewers' : top_stream['viewer_count'],
                'top_5_viewers' : viewer_counts[:5],
                'source' : 'twitch'
             }

            self.save_raw_data({
                'streams' : streams_data[:20],
                'metadata' : result
            }, game_name)
        
            return result
    
        except Exception as e:
            self.logger.error(f"Error collecting game data: {e}")
            return self._empty_result(game_name, error=str(e))
        
    def collect_batch(self, game_names: List[str], max_workers: int = 5) -> List[dict]:
        """Collect data for multiple games in parallel"""

        results = [] 

        with ThreadPoolExecutor(max_workers=max_workers) as executor:

            future_to_game = {
                executor.submit(self.collect_game_data, game): game
                for game in game_names
            }

            for future in as_completed(future_to_game):
                game = future_to_game[future]
                try:
                    result = future.result()
                    results.append(result)
                    self.logger.info(f"Collected data for {game}: {result['total_viewers']} viewers")
                except Exception as e:
                    self.logger.error(f"Error collecting data for {game}: {e}")
                    results.append(self._empty_result(game, error=str(e)))

            return results
        
    
    def _get_game_id(self, game_name: str) -> Optional[str]:
        """Convert game name to Twitch's internal ID(with caching)"""

        if game_name in self._game_id_cache:
            return self._game_id_cache[game_name]
        
        try:
            response = requests.get(
                f"{self.base_url}/games",
                headers=self.headers,
                params={'name': game_name},
                timeout=self.timeout
            )
            response.raise_for_status()

            games = response.json().get('data', [])

            if games:
                game_id = games[0]['id']

                self._game_id_cache[game_name] = game_id
                self.logger.debug(f"Cached game ID for {game_name}: {game_id}")
                return game_id
            
            return None
        
        except Exception as e:
            self.logger.error(f"Error getting game ID for {game_name}: {e}")
            return None
        
    def _get_streams(self, game_id: str, max_streams: int = 500) -> list:
        """ Get active streams for a game
            Limited to max_streams to prevent huge responses
        """

        streams = []
        params = {
            'game_id': game_id,
            'first': 100
        }

        while len(streams) < max_streams:
            try:
                response = requests.get(
                    f"{self.base_url}/streams",
                    headers=self.headers,
                    params=params,
                    timeout=self.timeout
                )
                response.raise_for_status()

                data = response.json()
                batch = data.get('data', [])

                if not batch:
                    break

                streams.extend(batch)

                cursor = data.get('pagination', {}).get('cursor')
                if not cursor:
                    break

                params['after'] = cursor
                self._rate_limit()

            except Exception as e:
                self.logger.error(f"Error fetching streams: {e}")
                break

        return streams[:max_streams]
    
    def get_trending_games(self, limit: int = 20) -> List[dict]:
        """
        Get currently trending games on Twitch
        Useful for discovery
        """
        if not self.headers:
            self._authenticate()

        try:
            response = requests.get(
                f"{self.base_url}/games/top",
                headers=self.headers,
                params={'first': limit},
                timeout=self.timeout
            )
            response.raise_for_status()

            games = response.json().get('data', [])
            return [{'name': g['name'], 'id': g['id']} for g in games]
        
        except Exception as e:
            self.logger.error(f"Error fetching trending games: {e}")
            return []
    
    def _empty_result(self, game_name: str, error: str = None) -> dict:
        #Return empty data when game isn't found or error occurs
        return {
            'game_name': game_name,
            'timestamp': datetime.now(),
            'total_viewers': 0,
            'stream_count': 0,
            'average_viewers_per_stream': 0,
            'top_streamer': 'Not Found',
            'top_streamer_viewers': 0,
            'top_5_viewers': [],
            'source':'twitch',
            'error': error
        }