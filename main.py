#!/usr/bin/env python3
"""
Data Analyst AI Agent
Main entry point for the Telegram bot
"""

import asyncio
import logging
import sys

import config
from src.agent import create_agent

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)

logger = logging.getLogger(__name__)


async def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("Starting Data Analyst AI Agent")
    logger.info("=" * 60)

    bot_token = config.TELEGRAM_BOT_TOKEN
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not configured")
        sys.exit(1)

    agent = create_agent(bot_token)

    try:
        await agent.run()
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())