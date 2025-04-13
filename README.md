# Social Media Text Analyzer empowered with AI

A Python application that analyzes social media content from Reddit and provides interactive chat capabilities using AI.

## Features

- Reddit content analysis
  - Sentiment analysis
  - Keyword extraction
  - Topic modeling
  - Entity recognition
  - Readability scoring
- Interactive AI Content Generation
- Data visualization
- Multi-language detection

## Prerequisites

- Python 3.8 or higher
- Reddit API credentials
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SocialMediaTextAnalyzer.git
cd SocialMediaTextAnalyzer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file with your API keys:
```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_reddit_user_agent
GEMINI_API_KEY=your_gemini_api_key
```

5. Initialize NLTK data:
```bash
python initialize.py
```

## Usage

1. Run the main application:
```bash
python main.py
```

2. Enter your search query when prompted
3. View the analysis results
4. Interact with the Gemini AI chatbot
5. Type 'abort' to end the chat session

## Project Structure

```
SocialMediaAnalyzer/
├── config/
│   └── config.py
├── src/
│   ├── content_generator.py
│   ├── entity_analysis.py
│   ├── reddit_client.py
│   ├── sentiment_analysis.py
│   ├── text_analysis.py
│   └── visualization.py
├── .env
├── .gitignore
├── initialize.py
├── main.py
└── requirements.txt
```

## Contributing

Feel free to fork the project and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
