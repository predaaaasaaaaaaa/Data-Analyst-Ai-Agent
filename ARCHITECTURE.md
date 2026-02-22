# Data-Analyst-AI-Agent Architecture

## Project Overview
A local-hosted Telegram bot that analyzes data from images and generates professional Excel reports.

## Core Components

### 1. **Image Processor** (`image_processor.py`)
- Receives image from Telegram
- Extracts tabular data using OCR (Tesseract) or table detection (OpenCV)
- Returns structured data (DataFrame)

### 2. **Data Analyzer** (`data_analyzer.py`)
- Receives DataFrame from image processor
- Performs comprehensive analysis:
  - Descriptive statistics (mean, median, std, quartiles)
  - Data quality checks (missing values, outliers)
  - Correlation analysis
  - Trend detection
  - Anomaly detection
- Returns analysis results (dict/JSON)

### 3. **Excel Generator** (`excel_generator.py`)
- Creates multi-sheet Excel workbook:
  - **Sheet 1:** Original data
  - **Sheet 2:** Summary statistics
  - **Sheet 3:** Correlations & relationships
  - **Sheet 4:** Anomalies & outliers
  - **Sheet 5:** Insights & recommendations
- Includes charts, formatting, professional styling
- Returns file path

### 4. **Telegram Bot** (`telegram_bot.py`)
- Listens for `/start`, `/help`, image uploads
- Manages conversation state
- Coordinates agent components
- Sends analysis status updates
- Uploads Excel file to user

### 5. **Main Agent** (`agent.py`)
- Orchestrates all components
- Error handling & logging
- Manages file cleanup

## Data Flow
```
Image → Extract Data → Analyze → Generate Excel → Send to User
```

## Technology Stack
- **Bot Framework:** python-telegram-bot (async)
- **Data Processing:** pandas, numpy
- **Excel Creation:** openpyxl
- **Image Processing:** OpenCV, Pillow
- **OCR:** pytesseract/EasyOCR
- **Analysis:** scikit-learn (optional)

## Deployment
- Local-hosted (runs on user's machine)
- Async architecture for non-blocking operations
- Telegram polling for simplicity (no webhooks)

