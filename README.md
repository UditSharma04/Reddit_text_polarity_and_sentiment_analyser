# 🚀 Social Media Text Analyzer empowered with AI

A Python application that analyzes social media content from Reddit and provides interactive chat capabilities using AI.

## ✨ Features

- Reddit content analysis
  - Sentiment analysis
  - Keyword extraction
  - Topic modeling
  - Entity recognition
  - Readability scoring
- Interactive AI Content Generation
- Data visualization
- Multi-language detection

## 🔧 Prerequisites

- Python 3.12.x (recommended). Note: Python 3.13 is not yet supported by some dependencies (e.g., `gensim`).
- Reddit API credentials
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

## ⚙️ Installation

1. Clone the repository (or open your local folder):
```bash
git clone https://github.com/ShreeshHunnur/SocialMediaTextAnalyzer.git
cd SocialMediaTextAnalyzer
# If your folder name is different, cd into it (e.g., Reddit_analyser)
```

2. Ensure Python 3.12 is available:
```bash
python3.12 --version
```

3. Create and activate a Python 3.12 virtual environment:
```bash
python3.12 -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

4. Upgrade tooling and install dependencies:
```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

5. Download the required spaCy English model:
```bash
python -m spacy download en_core_web_sm
```

6. Create a `.env` file with your API keys:
```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=script:reddit_analyser:1.0 (by u/your_username)
GEMINI_API_KEY=your_gemini_api_key
```

7. Initialize NLTK data (downloads to `nltk_data/` in the project):
```bash
python initialize.py
```

## Usage

1. Activate the virtual environment if not already active:
```bash
source .venv/bin/activate
```

2. Run the main application:
```bash
python main.py
```

3. Enter your search query when prompted
4. View the analysis results
5. Interact with the Gemini AI chatbot
6. Type 'abort' to end the chat session

### Simple UI (Streamlit)

For a non-technical demo UI:

```bash
source .venv/bin/activate
pip install -r requirements.txt  # ensure Streamlit is installed
streamlit run app.py
```

Then open the provided local URL in your browser, enter a topic, and click Analyze.

## 📁 Project Structure

```
Reddit_analyser/
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

## 🛠️ Tips & Troubleshooting

- If installation fails on Python 3.13 (e.g., `gensim` or `scikit-learn` wheels unavailable), switch to Python 3.12:
  - macOS: install via `brew install python@3.12` and use `python3.12`
  - Create venv with `python3.12 -m venv .venv`
- If spaCy errors about missing model, re-run:
  ```bash
  python -m spacy download en_core_web_sm
  ```
- If NLTK complains about missing `stopwords`, re-run:
  ```bash
  python initialize.py
  ```

## 🤝 Contributing

Feel free to fork the project and submit pull requests.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details. 
