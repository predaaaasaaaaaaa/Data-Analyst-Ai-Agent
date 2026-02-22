import logging
import asyncio
from pathlib import Path
from typing import Optional
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError
import config
from .image_processor import ImageProcessor
from .data_analyzer import DataAnalyzer
from .excel_generator import ExcelReportGenerator

logger = logging.getLogger(__name__)


class DataAnalystBot:
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=token)
        self.image_processor = ImageProcessor()
        self.data_analyzer = DataAnalyzer()
        self.excel_generator = ExcelReportGenerator()
        self.logger = logger

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
👋 Welcome to Data Analyst AI Agent!

I can help you analyze data from images. Just:
1. Take a photo of your data table
2. Send it to me
3. I'll analyze it and send you a detailed Excel report

📊 What I can do:
• Extract data from images (tables, charts)
• Calculate statistics (mean, median, std dev, etc.)
• Detect outliers and anomalies
• Analyze correlations
• Generate professional Excel reports
• Provide actionable insights

Use /help for more information.
        """
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📖 How to use:

1. Send me a photo of data (table, screenshot, chart)
2. I'll extract and analyze the data
3. You'll receive a detailed Excel report with:
   • Raw data
   • Summary statistics
   • Data quality report
   • Correlation analysis
   • Outlier detection
   • Insights & recommendations

🎯 Supported formats:
• JPG, PNG, GIF
• Tables in images
• Screenshots of spreadsheets

⚠️ Tips:
• Make sure the image is clear and readable
• Tables with headers work best
• File size limit: 25MB

Any questions? Just send me an image to get started!
        """
        await update.message.reply_text(help_text)

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle photo uploads"""
        try:
            # Check user authorization (optional)
            if config.TELEGRAM_USER_ID and str(update.effective_user.id) != config.TELEGRAM_USER_ID:
                await update.message.reply_text("❌ Unauthorized access")
                return

            # Send processing message
            processing_msg = await update.message.reply_text("🔄 Processing image... This may take a moment.")
            
            # Download photo
            file = await context.bot.get_file(update.message.photo[-1].file_id)
            
            # Save to uploads directory
            image_path = config.UPLOADS_DIR / f"{update.message.photo[-1].file_id}.jpg"
            await file.download_to_drive(image_path)
            
            self.logger.info(f"Processing image from user {update.effective_user.id}")
            
            # Extract data
            await processing_msg.edit_text("📸 Extracting data from image...")
            df = self.image_processor.extract_data_from_image(str(image_path))
            
            if df is None or len(df) == 0:
                await processing_msg.edit_text(
                    "❌ Could not extract data from image. Make sure it contains a readable table."
                )
                return
            
            # Analyze data
            await processing_msg.edit_text("📊 Analyzing data...")
            analysis = self.data_analyzer.analyze_data(df)
            
            if 'error' in analysis:
                await processing_msg.edit_text(f"❌ Analysis failed: {analysis['error']}")
                return
            
            # Generate Excel
            await processing_msg.edit_text("📝 Generating Excel report...")
            report_filename = f"analysis_{update.message.photo[-1].file_id}.xlsx"
            report_path = config.REPORTS_DIR / report_filename
            
            excel_path = self.excel_generator.generate_report(df, analysis, str(report_path))
            
            if not excel_path or not Path(excel_path).exists():
                await processing_msg.edit_text("❌ Failed to generate Excel report")
                return
            
            # Send report
            await processing_msg.edit_text("📤 Sending report...")
            
            with open(excel_path, 'rb') as f:
                await update.message.reply_document(
                    document=f,
                    filename=report_filename,
                    caption=f"""
✅ Analysis Complete!

📊 Data Summary:
• Rows: {df.shape[0]}
• Columns: {df.shape[1]}

📈 Key Findings:
"""
                )
            
            # Add insights
            insights_text = "\n".join([f"• {insight}" for insight in analysis.get('insights', {}).get('insights', [])])
            await update.message.reply_text(f"💡 Insights:\n{insights_text}")
            
            await processing_msg.delete()
            self.logger.info(f"Successfully processed image for user {update.effective_user.id}")
            
        except TelegramError as e:
            self.logger.error(f"Telegram error: {e}")
            await update.message.reply_text(f"❌ Telegram error: {e}")
        except Exception as e:
            self.logger.error(f"Error processing photo: {e}", exc_info=True)
            await update.message.reply_text(f"❌ Error processing image: {str(e)}")

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        await update.message.reply_text(
            "👋 I work with images! Please send me a photo of data to analyze.\n\nUse /help for more info."
        )

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        self.logger.error(f"Update {update} caused error: {context.error}", exc_info=context.error)

    def get_application(self) -> Application:
        """Create and configure the bot application"""
        app = Application.builder().token(self.token).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        
        # Error handler
        app.add_error_handler(self.error_handler)
        
        return app

    async def run(self):
        """Run the bot"""
        app = self.get_application()
        self.logger.info("Starting Data Analyst Bot...")
        await app.run_polling()


async def start_bot(token: str):
    """Start the bot"""
    bot = DataAnalystBot(token)
    await bot.run()
