"""
`filtercss` lets you filter unused rules from CSS files, like <https://purgecss.com/> but in Python.
"""
from dataclasses import dataclass
from typing import Union, List

import tinycss2
from bs4 import BeautifulSoup
from tinycss2.ast import QualifiedRule, WhitespaceToken


@dataclass
class Stylesheet:
    contents: List


def parse_css(css: str) -> Stylesheet:
    """
    Parse a string of CSS into a `StyleSheet` object.

    :param css: A CSS string.
    :return: A `Stylesheet` object.
    """

    return Stylesheet(tinycss2.parse_stylesheet(css))


def unparse_css(css: Stylesheet) -> str:
    """
    Unparse (serialize) a `Stylesheet` object into a string.

    :param css: A `Stylesheet` object.
    :return: A CSS string.
    """
    return tinycss2.serialize(css.contents)


def filter_css(css: Union[str, Stylesheet], html: str, soup_features: str = "lxml") -> str:
    """
    Clean up the given CSS to only include rules that affect the given HTML contents.
    If the CSS provided is already a parsed `Stylesheet` the cleaning process will be faster.

    :param css: A CSS string or `Stylesheet` object.
    :param html: A HTML string.
    :param soup_features: A BeautifulSoup4 parser selector (like `lxml`, `html.parser` or `html5lib`).
    :return: A CSS string.
    """
    # Parse the input CSS, or take it as is if already parsed.
    if isinstance(css, Stylesheet):
        original_sheet = css
    else:
        original_sheet = parse_css(css)
    # Prep the output CSS and create our soup.
    contents = []
    soup = BeautifulSoup(html, soup_features)

    cache = {}
    # Go over all of the rules in the original sheet.
    for rule in original_sheet.contents:
        # Include rules that do not have selectors, or that that cssutils doesn't understand.
        if not isinstance(rule, QualifiedRule):
            contents.append(rule)
            continue

        prelude = tinycss2.serialize(rule.prelude)
        if cache.get(prelude, False):
            # We have a selector match, include the rule.
            contents.append(rule)
            continue

        # See if the selector matches anything.
        try:
            matches = soup.select(prelude)
        except:
            # Be conservative and include an element if the soup errors out.
            matches = True

        # Cache whether the selector matched or not, so we save soup lookups.
        cache[prelude] = matches
        if matches:
            # We have a selector match, include the rule.
            # Note that this includes the full rule, even with selectors that did not match.
            contents.append(rule)

    # Filter the rules for now additional whitespace.
    new_rules = []
    was_whitespace = False
    for rule in contents:
        if rule.type == "whitespace":
            if not was_whitespace:
                new_rules.append(rule)
            was_whitespace = True
        else:
            new_rules.append(rule)
            was_whitespace = False

    # Produce the final CSS string output.
    return unparse_css(Stylesheet(new_rules))
