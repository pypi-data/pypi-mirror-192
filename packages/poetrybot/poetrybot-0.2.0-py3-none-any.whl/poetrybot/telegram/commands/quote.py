import logging
import re

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from poetrybot.database import store
from poetrybot.database.api import get_a_random_poem, is_user_in_allow_list

logger = logging.getLogger(__name__)

QUOTE_REGEX_AUTHOR = re.compile(
    r"""
(?:/quote)                      # /quote
(?:@\w+)?                       # name of the bot
\s+                             # one or more spaces
(?P<author>[A-Za-z\s]+)         # the author
""",
    re.VERBOSE,
)

QUOTE_REGEX_AUTHOR_ABOUT = re.compile(
    r"""
(?:/quote)                      # /quote
(?:@\w+)?                       # name of the bot
\s+                             # one or more spaces
(?P<author>[A-Za-z\s]+)?        # the author (is optional)
(?:about)                       # about
(?P<argument>[A-Za-z\s]+)?      # the argument (is optional)
""",
    re.VERBOSE,
)


async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get a poem."""
    with store.get_session() as s:

        user_id = update.effective_user.id
        if not is_user_in_allow_list(s, user_id=user_id):
            logger.warning(
                "Telegram user with id '{}' and username"
                " '{}' tried to get a quote.".format(
                    user_id, update.effective_user.username
                )
            )
            return

        author, argument = parse_quote(update.message.text)
        poem = get_a_random_poem(s, author=author, argument=argument)

        reply = f"{poem.verses}\n\n_{poem.author.name}_" if poem else "No quote found!"

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply, parse_mode=ParseMode.MARKDOWN
    )


def parse_quote(text: str):
    """Parse text to extract author and argument."""
    author = None
    argument = None

    matched = QUOTE_REGEX_AUTHOR_ABOUT.match(text)
    if not matched:
        matched = QUOTE_REGEX_AUTHOR.match(text)

    if matched:
        try:
            author = matched.group("author").strip()
        except (IndexError, AttributeError):
            pass

        try:
            argument = matched.group("argument").strip()
        except (IndexError, AttributeError):
            pass

    return author, argument
