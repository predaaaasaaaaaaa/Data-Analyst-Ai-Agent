# Data Analyst AI Agent

A local-hosted Telegram bot that analyzes data from images and generates professional Excel reports.

## Features

🎯 **Core Capabilities:**
- Extract tabular data from images using OCR
- Comprehensive data analysis (descriptive statistics, correlations, outliers)
- Professional Excel report generation with multiple sheets
- Telegram bot interface for easy access
- Automatic insights and recommendations

📊 **Analysis Includes:**
- Summary statistics (mean, median, std dev, quartiles)
- Data quality assessment (missing values, duplicates)
- Correlation analysis
- Outlier detection (IQR method)
- Trend detection
- Actionable insights

## Architecture

```
src/
├── image_processor.py   - Image to data extraction (OCR)
├── data_analyzer.py     - Statistical analysis engine
├── excel_generator.py   - Multi-sheet Excel report generation
├── telegram_bot.py      - Telegram bot interface
└── agent.py             - Main orchestrator
```

## Setup

### Prerequisites
- Python 3.8+
- Telegram Bot Token (from @BotFather)

### Installation

1. **Clone/Navigate to project:**
   ```bash
   cd ~/python-for-ai/Data-Analyst-Ai-Agent
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure bot token:**
   Option A - Direct in `config.py`:
   ```python
   TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
   ```
   
   Option B - Environment variable:
   ```bash
   export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
   ```

### Optional: Tesseract OCR

For better OCR performance:

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

## Usage

### Run the bot:
```bash
python main.py
```

The bot will:
1. Start polling for messages
2. Wait for users to send photo
3. Extract and analyze data
4. Send Excel report back

### Telegram Bot Commands:
- `/start` - Welcome message
- `/help` - Usage instructions
- Send photo → Automatic analysis

## Data Flow

```
Image Upload (Telegram)
    ↓
Image Processing (OCR extraction)
    ↓
Data Analysis (Statistics, Correlations, Outliers)
    ↓
Excel Report Generation (Multi-sheet with formatting)
    ↓
Send Report to User
```

## Report Contents

The generated Excel file includes:

1. **Raw Data** - Original extracted data with filters
2. **Summary Statistics** - Mean, median, std dev, quartiles, skewness
3. **Data Quality** - Missing values, duplicates, data types
4. **Correlations** - Strong correlations between numeric columns
5. **Outliers** - Detected anomalies using IQR method
6. **Insights** - Actionable recommendations and findings

## Project Structure

```
Data-Analyst-Ai-Agent/
├── main.py                      # Entry point
├── config.py                    # Configuration
├── requirements.txt             # Dependencies
├── ARCHITECTURE.md              # Architecture details
├── SPEC.md                      # Implementation spec
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
├── src/
│   ├── __init__.py
│   ├── agent.py                 # Main agent
│   ├── image_processor.py       # OCR & image processing
│   ├── data_analyzer.py         # Analysis engine
│   ├── excel_generator.py       # Report generation
│   └── telegram_bot.py          # Bot interface
└── data/
    ├── uploads/                 # Uploaded images
    └── reports/                 # Generated reports
```

## Technology Stack

- **Telegram Interface:** python-telegram-bot (async)
- **Data Processing:** pandas, numpy
- **Excel Generation:** openpyxl
- **Image Processing:** OpenCV, Pillow
- **OCR:** EasyOCR, pytesseract
- **Analysis:** scikit-learn

## Configuration

Edit `config.py` to customize:
- Bot token
- Log level
- File size limits
- OCR languages
- Analysis parameters

## Troubleshooting

**Issue: "Bot token not found"**
- Ensure `TELEGRAM_BOT_TOKEN` is set in `config.py` or environment

**Issue: "Could not extract data from image"**
- Make sure image is clear and readable
- Try a screenshot of your data table
- Ensure good lighting if taking photos

**Issue: Slow analysis on large datasets**
- This is normal for datasets with >10k rows
- Consider splitting large files

## Future Enhancements

- [ ] Support for CSV/Excel uploads
- [ ] Custom analysis templates
- [ ] Data visualization in Excel
- [ ] Cloud storage integration
- [ ] Real-time collaboration
- [ ] Advanced ML-based insights

## License

MIT License - Feel free to use and modify

## Author

Built with ❤️ for data analysis automation
