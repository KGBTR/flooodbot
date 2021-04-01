from praw import Reddit
import logging
from os import getenv

from commands import listing, flood

def main():
    bot: Reddit

    LOG_LEVEL = getenv("LOG_LEVEL", "INFO")

    logging.basicConfig(
        level=LOG_LEVEL,
        datefmt="%d/%m/%Y %H:%M:%S",
        format="%(asctime)s, %(levelname)s [%(filename)s:%(lineno)d] %(funcName)s(): %(message)s",
    )
    logger = logging.getLogger(__name__)

    try:
        BOT_CLIENT_SECRET = getenv("BOT_CLIENT_SECRET")
        BOT_CLIENT_ID = getenv("BOT_CLIENT_ID")
        BOT_PASSWORD = getenv("BOT_PASSWORD")
        BOT_USERAGENT = getenv("BOT_USERAGENT", "BotName:V1.0 by BotDeveloper")
        BOT_USERNAME = getenv("BOT_USERNAME")

        BOT_ACTIVE_SUBREDDIT = getenv("BOT_ACTIVE_SUBREDDIT", "testyapiyorum")

        if BOT_CLIENT_SECRET and BOT_CLIENT_ID and BOT_PASSWORD and BOT_USERNAME:
            logger.info("Using environment variables")
            bot = Reddit(
                client_id=BOT_CLIENT_ID,
                client_secret=BOT_CLIENT_SECRET,
                password=BOT_PASSWORD,
                user_agent=BOT_USERAGENT,
                username=BOT_USERNAME,
            )
        else:
            logger.info("Using praw.ini")
            bot = Reddit("KGBTRBot", config_interpolation="extended")
        logger.info(f"Logged as u/{bot.user.me()}")
    except Exception as err:
        logger.exception(f"Error occurred while authentication.")

    for comment in bot.subreddit(BOT_ACTIVE_SUBREDDIT).stream.comments():
        comment.body = comment.body.lower().strip()
        if comment.author.name != f"{bot.user.me()}":
            flood(comment=comment, message_to=bot.user.me())
            listing(comment=comment, message_to=bot.user.me())

if __name__ == "__main__":
    main()
