# Redizer Backend

FastAPI-based backend for the Redizer Reddit analysis platform, providing powerful APIs for Reddit data extraction, sentiment analysis, and AI-powered insights.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [macOS Setup](#macos-setup)
  - [Windows Setup](#windows-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Technologies](#technologies)

---

## 🎯 Overview

The backend provides RESTful APIs for:

- **Reddit Data Extraction**: Fetch posts and comments using PRAW
- **Sentiment Analysis**: Analyze emotional tone using VADER and TextBlob
- **Text Analysis**: Extract keywords, entities, and patterns
- **Trend Analysis**: Detect temporal patterns and activity trends
- **AI Generation**: Create summaries and insights using GPT
- **Word Cloud Generation**: Create visual representations of text data
- **Interactive Chat**: Conversational AI for data exploration

---

## 📦 Prerequisites

### Required Software

- **Python**: Version 3.8 or higher
- **pip**: Python package manager (comes with Python)

### API Credentials

You'll need:
1. **Reddit API credentials** (client ID, client secret, user agent)
2. **OpenAI API key** (for AI features)

### Verify Installation

```bash
python --version    # Should show 3.8.0 or higher
pip --version       # Should show pip version
```

---

## 🚀 Installation

### macOS Setup

#### 1. Install Python

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Verify installation
python3 --version
pip3 --version
```

**Option B: Using Official Installer**
1. Download the macOS installer from [python.org](https://www.python.org/downloads/)
2. Run the `.pkg` file and follow installation prompts
3. Open Terminal and verify installation

#### 2. Create Virtual Environment (Recommended)

```bash
# Navigate to backend directory
cd /path/to/Redizer/Reddit_analyser

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Your prompt should now show (venv)
```

#### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements_backend.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

#### 4. Verify Installation

```bash
pip list
```

You should see all packages from `requirements_backend.txt` installed.

---

### Windows Setup

#### 1. Install Python

**Option A: Using Official Installer (Recommended)**
1. Download the Windows installer from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ⚠️ **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Restart your computer

**Option B: Using Microsoft Store**
1. Open Microsoft Store
2. Search for "Python 3.11"
3. Click "Get" to install

**Verify Installation:**
```powershell
python --version
pip --version
```

#### 2. Create Virtual Environment (Recommended)

```powershell
# Navigate to backend directory
cd C:\path\to\Redizer\Reddit_analyser

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Your prompt should now show (venv)
```

#### 3. Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements_backend.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

**Note**: If you encounter SSL errors, try:
```powershell
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements_backend.txt
```

#### 4. Verify Installation

```powershell
pip list
```

---

## ⚙️ Configuration

### 1. Get Reddit API Credentials

1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Scroll to "Developed Applications"
3. Click "Create App" or "Create Another App"
4. Fill in:
   - **Name**: Redizer (or any name)
   - **App type**: Select "script"
   - **Description**: Reddit analysis tool (optional)
   - **About URL**: Leave blank or use your URL
   - **Redirect URI**: `http://localhost:8000` (required field)
5. Click "Create app"
6. Note down:
   - **Client ID**: String under "personal use script"
   - **Client Secret**: String next to "secret"

### 2. Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the key (you won't see it again!)

### 3. Configure Credentials

Edit `config/config.py` with your credentials:

```python
import os

# Reddit API Configuration
REDDIT_CLIENT_ID = "your_client_id_here"
REDDIT_CLIENT_SECRET = "your_client_secret_here"
REDDIT_USER_AGENT = "Redizer/1.0 by YourRedditUsername"

# OpenAI Configuration
OPENAI_API_KEY = "sk-your-openai-api-key-here"

# Optional: Reddit Account (for authenticated requests)
REDDIT_USERNAME = "your_reddit_username"  # Optional
REDDIT_PASSWORD = "your_reddit_password"  # Optional
```

**Security Notes:**
- ⚠️ Never commit API keys to version control
- Keep `config/config.py` in `.gitignore`
- Consider using environment variables for production

**Alternative: Environment Variables**

```bash
# macOS/Linux
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_secret"
export OPENAI_API_KEY="your_openai_key"

# Windows PowerShell
$env:REDDIT_CLIENT_ID="your_client_id"
$env:REDDIT_CLIENT_SECRET="your_secret"
$env:OPENAI_API_KEY="your_openai_key"
```

---

## 🎮 Running the Application

### Start the Backend Server

**macOS/Linux:**
```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run the server
python backend.py
```

**Windows:**
```powershell
# Activate virtual environment (if not already active)
.\venv\Scripts\activate

# Run the server
python backend.py
```

### What to Expect

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

The server is now running on `http://localhost:8000`

### Verify Server is Running

Open your browser to:
- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

---

## 📚 API Documentation

### Interactive Documentation

FastAPI provides automatic interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

#### 1. Search Reddit
```
POST /api/search
```
**Body:**
```json
{
  "query": "python programming",
  "limit": 100,
  "subreddit": "python",
  "time_filter": "week"
}
```

#### 2. Analyze Data
```
POST /api/analyze
```
**Body:**
```json
{
  "results": [...],  // Results from /api/search
  "analysis_type": "all_features"
}
```

#### 3. Generate Content
```
POST /api/generate-content
```
**Body:**
```json
{
  "type": "summary",
  "context": {...},
  "prompt": "Summarize key insights"
}
```

#### 4. Chat with AI
```
POST /api/chat
```
**Body:**
```json
{
  "message": "What are the main topics?",
  "context": {...}
}
```

#### 5. Generate Word Cloud
```
POST /api/generate-wordcloud
```
**Body:**
```json
{
  "text": "your text data here"
}
```

### Response Format

All endpoints return JSON:
```json
{
  "success": true,
  "data": {...},
  "error": null
}
```

---

## 📁 Project Structure

```
Reddit_analyser/
├── backend.py                    # Main FastAPI application
├── requirements_backend.txt      # Python dependencies
│
├── config/
│   └── config.py                 # API credentials configuration
│
├── src/
│   ├── reddit_client.py          # Reddit API wrapper (PRAW)
│   ├── sentiment_analysis.py    # Sentiment analysis (VADER, TextBlob)
│   ├── text_analysis.py         # Keyword extraction, text processing
│   ├── trend_analysis.py        # Temporal pattern analysis
│   ├── entity_analysis.py       # Named Entity Recognition (spaCy)
│   ├── content_generator.py     # AI content generation (OpenAI)
│   ├── utils.py                 # Helper functions
│   └── visualization.py         # Data visualization utilities
│
├── nltk_data/                   # NLTK data files (auto-downloaded)
│
└── README.md                    # This file
```

---

## 🐛 Troubleshooting

### Common Issues

#### Port 8000 Already in Use

**macOS/Linux:**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn backend:app --host 0.0.0.0 --port 8001
```

**Windows:**
```powershell
# Find process
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

#### Module Import Errors

```bash
# Ensure you're in the virtual environment
# macOS/Linux
source venv/bin/activate

# Windows
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements_backend.txt
```

#### Reddit API Authentication Errors

**Error**: `401 Unauthorized` or `403 Forbidden`

**Solution**:
1. Verify credentials in `config/config.py`
2. Ensure Reddit app type is "script"
3. Check user agent format: `AppName/Version by RedditUsername`

#### spaCy Model Not Found

```bash
# Download the English language model
python -m spacy download en_core_web_sm

# Verify installation
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Success!')"
```

#### OpenAI API Errors

**Error**: `AuthenticationError` or `RateLimitError`

**Solutions**:
1. Verify API key in `config/config.py`
2. Check API key has sufficient credits
3. Ensure no extra spaces in the API key

#### NLTK Data Not Found

The first run will automatically download required NLTK data. If it fails:

```python
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
```

#### CORS Errors from Frontend

Ensure CORS is configured in `backend.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔧 Development Tips

### Running in Development Mode

```bash
# Auto-reload on code changes
python backend.py
# or
uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

### Testing Endpoints

**Using curl:**
```bash
# Test health check
curl http://localhost:8000/

# Test search (POST)
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"python","limit":10}'
```

**Using HTTPie:**
```bash
# Install httpie
pip install httpie

# Test endpoint
http POST localhost:8000/api/search query="python" limit:=10
```

### Logging

Logs are printed to console. To customize logging:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## 🛠️ Technologies

### Core Framework
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

### Reddit Integration
- **PRAW**: Python Reddit API Wrapper

### Natural Language Processing
- **VADER Sentiment**: Social media sentiment analysis
- **TextBlob**: Text processing and sentiment
- **spaCy**: Advanced NLP and entity recognition
- **NLTK**: Natural language toolkit

### Data Processing
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing

### AI & Generation
- **OpenAI**: GPT for content generation
- **WordCloud**: Word cloud visualization

### Utilities
- **python-dotenv**: Environment variable management
- **Pillow**: Image processing

---

## 📊 Performance Considerations

### Rate Limits

- **Reddit API**: ~60 requests per minute
- **OpenAI API**: Varies by plan and model

### Optimization Tips

1. **Cache results** for frequently accessed data
2. **Limit post counts** for faster analysis (default: 100)
3. **Use batch processing** for large datasets
4. **Monitor API quotas** to avoid rate limits

---

## 🔒 Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** in production
3. **Rotate API keys** regularly
4. **Implement rate limiting** on endpoints
5. **Validate all input data** using Pydantic models
6. **Use HTTPS** in production

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PRAW Documentation](https://praw.readthedocs.io/)
- [spaCy Documentation](https://spacy.io/usage)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [Reddit API Rules](https://github.com/reddit-archive/reddit/wiki/API)

---

## 🆘 Getting Help

If you encounter issues:

1. **Check server logs** in the terminal
2. **Review API documentation** at `/docs`
3. **Verify credentials** in `config/config.py`
4. **Test with small datasets** first
5. **Review this README** for common solutions

---

## 📄 License

**Copyright © 2025. All Rights Reserved.**

This is proprietary software. See the main project README for license details.

---

**Happy Coding! 🚀**
