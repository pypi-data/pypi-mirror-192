import logging
from typing import Any, Type

import frontmatter
from markdown2 import markdown

from ..base_parsers import BasePageParser


class MarkdownPageParser(BasePageParser):
    @staticmethod
    def markup(content: str, page: "Page") -> str:
        """
        Parses the content with the parser using markdown2. 
        If markdown_extras are defined in the page's `parser_extras`, they will be passed into the parser.
        """
        extras = getattr(page, "parser_extras", {})
        logging.debug(f"Parsing Markdown using extras:", extras)
        markup = markdown(content, extras=extras.get("markdown_extras", []))
        return markup
