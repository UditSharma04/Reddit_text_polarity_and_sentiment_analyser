# Redizer Frontend

Modern, responsive frontend for the Redizer Reddit analysis platform built with Next.js, TypeScript, and Tailwind CSS.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [macOS Setup](#macos-setup)
  - [Windows Setup](#windows-setup)
- [Running the Application](#running-the-application)
- [Building for Production](#building-for-production)
- [Project Structure](#project-structure)
- [Available Scripts](#available-scripts)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Technologies](#technologies)

---

## 🎯 Overview

The frontend provides a beautiful, intuitive interface for Reddit data analysis with:

- **Search Interface**: Customizable search parameters
- **Interactive Charts**: Sentiment, keywords, subreddit activity
- **Visualizations**: Word clouds and temporal trend graphs
- **Data Explorer**: Expandable posts/comments with pagination
- **AI Chat**: Interactive assistant for insights and questions
- **Export Features**: Download data as CSV or JSON

---

## 📦 Prerequisites

### Required Software

- **Node.js**: Version 18.0 or higher
- **npm**: Version 9.0 or higher (comes with Node.js)

### Verify Installation

```bash
node --version    # Should show v18.0.0 or higher
npm --version     # Should show 9.0.0 or higher
```

---

## 🚀 Installation

### macOS Setup

#### 1. Install Node.js

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js
brew install node

# Verify installation
node --version
npm --version
```

**Option B: Using Official Installer**
1. Download the macOS installer from [nodejs.org](https://nodejs.org/)
2. Run the `.pkg` file and follow installation prompts
3. Open Terminal and verify installation

#### 2. Clone and Navigate to Project

```bash
cd /path/to/Redizer/frontend
```

#### 3. Install Dependencies

```bash
npm install
```

This will install all required packages listed in `package.json`.

#### 4. Verify Installation

```bash
npm list --depth=0
```

You should see all dependencies installed without errors.

---

### Windows Setup

#### 1. Install Node.js

**Option A: Using Installer (Recommended)**
1. Download the Windows installer (.msi) from [nodejs.org](https://nodejs.org/)
2. Run the installer
3. Check "Automatically install necessary tools" if prompted
4. Follow the installation wizard
5. Restart your computer

**Option B: Using Chocolatey**
```powershell
# Open PowerShell as Administrator
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Node.js
choco install nodejs

# Verify installation
node --version
npm --version
```

#### 2. Open Command Prompt or PowerShell

```powershell
# Navigate to project directory
cd C:\path\to\Redizer\frontend
```

#### 3. Install Dependencies

```powershell
npm install
```

**Note**: On Windows, you may need to run as Administrator if you encounter permission errors.

#### 4. Verify Installation

```powershell
npm list --depth=0
```

---

## 🎮 Running the Application

### Development Mode

**macOS/Linux:**
```bash
npm run dev
```

**Windows:**
```powershell
npm run dev
```

The application will start on `http://localhost:3000`

### What to Expect

1. Development server starts in seconds
2. Open your browser to `http://localhost:3000`
3. Hot-reload is enabled (changes reflect automatically)
4. Console shows compilation status

### Important Notes

⚠️ **Backend Requirement**: The frontend requires the FastAPI backend to be running on `http://localhost:8000`

To start the backend:
```bash
# In a separate terminal
cd ../Reddit_analyser
python backend.py
```

---

## 🏗️ Building for Production

### Create Production Build

**macOS/Linux:**
```bash
npm run build
```

**Windows:**
```powershell
npm run build
```

This creates an optimized build in the `.next` folder.

### Start Production Server

**macOS/Linux:**
```bash
npm start
```

**Windows:**
```powershell
npm start
```

The production server runs on `http://localhost:3000`

### Production Build Features

- ✅ Optimized for performance
- ✅ Minified JavaScript and CSS
- ✅ Static page generation where possible
- ✅ Image optimization
- ✅ Code splitting

---

## 📁 Project Structure

```
frontend/
├── app/
│   ├── layout.tsx              # Root layout component
│   ├── page.tsx                # Main page (dashboard)
│   ├── globals.css             # Global styles
│   └── favicon.ico             # Site icon
│
├── components/
│   ├── SearchBar.tsx           # Search input and controls
│   ├── MetricsCard.tsx         # Key metrics display
│   ├── SentimentChart.tsx      # Sentiment distribution chart
│   ├── KeywordsChart.tsx       # Top keywords bar chart
│   ├── SubredditChart.tsx      # Subreddit activity chart
│   ├── WordCloudChart.tsx      # Word cloud visualization
│   ├── TemporalGraph.tsx       # Time-based activity graphs
│   ├── RedditPostsView.tsx     # Expandable post/comment view
│   ├── ChatInterface.tsx       # AI chat component
│   └── GeneratedContent.tsx    # AI-generated content display
│
├── lib/
│   └── api.ts                  # API client functions
│
├── public/                     # Static assets
│
├── .eslintrc.json             # ESLint configuration
├── eslint.config.mjs          # ESLint rules
├── next.config.ts             # Next.js configuration
├── package.json               # Dependencies and scripts
├── postcss.config.mjs         # PostCSS configuration
├── tailwind.config.ts         # Tailwind CSS configuration
├── tsconfig.json              # TypeScript configuration
└── README.md                  # This file
```

---

## 📜 Available Scripts

### Development
```bash
npm run dev          # Start development server (port 3000)
npm run build        # Create production build
npm start            # Start production server
```

### Code Quality
```bash
npm run lint         # Run ESLint to check code quality
```

### Cleanup
```bash
# macOS/Linux
rm -rf .next node_modules
npm install

# Windows
rmdir /s /q .next node_modules
npm install
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env.local` file in the `frontend/` directory (optional):

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Development
NODE_ENV=development
```

### Next.js Configuration

Edit `next.config.ts` to customize:
- Redirects and rewrites
- Image domains
- Environment variables
- Build optimizations

### Tailwind Configuration

Edit `tailwind.config.ts` to customize:
- Colors and themes
- Spacing and sizing
- Custom utilities

---

## 🐛 Troubleshooting

### Common Issues

#### Port 3000 Already in Use

**macOS/Linux:**
```bash
# Find process using port 3000
lsof -ti:3000

# Kill the process
kill -9 $(lsof -ti:3000)

# Or use a different port
npm run dev -- -p 3001
```

**Windows:**
```powershell
# Find process using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port
npm run dev -- -p 3001
```

#### Module Not Found Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Build Failures

```bash
# Clear Next.js cache
rm -rf .next

# Rebuild
npm run build
```

#### CORS Errors

Ensure the backend is running and CORS is configured in `Reddit_analyser/backend.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### TypeScript Errors

```bash
# Check TypeScript configuration
npx tsc --noEmit

# Fix auto-fixable issues
npm run lint -- --fix
```

---

## 🔧 Development Tips

### Hot Reload Issues

If hot reload stops working:
```bash
# Restart dev server
# Press Ctrl+C to stop
npm run dev
```

### VSCode Integration

Recommended extensions:
- ESLint
- Tailwind CSS IntelliSense
- TypeScript and JavaScript Language Features
- Prettier - Code formatter

### Browser DevTools

- Open with `F12` or `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Windows)
- Check Console for errors
- Use Network tab to debug API calls
- React DevTools for component inspection

---

## 🛠️ Technologies

### Core Framework
- **Next.js 14**: React framework with server-side rendering
- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript

### Styling
- **Tailwind CSS**: Utility-first CSS framework
- **PostCSS**: CSS transformations

### Data Visualization
- **Chart.js**: Versatile charting library
- **react-chartjs-2**: React wrapper for Chart.js

### UI Components
- **Lucide Icons**: Beautiful icon set
- **Custom Components**: Reusable React components

### HTTP Client
- **Axios**: Promise-based HTTP client

### Development Tools
- **ESLint**: Code linting
- **TypeScript**: Static type checking

---

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

---

## 🆘 Getting Help

If you encounter issues:

1. **Check the browser console** for error messages
2. **Check the terminal** for build/runtime errors
3. **Verify backend is running** on port 8000
4. **Clear cache and rebuild** if errors persist
5. **Review this README** for setup instructions

---

## 📄 License

**Copyright © 2025. All Rights Reserved.**

This is proprietary software. See the main project README for license details.

---

**Happy Coding! 🚀**
