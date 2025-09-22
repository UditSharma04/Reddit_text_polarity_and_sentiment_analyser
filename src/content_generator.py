import os
os.environ.setdefault("GRPC_VERBOSITY", "ERROR")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
try:
    from absl import logging as absl_logging
    absl_logging.set_verbosity(absl_logging.ERROR)
except Exception:
    pass

import google.generativeai as genai
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

        # In-memory analysis context used to ground chat replies
        self.context_text = ""

    def set_context(self, topic: str, keywords: List[str] | None = None, sentiment_data: Dict | None = None, entities: Dict | None = None):
        """Store analysis context to ground future chat replies."""
        try:
            kw = []
            for k in (keywords or []):
                if isinstance(k, (list, tuple)) and len(k) == 2:
                    kw.append(str(k[1]))
                else:
                    kw.append(str(k))
            kw_text = ", ".join(kw[:20])

            sent_text = ""
            if sentiment_data:
                sent_text = (
                    f"Positive {sentiment_data.get('positive', 0):.1f}%, "
                    f"Negative {sentiment_data.get('negative', 0):.1f}%, "
                    f"Neutral {sentiment_data.get('neutral', 0):.1f}%"
                )

            ent_parts = []
            if entities:
                for et, el in entities.items():
                    if el:
                        ent_parts.append(f"{et}: {', '.join(sorted(set(el))[:15])}")
            ent_text = " | ".join(ent_parts)

            self.context_text = (
                "You are assisting with the following analysis context.\n"
                f"Topic: {topic}.\n"
                f"Keywords: {kw_text}.\n"
                + (f"Sentiment: {sent_text}.\n" if sent_text else "")
                + (f"Entities: {ent_text}.\n" if ent_text else "")
                + "Always assume follow-up questions refer to this topic unless the user says otherwise."
            )
        except Exception:
            # Fail closed; empty context
            self.context_text = ""

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
        """Generate a short, engaging post based on analysis (non-interactive)."""
        try:
            keyword_list = []
            if keywords:
                # keywords may be list of tuples (count, word) or strings
                for kw in keywords:
                    if isinstance(kw, (list, tuple)) and len(kw) == 2:
                        keyword_list.append(str(kw[1]))
                    else:
                        keyword_list.append(str(kw))
            keyword_text = ", ".join(keyword_list[:10])

            sentiment_summary = ""
            if sentiment_data and isinstance(sentiment_data, dict):
                sentiment_summary = (
                    f"Positive {sentiment_data.get('positive', 0):.1f}%, "
                    f"Negative {sentiment_data.get('negative', 0):.1f}%, "
                    f"Neutral {sentiment_data.get('neutral', 0):.1f}%"
                )

            prompt_lines = [
                "You are a helpful assistant that writes a concise, engaging social media post.",
                f"Platform: {platform}.",
                f"Topic/query: {query}.",
                f"Important keywords: {keyword_text}.",
            ]
            if sentiment_summary:
                prompt_lines.append(f"Sentiment distribution: {sentiment_summary}.")
            prompt_lines.append(
                "Write 1 short post (2-4 sentences), friendly tone, no hashtags, no emojis."
            )
            prompt = "\n".join(prompt_lines)

            response = self.model.generate_content(prompt)
            text = getattr(response, "text", None)
            if not text and hasattr(response, "candidates") and response.candidates:
                text = response.candidates[0].content.parts[0].text
            return [text or ""]
        except Exception as e:
            logging.error(f"Content generation failed: {e}")
            return [""]

    def chat_reply(self, message: str) -> str:
        """Return a single-turn chat response for UI chat box."""
        try:
            prefixed = (self.context_text + "\n\nUser message: " + message) if self.context_text else message
            response = self.chat.send_message(prefixed)
            if hasattr(response, "text"):
                return response.text
            if hasattr(response, "candidates") and response.candidates:
                return response.candidates[0].content.parts[0].text
            return ""
        except Exception as e:
            logging.error(f"Chat reply failed: {e}")
            return ""