# Implementation Specification

## Files to Generate (in order)

### 1. `config.py`
- Bot token from environment or config file
- Logging configuration
- Path settings

### 2. `requirements.txt`
- All dependencies pinned to versions

### 3. `src/image_processor.py`
- `extract_data_from_image(image_path) -> pd.DataFrame`
- Uses pytesseract/EasyOCR for OCR
- Returns structured DataFrame

### 4. `src/data_analyzer.py`
- `analyze_data(df) -> dict`
- Returns: stats, correlations, outliers, trends
- Uses pandas & numpy

### 5. `src/excel_generator.py`
- `generate_report(df, analysis_results, output_path) -> str`
- Multi-sheet Excel with formatting
- Includes charts

### 6. `src/telegram_bot.py`
- Async bot using python-telegram-bot
- Handlers: /start, /help, photo upload
- Coordinates all components

### 7. `src/agent.py`
- Main orchestrator
- Error handling

### 8. `main.py`
- Entry point, starts bot

### 9. `.gitignore` and `README.md`

