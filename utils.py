from logging import getLogger
from pathlib import Path
from string import Template

logger = getLogger("utils")

def read_file(path: str) -> str:
    return open(Path(__file__).parent / path, "r").read()

def fill_template(template: str, replaced: dict) -> str:
    if bool(replaced):
        try:
            template = template.format_map(replaced)
        except Exception:
            logger.exception("Error occurred while filling template.")

    else:
        logger.warn(f"replaced should not be empty dictionary.")

    return template