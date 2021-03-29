from praw import Reddit
import logging
import json

bot = Reddit("Bot", config_interpolation="extended")
logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="%(asctime)s, %(levelname)s [%(filename)s:%(lineno)d] %(funcName)s(): %(message)s",
)
logger = logging.getLogger(__name__)
data = json.loads(open("floods.json", "r").read())

for top_level_comment in bot.subreddit("testyapiyorum").stream.comments():
    top_level_comment.body = top_level_comment.body.lower().strip()
    for key, value in data["floods"].items():
        if (
            key.lower().strip() in top_level_comment.body
            and f"{data['config']['mark']}{data['config']['command']}" in top_level_comment.body
            and not top_level_comment.saved
        ):
            try:
                logger.info(
                  f"""{
                    top_level_comment.body
                  } from u/{
                    top_level_comment.author
                  } in r/{
                    top_level_comment.subreddit
                  }\nReplied with: {
                    value.strip()
                  }\n"""
                )
                top_level_comment.reply(f"{value.strip()}\n\n ^()")
                top_level_comment.save()
            except Exception:
                logger.error(f"Reply to {top_level_comment.id} failed")
