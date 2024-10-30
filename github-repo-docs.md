# Crypto AI Assistant

A multilingual cryptocurrency assistant powered by LLaMA 3.1 and real-time price data. The assistant provides cryptocurrency information and price updates while handling multiple languages through an intuitive chat interface.

## 🌟 Features

- Real-time cryptocurrency price tracking
- Multilingual support with English responses
- Interactive price charts and visualizations
- Rate-limited and cached API calls
- Both web (Streamlit) and CLI interfaces

## 🛠️ Technology Stack

- **Language Model**: LLaMA 3.1 8B via Together AI
- **Frontend**: Streamlit
- **APIs**: Together AI, CoinGecko
- **Visualization**: Plotly
- **Caching**: Python LRU Cache

## 📋 Prerequisites

- Python 3.8+
- Together AI API key
- Git

## 🚀 Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crypto-ai-assistant.git
cd crypto-ai-assistant
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Edit `.env` and add your Together AI API key:
```
TOGETHER_API_KEY=your_api_key_here
```

5. Configure application settings:
```bash
cp config/config.example.json config/config.json
```
Adjust settings in `config.json` as needed:
```json
{
    "cache_duration": 300,
    "rate_limit_delay": 1
}
```

## 🎯 Usage

### Web Interface
```bash
streamlit run app.py
```
Access the web interface at `http://localhost:8501`

### Command Line Interface
```bash
python main.py
```

## 🤖 Prompt Engineering Approach

The assistant uses a carefully crafted prompt structure to maintain consistent behavior:

1. **Language Detection**:
   - System prompt focuses on ISO language code identification
   - Low temperature (0.1) for consistent results

2. **Response Generation**:
   - Acknowledges user's language while maintaining English responses
   - Includes real-time price data when relevant
   - Maintains conversation context for coherent dialogue

### Example Conversations

```
User: ¿Cuál es el precio del Bitcoin?
Assistant: I notice you're asking in Spanish. The current Bitcoin price is $67,890.45 USD. 
Let me know if you need any other cryptocurrency information!

User: Explain blockchain technology
Assistant: A blockchain is a decentralized digital ledger that securely records transactions 
across a network of computers. Each block contains transaction data and is linked to the 
previous block, creating an unalterable chain of information.

User: ビットコインの価格は？
Assistant: I see you're asking about Bitcoin's price in Japanese. The current Bitcoin price 
is $67,890.45 USD. I can also provide information about other cryptocurrencies if you're 
interested.
```

## ⚠️ Limitations and Assumptions

1. **Language Support**:
   - Relies on LLaMA's language detection capabilities
   - May have varying accuracy for less common languages
   - Responses are English-only

2. **Rate Limiting**:
   - Default 1 second delay between API calls
   - May impact response time during heavy usage
   - Cache duration set to 5 minutes by default

3. **Price Data**:
   - Assumes CoinGecko API availability
   - Limited to supported cryptocurrencies
   - Price updates may have slight delays

4. **Model Limitations**:
   - Uses LLaMA 3.1 8B model
   - May have knowledge cutoff date limitations
   - Response quality depends on prompt engineering

## 📁 Project Structure

```
crypto-ai-assistant/
├── app.py                 # Streamlit web interface
├── main.py               # CLI entry point
├── requirements.txt      # Project dependencies
├── .env.example         # Environment variables template
├── config/
│   ├── config.example.json  # Configuration template
│   └── config.json         # Active configuration
└── src/
    ├── agent.py         # Core AI agent implementation
    ├── crypto_api.py    # Cryptocurrency API wrapper
    └── utils.py         # Utility functions
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
