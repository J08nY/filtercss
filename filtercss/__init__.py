"""
`filtercss` lets you filter unused rules from CSS files, like <https://purgecss.com/> but in Python.
"""

import logging
from typing import Union

import cssutils
from bs4 import BeautifulSoup
from cssutils import CSSParser
from cssutils.css import CSSStyleSheet
from cssutils.serialize import CSSSerializer, Preferences

_min_prefs = Preferences()
_min_prefs.useMinified()
_min_serializer = CSSSerializer(_min_prefs)
_default_prefs = Preferences()
_default_serializer = CSSSerializer(_default_prefs)

# This is bad, but cssutils has very weird global setup like this,
# so no way to get around it.
cssutils.log.setLevel(logging.FATAL)


def parse_css(css: str) -> CSSStyleSheet:
    """
    Parse a string of CSS into a `CSSStyleSheet` object.

    :param css: A CSS string.
    :return: A `CSSStyleSheet` object.
    """
    return CSSParser().parseString(css, validate=False)


def unparse_css(css: CSSStyleSheet, minify: bool) -> str:
    """
    Unparse (serialize) a `CSSStyleSheet` object into a string. If `minify` is
    set, also minifies the output.

    :param css: A `CSSStyleSheet` object.
    :param minify: Whether to minify the output.
    :return: A CSS string.
    """
    # Again the weird cssutils global setup, have to set the global serializer
    # here and remember what it was before to put it back.
    ser = cssutils.ser
    if minify:
        cssutils.setSerializer(_min_serializer)
    else:
        cssutils.setSerializer(_default_serializer)
    result = css.cssText.decode()
    cssutils.setSerializer(ser)

    return result


def filter_css(css: Union[str, CSSStyleSheet], html: str, minify: bool = True) -> str:
    """
    Clean up the given CSS to only include rules that affect the given HTML contents.
    Also minifies the output CSS if `minify` is set. If the CSS provided is already
    a parsed `CSSStyleSheet` the cleaning process will be significantly faster.

    :param css: A CSS string or `CSSStyleSheet` object.
    :param html: A HTML string.
    :param minify: Whether to minify the output.
    :return: A CSS string.
    """
    # Parse the input CSS, or take it as is if already parsed.
    if isinstance(css, CSSStyleSheet):
        original_sheet = css
    else:
        original_sheet = parse_css(css)
    # Prep the output CSS and create our soup.
    new_sheet = CSSStyleSheet(validating=False)
    soup = BeautifulSoup(html, "html")

    cache = {}
    # Go over all of the rules in the original sheet.
    for rule in original_sheet:
        # Include rules that do not have selectors, or that that cssutils doesn't understand.
        if not hasattr(rule, "selectorList"):
            new_sheet.add(rule)
            continue

        # Go over all the selectors, if one matches, add the rule and continue
        for selector in rule.selectorList:
            text = selector.selectorText
            if text in cache:
                if cache[text]:
                    # We have a selector match, include the rule.
                    # Note that this includes the full rule, even with selectors that did not match.
                    new_sheet.add(rule)
                    break
                else:
                    continue

            # See if the selector matches anything.
            try:
                matches = soup.select(text)
            except:
                # Be conservative and include an element if the soup errors out.
                matches = True

            # Cache whether the selector matched or not, so we save soup lookups.
            cache[text] = matches
            if matches:
                # We have a selector match, include the rule.
                # Note that this includes the full rule, even with selectors that did not match.
                new_sheet.add(rule)
                break

    # Produce the final CSS string output.
    return unparse_css(new_sheet, minify)
