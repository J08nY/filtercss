# filtercss

**filtercss** lets you filter unused rules from CSS files, like <https://purgecss.com/> but in Python.

## Installation

```shell
pip install filtercss
```

## Example

Filtering is simple, just use `filter_css`.

```python
from filtercss import filter_css

css = """
.test1, .test3 {
    color: red;
}
.test2 {
    color: blue;
}
"""

html = """
<a class="test1 some-other-cls">test</a>
"""

res_css = filter_css(css, html)
assert "test1" in res_css
assert "test2" not in res_css
```

## Limitations

**filtercss** uses [tinycss2](https://doc.courtbouillon.org/tinycss2/stable/). Also **filtercss** will not be able
to anticipate what DOM elements might be inserted by any JavaScript and thus will happily filter out the unused
CSS rules they might want to use. **filtercss** uses BeautifulSoup4 to parse HTML and to detect whether a
CSS selector in a rule matches against a given file. However, BeautifulSoup4 might not support all of the CSS
selectors, in which case **filtercss** is conservative and includes the given CSS rule. **filtercss** is also
not optimal in that it includes a full CSS rule if any of its selectors matches and it does not filter out
unmatched selectors from the rule. Note that this may change in the future.

## License

MIT License