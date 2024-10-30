from typing import Dict, List, Optional
from together import Together
from .crypto_api import CryptoAPI
from functools import lru_cache
import json
import time

class CryptoAgent:
    def __init__(self, api_key: str):
        """
        Initialize the CryptoAgent with API key and configuration.
        
        Args:
            api_key (str): Together AI API key
        """
        self.together_client = Together(api_key=api_key)
        self.model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

        self.crypto_api = CryptoAPI()
        self.conversation_history = []
        
        # Load configuration
        with open('config/config.json', 'r') as f:
            config = json.load(f)
            self.cache_duration = config.get('cache_duration', 300)
            self.rate_limit_delay = config.get('rate_limit_delay', 1)

    @lru_cache(maxsize=128)
    def detect_language(self, text: str) -> str:
        """
        Detect the language of input text using LLaMA model.
        
        Args:
            text (str): Input text to detect language
            
        Returns:
            str: ISO language code
        """
        try:
            response = self.together_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a language detection tool. Respond with only the ISO language code."
                    },
                    {
                        "role": "user",
                        "content": f"What language is this text in: {text}"
                    }
                ],
                max_tokens=10,
                temperature=0.1
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return "en"  # Default to English on error

    def get_crypto_price(self, symbol: str = "bitcoin") -> Dict:
        """
        Fetch cryptocurrency price with caching and rate limiting.
        
        Args:
            symbol (str): Cryptocurrency symbol (default: "bitcoin")
            
        Returns:
            Dict: Price data
        """
        return self.crypto_api.get_price(symbol, self.cache_duration, self.rate_limit_delay)

    def process_message(self, user_message: str) -> str:
        """
        Process user message and return appropriate response.
        
        Args:
            user_message (str): User's input message
            
        Returns:
            str: Agent's response
        """
        try:
            # Detect language
            detected_lang = self.detect_language(user_message)
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message,
                "detected_language": detected_lang
            })
            
            # Create system message
            system_message = {
                "role": "system",
                "content": f"""You are a helpful cryptocurrency assistant. 
                The user is writing in {detected_lang}. 
                Always respond in English, but acknowledge their language.
                You have access to real-time crypto prices.
                Keep responses concise and focused on cryptocurrency information."""
            }
            
            # Generate response using LLaMA
            response = self.together_client.chat.completions.create(
                model=self.model,
                messages=[
                    system_message,
                    *[{"role": msg["role"], "content": msg["content"]} 
                      for msg in self.conversation_history[-5:]]  # Keep last 5 messages
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Check if price fetch is needed
            if any(keyword in user_message.lower() for keyword in ["price", "valor", "precio", "worth", "cost", "価格"]):
                try:
                    crypto_data = self.get_crypto_price("bitcoin")
                    price = crypto_data.get('bitcoin', {}).get('usd', 0)
                    assistant_response += f"\nCurrent BTC Price: ${price:,.2f} USD"
                except Exception as e:
                    assistant_response += f"\nSorry, I couldn't fetch the current price. Error: {str(e)}"
            
            # Add response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_response
            })
            
            return assistant_response
            
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def clear_context(self):
        """Clear conversation history"""
        self.conversation_history = []
