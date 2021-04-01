from praw.models import Comment
from logging import getLogger
from json import loads as json_load
from os import getenv
from urllib.parse import urlencode, quote

from utils import read_file, fill_template

PY_ENV = getenv("PY_ENV", "development")

logger = getLogger("commands")
floods: dict = json_load(read_file("./floods.json"))
config: dict = json_load(read_file("./config.json"))

# FOR: Scans by iterating whether there is a match with the comment thrown on all key values
# `!flood {flood name}` by default
def flood(comment: Comment, message_to: str) -> None:
    try:
        FLOOD_TEMPLATE = fill_template(
            template=read_file("./template/FLOOD.md"),
            replaced={
                "author": comment.author.name,
                "mark": config["mark"],
                "command-list": config["commands"]["list"],
                "source-code": config["source-code"],
                "add-flood": f"https://www.reddit.com/message/compose?to=u/{message_to}&{urlencode(config['send-message']['add-flood'], quote_via=quote)}",
                "make-suggestion": f"https://www.reddit.com/message/compose?to=u/{message_to}&{urlencode(config['send-message']['make-suggestion'], quote_via=quote)}",
                "report-error": f"https://www.reddit.com/message/compose?to=u/{message_to}&{urlencode(config['send-message']['report-error'], quote_via=quote)}",
                "flood": "{flood}",
            },
        )

        for key, value in floods.items():
            if (
                key.lower().strip() in comment.body
                and f"{config['mark']}{config['commands']['base']}" in comment.body
                and not comment.saved
            ):
                FLOOD_TEMPLATE = fill_template(
                    template=FLOOD_TEMPLATE, replaced={"flood": value.strip()}
                )
                logger.info(
                    f"{comment.body} from u/{comment.author} in r/{comment.subreddit}"
                )
                logger.info(f"Replied to https://reddit.com{comment.permalink}")
                # DEBUG:
                if PY_ENV == "production":
                    comment.reply(FLOOD_TEMPLATE)
                elif PY_ENV == "development":
                    logger.info(FLOOD_TEMPLATE)
    except Exception:
        comment.unsave()
        logger.exception(
            f"Error occurred while replied to https://reddit.com{comment.permalink}"
        )


# FOR: Listing flood `!list` by default
def listing(comment: Comment, message_to: str) -> None:
    try:
        LISTING_TEMPLATE = fill_template(
            template=read_file("./template/LISTING.md"),
            replaced={
                "author": comment.author.name,
                "floods": "\n".join([f"- {key}" for key in list(floods.keys())]),
                "mark": config["mark"],
                "command-base": config["commands"]["base"],
                "source-code": config["source-code"],
                "add-flood": f"https://www.reddit.com/message/compose?to=u/{message_to}&{urlencode(config['send-message']['add-flood'], quote_via=quote)}",
                "make-suggestion": f"https://www.reddit.com/message/compose?to=u/{message_to}&{urlencode(config['send-message']['make-suggestion'], quote_via=quote)}",
                "report-error": f"https://www.reddit.com/message/compose?to=u/{message_to}&{urlencode(config['send-message']['report-error'], quote_via=quote)}",
            },
        )

        if (
            f"{config['mark']}{config['commands']['list']}" in comment.body
            and not comment.saved
        ):
            logger.info(
                f"{comment.body} from u/{comment.author} in r/{comment.subreddit}"
            )
            logger.info(f"Replied to https://reddit.com{comment.permalink}")
            if PY_ENV == "production":
                comment.reply(LISTING_TEMPLATE)
                comment.save()
            elif PY_ENV == "development":
                logger.info(LISTING_TEMPLATE)
    except Exception:
        comment.unsave()
        logger.exception(
            f"Error occurred while replied to https://reddit.com{comment.permalink}"
        )
