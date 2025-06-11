"""
BASE COLLECTOR: Parent class that all collectors inherit from
Handles common tasks like logging, rate limiting and saving data

"""

from abc import ABC, abstractmethod
import logging
import time
from datetime import datetime
from pathlib import Path
import json


class BaseCollector(ABC):
    #Base class with common functionality for all data collectors

    def __init__(self, source_name: str):

        self.source_name = source_name
        self.logger = self._setup_logger()

        self.last_request_time = 0
        self.min_request_interval = 1

    def _setup_logger(self):
        
        #Create a logger for this collector
        logger = logging.getLogger(f"collector.{self.source_name}")

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

        return logger
    
    def _rate_limit(self):
        
        #Wait between requests to avoid hitting API limits
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def save_raw_data(self, data: dict, game_name: str):
        #Save collected data to a JSON file
        from config.settings import RAW_DATA_DIR

        #Create folder for this data source
        source_dir = RAW_DATA_DIR/self.source_name
        source_dir.mkdir(parents=True, exist_ok=True)

        #Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_game_name = game_name.replace(' ','_').replace(':','')
        filename = f"{safe_game_name}_{timestamp}.json"
        filepath = source_dir/filename

        #Save the data
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)

        self.logger.info(f"Saved {self.source_name} data to {filename}")

    @abstractmethod
    def collect_game_data(self, game_name: str) -> dict:

        """
        Each collector must implement this method
        It should return a dictionary with the collected data

        """
        pass


