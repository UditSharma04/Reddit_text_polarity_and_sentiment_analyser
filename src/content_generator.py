import google.generativeai as genai
import os
from typing import List, Dict
import logging

class ContentGenerator:
    def __init__(self):
        try:
            # Initialize Gemini API
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            genai.configure(api_key=api_key)
            
            # Initialize the model with Gemini 2.0 Flash
            generation_config = {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }
            
            # Initialize the model
            try:
                self.model = genai.GenerativeModel(
                    model_name="gemini-2.0-flash",
                    generation_config=generation_config
                )
                print("Successfully initialized Chatbot model!")
                
                self.chat = self.model.start_chat(history=[])
                print("Chat initialized successfully!")
                
            except Exception as model_error:
                print(f"Error initializing the model: {model_error}")
                raise
            
        except Exception as e:
            print(f"Error initializing the model: {e}")
            logging.error(f"Initialization failed: {str(e)}")
            raise

    def chat_loop(self):
        """Start an interactive chat loop with the user"""
        print("\nWelcome to Content Generator Chatbot!")
        print("Type 'abort' to end the conversation")
        print("-" * 50)

        try:
            while True:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                # Check for abort command
                if user_input.lower() == 'abort':
                    print("\nThank you for chatting! Goodbye!")
                    break
                
                # Generate response
                try:
                    response = self.chat.send_message(
                        user_input,
                        stream=True  # Enable streaming for better user experience
                    )
                    
                    # Print response as it streams
                    print("\nAI: ", end="", flush=True)
                    for chunk in response:
                        print(chunk.text, end="", flush=True)
                    print()  # New line after response
                    
                except Exception as e:
                    print(f"\nError generating response: {e}")
                    print("Please try again with a different question.")

        except KeyboardInterrupt:
            print("\n\nChat interrupted. Goodbye!")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            logging.error(f"Chat error: {str(e)}")

    def generate_content(self, query: str, keywords: List = None, sentiment_data: Dict = None, platform: str = "reddit") -> List[str]:
        """Maintain compatibility with existing interface but redirect to chat loop"""
        print("\nStarting interactive chat mode...")
        self.chat_loop()
        return ["Chat session ended"] 