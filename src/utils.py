import os
import json
from typing import Dict
from dotenv import load_dotenv

def load_config() -> Dict:
    """
    Load configuration from config.json file.
    
    Returns:
        Dict: Configuration parameters
        
    Raises:
        FileNotFoundError: If config file is missing
        json.JSONDecodeError: If config file is invalid
    """
    try:
        with open('config/config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("config.json not found in config directory")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in config.json")

def get_api_key() -> str:
    """
    Get Together AI API key from environment variables.
    
    Returns:
        str: API key
        
    Raises:
        ValueError: If API key is not found
    """
    load_dotenv()
    api_key = os.getenv('TOGETHER_API_KEY')
    if not api_key:
        raise ValueError("TOGETHER_API_KEY not found in environment variables")
    return api_key

def format_price(price: float) -> str:
    """
    Format price with proper decimal places and commas.
    
    Args:
        price (float): Price to format
        
    Returns:
        str: Formatted price string
    """
    return f"${price:,.2f}"