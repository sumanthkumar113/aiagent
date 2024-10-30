# app.py
import streamlit as st
from src.agent import CryptoAgent
from src.utils import get_api_key, load_config
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta

class StreamlitCryptoApp:
    def __init__(self):
        # Initialize the agent
        self.api_key = get_api_key()
        self.config = load_config()
        self.agent = CryptoAgent(self.api_key)
        
        # Initialize session state for message history if it doesn't exist
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        if 'price_history' not in st.session_state:
            st.session_state.price_history = []

    def display_header(self):
        """Display the app header and description"""
        st.title("🤖 Crypto AI Assistant")
        st.markdown("""
        Ask me anything about cryptocurrencies! I can:
        - Provide real-time crypto prices
        - Answer questions in multiple languages
        - Explain crypto concepts
        - Track price changes
        """)

    def display_price_chart(self):
        """Display the price chart if we have price history"""
        if st.session_state.price_history:
            # Create price chart
            fig = go.Figure(data=go.Scatter(
                x=[p['time'] for p in st.session_state.price_history],
                y=[p['price'] for p in st.session_state.price_history],
                mode='lines+markers',
                name='BTC Price'
            ))
            
            fig.update_layout(
                title='Bitcoin Price Movement',
                xaxis_title='Time',
                yaxis_title='Price (USD)',
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)

    def update_price_history(self, price):
        """Update the price history with new data"""
        current_time = datetime.now()
        st.session_state.price_history.append({
            'time': current_time,
            'price': price
        })
        
        # Keep only last 24 hours of data
        one_day_ago = current_time - timedelta(days=1)
        st.session_state.price_history = [
            p for p in st.session_state.price_history 
            if p['time'] > one_day_ago
        ]

    def display_message_history(self):
        """Display the conversation history"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def handle_user_input(self):
        """Handle user input and generate response"""
        if prompt := st.chat_input("What would you like to know about crypto?"):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get and display assistant response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                
                try:
                    # Get response from agent
                    response = self.agent.process_message(prompt)
                    
                    # Check if we need to update price history
                    if any(word in prompt.lower() for word in ['price', 'valor', 'precio', 'worth', 'cost']):
                        price_data = self.agent.get_crypto_price("bitcoin")
                        if price_data and 'bitcoin' in price_data:
                            self.update_price_history(price_data['bitcoin']['usd'])
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    message_placeholder.markdown(response)
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    message_placeholder.markdown(error_msg)

    def display_sidebar(self):
        """Display sidebar with additional controls and info"""
        with st.sidebar:
            st.header("Options")
            
            if st.button("Clear Conversation"):
                st.session_state.messages = []
                st.rerun()
            
            st.markdown("---")
            st.markdown("### Example Questions")
            st.markdown("""
            - What's the current Bitcoin price?
            - ¿Cuál es el precio del Bitcoin?
            - Explain blockchain technology
            - How do cryptocurrencies work?
            """)
            
            st.markdown("---")
            st.markdown("### About")
            st.markdown("""
            This AI assistant uses:
            - LLaMA Model for NLP
            - CoinGecko API for prices
            - Multi-language support
            """)

    def run(self):
        """Run the Streamlit app"""
        st.set_page_config(
            page_title="Crypto AI Assistant",
            page_icon="🤖",
            layout="wide"
        )
        
        # Apply custom CSS
        st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .stChat {
            max-width: 800px;
            margin: 0 auto;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display app components
        self.display_header()
        self.display_price_chart()
        self.display_message_history()
        self.handle_user_input()
        self.display_sidebar()

if __name__ == "__main__":
    app = StreamlitCryptoApp()
    app.run()