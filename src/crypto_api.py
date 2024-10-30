import requests
import time
from typing import Dict, Tuple

class CryptoAPI:
    def __init__(self):
        """Initialize the CryptoAPI with cache and rate limiting."""
        self.price_cache: Dict[str, Tuple[float, Dict]] = {}
        self.last_api_call: float = 0
    
    def get_price(self, symbol: str, cache_duration: int, rate_limit_delay: float) -> Dict:
        """
        Get cryptocurrency price with caching and rate limiting.
        
        Args:
            symbol (str): Cryptocurrency symbol
            cache_duration (int): How long to cache prices (in seconds)
            rate_limit_delay (float): Minimum delay between API calls
            
        Returns:
            Dict: Price data
            
        Raises:
            Exception: If API call fails
        """
        current_time = time.time()
        
        # Check cache
        if symbol in self.price_cache:
            cache_time, cache_data = self.price_cache[symbol]
            if current_time - cache_time < cache_duration:
                return cache_data
        
        # Rate limiting
        if current_time - self.last_api_call < rate_limit_delay:
            time.sleep(rate_limit_delay)
        
        try:
            # Using CoinGecko API
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            self.price_cache[symbol] = (current_time, data)
            self.last_api_call = current_time
            
            return data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching crypto price: {str(e)}")

    def clear_cache(self):
        """Clear the price cache"""
        self.price_cache.clear()