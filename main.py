from praw import Reddit
import logging
import json
from os import getenv


def main():
    bot: Reddit

    LOG_LEVEL = getenv("LOG_LEVEL", "INFO")

    logging.basicConfig(
        level=LOG_LEVEL,
        datefmt="%d/%m/%Y %H:%M:%S",
        format="%(asctime)s, %(levelname)s [%(filename)s:%(lineno)d] %(funcName)s(): %(message)s",
    )
    logger = logging.getLogger(__name__)

    REPLY_MESSAGE = open("REPLY.md", "r").read()

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
        logger.error(
            f"Error occurred while authentication."
        )
        logger.error(err)

    data = json.loads(open("floods.json", "r").read())

    for top_level_comment in bot.subreddit(BOT_ACTIVE_SUBREDDIT).stream.comments():
        top_level_comment.body = top_level_comment.body.lower().strip()
        for key, value in data["floods"].items():
            if (
                key.lower().strip() in top_level_comment.body
                and f"{data['config']['mark']}{data['config']['command']}"
                in top_level_comment.body
                and not top_level_comment.saved
            ):
                try:
                    logger.info(
                        f"{top_level_comment.body} from u/{top_level_comment.author} in r/{top_level_comment.subreddit}"
                    )
                    logger.info(
                        f"Replied to https://reddit.com{top_level_comment.permalink}"
                    )
                    logger.debug(f"\n{value.strip()}")
                    top_level_comment.reply(
                        REPLY_MESSAGE.replace("{author}", top_level_comment.author.name).replace("{flood}", value.strip())
                    )
                    top_level_comment.save()
                except Exception as err:
                    top_level_comment.unsave()
                    logger.error(
                        f"Error occurred while replied to https://reddit.com{top_level_comment.permalink}"
                    )
                    logger.error(err)


if __name__ == "__main__":
    main()
