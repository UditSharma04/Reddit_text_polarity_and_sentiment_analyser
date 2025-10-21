# Redizer - Reddit Data Analysis Platform

![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-red)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

A powerful, modern web application for analyzing Reddit discussions with advanced AI-powered insights, sentiment analysis, and beautiful visualizations.

---

## 📋 Table of Contents

- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Screenshots](#screenshots)
- [License](#license)

---

## 🎯 Problem Statement

Reddit is a goldmine of user-generated content, opinions, and discussions across countless topics. However, extracting meaningful insights from Reddit data presents several challenges:

1. **Information Overload**: Thousands of posts and comments make manual analysis impractical
2. **Sentiment Understanding**: Difficulty in gauging overall sentiment and emotional tone
3. **Trend Identification**: Hard to spot temporal patterns and trending topics
4. **Content Summarization**: Time-consuming to distill key insights from lengthy discussions
5. **Data Visualization**: Lack of intuitive tools to visualize Reddit data effectively
6. **Research Needs**: Researchers and marketers need structured ways to analyze Reddit conversations

Traditional Reddit browsing and basic search features don't provide the analytical depth needed for research, market analysis, or content strategy.

---

## 💡 Solution

**Redizer** is a full-stack web application that transforms Reddit data into actionable insights through:

### Core Capabilities

- **🔍 Advanced Search**: Query Reddit with customizable parameters (subreddits, time ranges, post limits)
- **😊 Sentiment Analysis**: AI-powered sentiment detection (positive, negative, neutral) for posts and comments
- **📊 Visual Analytics**: Interactive charts for sentiment distribution, keyword frequency, and subreddit activity
- **☁️ Word Cloud Generation**: Beautiful word clouds highlighting key terms and topics
- **📈 Temporal Analysis**: Time-based patterns showing activity by hour and day
- **🤖 AI-Powered Insights**: GPT-generated summaries and content recommendations
- **💬 Interactive Chat**: Ask questions and refine analysis through an AI assistant
- **📤 Data Export**: Download results in CSV or JSON format for further analysis
- **🎨 Modern UI/UX**: Clean, responsive interface with smooth loading states and intuitive navigation

### Key Differentiators

1. **Real-Time Analysis**: Process and analyze Reddit data on-demand
2. **Multi-Level Analysis**: Choose between basic sentiment analysis or comprehensive analysis with all features
3. **Expandable Post View**: Navigate posts and comments hierarchically with pagination
4. **Export Capabilities**: Take your data and insights with you
5. **AI Enhancement**: Leverage GPT for content generation and conversational insights

---

## ✨ Features

### Analysis Features
- ✅ Reddit post and comment extraction via PRAW
- ✅ Sentiment analysis using VADER and TextBlob
- ✅ Named Entity Recognition (NER) with spaCy
- ✅ Keyword extraction and frequency analysis
- ✅ Temporal pattern detection (hourly/daily activity)
- ✅ Subreddit activity comparison
- ✅ AI-generated summaries and insights

### Visualization Features
- ✅ Sentiment distribution (doughnut charts)
- ✅ Top keywords (bar charts)
- ✅ Subreddit activity (bar charts)
- ✅ Word cloud generation (Python-based)
- ✅ Temporal activity graphs (line charts)
- ✅ Interactive timeline views

### User Experience Features
- ✅ Clean, modern UI with indigo color scheme
- ✅ Tabbed interface (Overview, Visualizations, Data, Chat)
- ✅ Loading states with progress messages
- ✅ Expandable post/comment view
- ✅ Pagination for large datasets (10 posts per page)
- ✅ Copy-to-clipboard functionality
- ✅ Export to CSV/JSON
- ✅ Responsive design for all screen sizes

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Search    │  │ Analytics  │  │   Chat     │            │
│  │    UI      │  │   Charts   │  │ Interface  │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│         │                │                │                  │
│         └────────────────┴────────────────┘                  │
│                          │                                   │
│                    API Client (Axios)                        │
└──────────────────────────┼──────────────────────────────────┘
                           │ HTTP/REST
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                          ▼                                   │
│                  FastAPI Backend                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  API Endpoints (/search, /analyze, /chat, etc.)     │    │
│  └─────────────────────────────────────────────────────┘    │
│         │              │              │              │       │
│  ┌──────▼─────┐ ┌─────▼──────┐ ┌────▼─────┐ ┌──────▼────┐ │
│  │   Reddit   │ │ Sentiment  │ │  Trend   │ │   GPT     │ │
│  │   Client   │ │  Analysis  │ │ Analysis │ │ Generator │ │
│  │   (PRAW)   │ │  (VADER)   │ │ (pandas) │ │ (OpenAI)  │ │
│  └────────────┘ └────────────┘ └──────────┘ └───────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Frontend:**
- Next.js 14 (React framework)
- TypeScript (type safety)
- Tailwind CSS (styling)
- Chart.js (visualizations)
- Lucide Icons (UI icons)
- Axios (API requests)

**Backend:**
- FastAPI (Python web framework)
- PRAW (Reddit API wrapper)
- VADER & TextBlob (sentiment analysis)
- spaCy (NLP and entity recognition)
- pandas (data processing)
- OpenAI GPT (AI generation)
- WordCloud (visualization)

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.8+ and pip
- **Reddit API credentials** (client ID, client secret, user agent)
- **OpenAI API key** (for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Redizer
   ```

2. **Set up Backend**
   ```bash
   cd Reddit_analyser
   
   # Install Python dependencies
   pip install -r requirements_backend.txt
   
   # Configure credentials (see Reddit_analyser/README.md)
   # Edit config/config.py with your API keys
   ```

3. **Set up Frontend**
   ```bash
   cd ../frontend
   
   # Install Node dependencies
   npm install
   ```

4. **Start the Application**

   **Terminal 1 - Backend:**
   ```bash
   cd Reddit_analyser
   python backend.py
   # Backend runs on http://localhost:8000
   ```

   **Terminal 2 - Frontend:**
   ```bash
   cd frontend
   npm run dev
   # Frontend runs on http://localhost:3000
   ```

5. **Access the Application**
   
   Open your browser to `http://localhost:3000`

For detailed setup instructions, see:
- [Backend Setup Guide](Reddit_analyser/README.md)
- [Frontend Setup Guide](frontend/README.md)

---

## 📁 Project Structure

```
Redizer/
├── README.md                          # This file
├── Reddit_analyser/                   # Backend (FastAPI + Python)
│   ├── backend.py                     # Main FastAPI application
│   ├── requirements_backend.txt       # Python dependencies
│   ├── config/
│   │   └── config.py                  # API credentials configuration
│   ├── src/
│   │   ├── reddit_client.py          # Reddit API interaction
│   │   ├── sentiment_analysis.py     # Sentiment processing
│   │   ├── text_analysis.py          # Text and keyword analysis
│   │   ├── trend_analysis.py         # Temporal pattern analysis
│   │   ├── entity_analysis.py        # Named entity recognition
│   │   ├── content_generator.py      # AI content generation
│   │   └── utils.py                  # Helper functions
│   └── README.md                      # Backend documentation
│
└── frontend/                          # Frontend (Next.js + TypeScript)
    ├── app/
    │   ├── page.tsx                   # Main application page
    │   ├── layout.tsx                 # Root layout
    │   └── globals.css                # Global styles
    ├── components/
    │   ├── SearchBar.tsx              # Search input component
    │   ├── MetricsCard.tsx            # Metrics display
    │   ├── SentimentChart.tsx         # Sentiment visualization
    │   ├── KeywordsChart.tsx          # Keywords visualization
    │   ├── SubredditChart.tsx         # Subreddit activity chart
    │   ├── WordCloudChart.tsx         # Word cloud display
    │   ├── TemporalGraph.tsx          # Temporal trends chart
    │   ├── RedditPostsView.tsx        # Expandable post/comment view
    │   ├── ChatInterface.tsx          # AI chat interface
    │   └── GeneratedContent.tsx       # AI-generated content display
    ├── lib/
    │   └── api.ts                     # API client functions
    ├── package.json                   # Node dependencies
    └── README.md                      # Frontend documentation
```

---

## 🛠️ Technologies Used

### Frontend
- [Next.js 14](https://nextjs.org/) - React framework
- [TypeScript](https://www.typescriptlang.org/) - Type-safe JavaScript
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Chart.js](https://www.chartjs.org/) - Data visualization
- [React Chart.js 2](https://react-chartjs-2.js.org/) - React wrapper
- [Lucide Icons](https://lucide.dev/) - Icon library
- [Axios](https://axios-http.com/) - HTTP client

### Backend
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [PRAW](https://praw.readthedocs.io/) - Python Reddit API Wrapper
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment) - Sentiment analysis
- [TextBlob](https://textblob.readthedocs.io/) - Text processing
- [spaCy](https://spacy.io/) - NLP library
- [pandas](https://pandas.pydata.org/) - Data manipulation
- [OpenAI](https://openai.com/) - GPT integration
- [WordCloud](https://github.com/amueller/word_cloud) - Word cloud generation
- [Uvicorn](https://www.uvicorn.org/) - ASGI server

---

## 📸 Screenshots

### Main Dashboard
The main interface with search, sentiment analysis, and key metrics.

### Visualizations Tab
Word cloud and temporal activity graphs showing trends over time.

### Data Explorer
Expandable post view with pagination for easy navigation through results.

### AI Chat Assistant
Interactive chat interface for asking questions and refining analysis.

---

## 📄 License

**Copyright © 2025. All Rights Reserved.**

This software and associated documentation files (the "Software") are proprietary and confidential. Unauthorized copying, modification, distribution, or use of this Software, via any medium, is strictly prohibited without explicit written permission from the owner.

For licensing inquiries, please contact: [Your Contact Information]

---

## 🤝 Contributing

This is a proprietary project. Contributions are not accepted at this time.

---

## 📧 Contact & Support

For questions, issues, or feature requests, please contact:
- **Email**: [Your Email]
- **GitHub**: [Your GitHub Profile]

---

## 🙏 Acknowledgments

- Reddit API for providing access to discussion data
- OpenAI for GPT capabilities
- The open-source community for amazing libraries and tools

---

**Built with ❤️ using Next.js and FastAPI**

