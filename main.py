from src.agent import CryptoAgent
from src.utils import load_config, get_api_key

def main():
    # Load configuration
    config = load_config()
    api_key = get_api_key()
    
    # Initialize agent
    agent = CryptoAgent(api_key)
    
    print("Crypto Agent initialized. Type 'quit' to exit.")
    print("Example commands:")
    print("- What's the current Bitcoin price?")
    print("- ¿Cuál es el precio del Bitcoin?")
    print("- Show me crypto prices")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                break
                
            response = agent.process_message(user_input)
            print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main()