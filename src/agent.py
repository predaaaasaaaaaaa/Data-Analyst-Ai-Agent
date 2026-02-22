import logging
import asyncio
from pathlib import Path
from typing import Optional
import config
from .telegram_bot import DataAnalystBot

logger = logging.getLogger(__name__)


class DataAnalystAgent:
    """Main agent orchestrator"""
    
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.bot = DataAnalystBot(bot_token)
        self.logger = logger

    async def initialize(self) -> bool:
        """Initialize the agent"""
        try:
            self.logger.info("Initializing Data Analyst Agent...")
            
            if not self.bot_token:
                self.logger.error("Bot token not configured")
                return False
            
            config.DATA_DIR.mkdir(exist_ok=True)
            config.UPLOADS_DIR.mkdir(exist_ok=True)
            config.REPORTS_DIR.mkdir(exist_ok=True)
            
            self.logger.info("Agent initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize agent: {e}", exc_info=True)
            return False

    async def run(self):
        """Run the agent"""
        if not await self.initialize():
            self.logger.error("Initialization failed")
            return
        
        self.logger.info("Starting bot...")
        try:
            await self.bot.run()
        except (KeyboardInterrupt, asyncio.CancelledError):
            self.logger.info("Agent stopped by user")
            self.bot.stop()
        except Exception as e:
            self.logger.error(f"Agent error: {e}", exc_info=True)
            raise


def create_agent(bot_token: str) -> DataAnalystAgent:
    """Create agent instance"""
    return DataAnalystAgent(bot_token)
