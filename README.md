# 🚀 Enhanced Reddit Analyzer - Research-Grade Social Media Analysis

A powerful Python application that provides **research-grade analysis** of Reddit content with **interactive web interface**, advanced visualizations, and AI-powered insights.

## ✨ Key Features

### 🌐 **Interactive Web Interface**
- **Professional Streamlit dashboard** with tabbed interface
- **Real-time progress indicators** and status updates
- **Auto-generating visualizations** with no page refreshes
- **Immediate CSV/JSON data exports**
- **Interactive charts** with zoom, hover, and filtering

### 📊 **Advanced Analytics**
- **Sentiment analysis** with temporal trends
- **Keyword extraction** with frequency visualization
- **Topic modeling** and trend detection
- **Named entity recognition**
- **Community comparison** across subreddits
- **Engagement metrics** analysis
- **Time-based trend analysis**

### 🔬 **Research-Ready Outputs**
- **High-resolution charts** (300 DPI PNG)
- **Interactive HTML visualizations**
- **Statistical data tables** (CSV, JSON)
- **Publication-ready exports**
- **Comprehensive trend reports**
- **Word clouds** and temporal analysis

## 🔧 Prerequisites

- Python 3.12.x (recommended). Note: Python 3.13 is not yet supported by some dependencies (e.g., `gensim`).
- Reddit API credentials
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

## ⚙️ Quick Setup

### 🚀 **One-Command Setup (Recommended)**

1. **Clone and navigate to the project:**
```bash
git clone <your-repo-url>
cd Reddit_analyser
```

2. **Create and activate Python 3.12 virtual environment:**
```bash
python3.12 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR .venv\Scripts\Activate.ps1  # Windows PowerShell
```

3. **Run the automated setup script:**
```bash
./setup_enhanced.sh
```
*This script automatically installs all dependencies, downloads required models, and verifies the installation.*

4. **Create your `.env` file with API credentials:**
```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=script:reddit_analyser:1.0 (by u/your_username)
GEMINI_API_KEY=your_gemini_api_key
```

### 🔧 **Manual Setup (Alternative)**

If you prefer manual installation:

1. **Ensure Python 3.12 is available:**
```bash
python3.12 --version
```

2. **Install dependencies:**
```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python initialize.py
```

## 🌐 Usage - Interactive Web Interface (Recommended)

### **Start the Enhanced Web Application:**

```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate

# Launch the interactive web interface
./run_streamlit.sh
```

**The app will automatically open in your browser at:** `http://localhost:8501`

### **Using the Web Interface:**

1. **Enter your research topic** (e.g., "climate change", "AI in education", "cryptocurrency")
2. **Select analysis type** from the sidebar:
   - **Basic Analysis** - Quick sentiment and keywords
   - **Advanced Research Analysis** - Full research features
   - **Trend Analysis** - Focus on temporal patterns  
   - **All Features** - Complete analysis suite
3. **Click "Analyze Reddit Data"** and watch the progress bar
4. **Explore results** in organized tabs:
   - **📊 Overview** - Sentiment, keywords, entities
   - **📈 Trends** - Time-based activity analysis
   - **🏘️ Communities** - Subreddit comparison
   - **📋 Data** - Raw data and exports
5. **Download results** instantly (CSV/JSON)
6. **View auto-generated visualizations** in `streamlit_visualizations/` folder

## 💻 Command-Line Interface (Alternative)

For programmatic use or batch processing:

```bash
source .venv/bin/activate
python main.py
```

Follow the prompts to enter your search query and view terminal-based results.

## 📁 Project Structure

```
Reddit_analyser/
├── 🌐 app.py                          # Enhanced Streamlit web interface
├── 💻 main.py                         # Command-line version
├── ⚙️ requirements.txt                # Dependencies
├── 🚀 setup_enhanced.sh               # Automated setup script
├── 🌐 run_streamlit.sh                # Launch web interface
├── 📚 ENHANCED_FEATURES.md            # New features documentation
├── 📖 STREAMLIT_GUIDE.md              # Web interface guide
├── config/
│   └── config.py                      # Application configuration
├── src/                               # 🧠 Core analysis modules
│   ├── reddit_client.py               # Reddit API integration
│   ├── sentiment_analysis.py          # Sentiment classification
│   ├── text_analysis.py               # Text processing & keywords
│   ├── entity_analysis.py             # Named entity recognition
│   ├── advanced_visualization.py      # Research-grade charts
│   ├── trend_analysis.py              # Temporal trend analysis
│   ├── research_export.py             # Publication exports
│   ├── content_generator.py           # AI content generation
│   └── visualization.py               # Basic visualizations
└── streamlit_visualizations/          # 📊 Auto-generated charts
    ├── temporal_trends.png            # Time-based analysis
    ├── subreddit_analysis.png         # Community comparison
    ├── engagement_metrics.png         # User engagement
    ├── wordcloud.png                  # Word frequency
    └── interactive_timeline.html      # Interactive charts
```

## 📊 What You Get

### **🌐 Interactive Web Dashboard**
- **Professional interface** with organized tabs
- **Real-time progress** indicators during analysis
- **Auto-generating charts** with no page refreshes
- **Immediate downloads** (CSV, JSON)
- **Interactive visualizations** with hover details

### **📈 Research-Grade Analytics**
- **Temporal trend analysis** showing when topics were popular
- **Subreddit community comparison** with engagement metrics
- **Sentiment analysis** with time-based patterns
- **Word frequency analysis** with interactive charts
- **Named entity recognition** and topic modeling

### **🔬 Publication-Ready Outputs**
- **High-resolution charts** (300 DPI PNG) for papers
- **Interactive HTML visualizations** for presentations
- **Statistical data tables** with comprehensive metrics
- **CSV/JSON exports** for further analysis
- **Professional formatting** suitable for research

## 🛠️ Troubleshooting

### **Common Issues:**

**🐍 Python Version Issues:**
- Use Python 3.12.x (not 3.13) for best compatibility
- Install via `brew install python@3.12` on macOS

**📦 Dependency Issues:**
```bash
# Re-run the setup script
./setup_enhanced.sh

# Or manually install missing components
python -m spacy download en_core_web_sm
python initialize.py
```

**🌐 Web Interface Issues:**
```bash
# Restart the Streamlit app
./run_streamlit.sh

# Or run directly
streamlit run app.py
```

**🔑 API Issues:**
- Verify your `.env` file has correct Reddit API credentials
- Check your Gemini API key is valid
- Ensure API rate limits aren't exceeded

## 🚀 Quick Start Guide

### **Ready to analyze Reddit data? Follow these steps:**

1. **📥 Setup (One-time):**
```bash
# Clone and navigate to project
cd Reddit_analyser

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Run automated setup
./setup_enhanced.sh
```

2. **🔑 Add your API keys to `.env` file:**
```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret  
REDDIT_USER_AGENT=script:reddit_analyser:1.0 (by u/your_username)
GEMINI_API_KEY=your_gemini_api_key
```

3. **🌐 Launch the web interface:**
```bash
./run_streamlit.sh
```

4. **🎉 Start analyzing!**
   - Open `http://localhost:8501` in your browser
   - Enter any topic (e.g., "climate change", "AI trends")
   - Watch the automated analysis and visualizations
   - Download results and view generated charts

**That's it! Your enhanced Reddit analyzer is ready for research-grade analysis.**

---

## 📚 Additional Resources

- **📖 [Enhanced Features Guide](ENHANCED_FEATURES.md)** - Complete feature overview
- **🌐 [Streamlit Interface Guide](STREAMLIT_GUIDE.md)** - Detailed web interface documentation
- **📁 [Project Structure](PROJECT_STRUCTURE.md)** - Clean codebase organization

## 🤝 Contributing

Feel free to fork the project and submit pull requests.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details. 
