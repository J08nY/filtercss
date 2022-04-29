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

**filtercss** uses [cssutils](https://cssutils.readthedocs.io/en/latest/), which as the project itself states
is not a fully compliant parser with either of the CSS 2.1 or 3 standards. Also **filtercss** will not be able
to anticipate what DOM elements might be inserted by any JavaScript and thus will happily filter out the unused
CSS rules they might want to use. **filtercss** uses BeautifulSoup4 to parse HTML and to detect whether a
CSS selector in a rule matches against a given file. However, BeautifulSoup4 might not support all of the CSS
selectors, in which case **filtercss** is conservative and includes the given CSS rule. **filtercss** is also
not optimal in that it includes a full CSS rule if any of its selectors matches and it does not filter out
unmatched selectors from the rule. Note that this may change in the future.

## Performance

**filtercss** is rather slow, mainly due to how slow the cssutils package is in parsing and serializing CSS
stylesheets. For an idea of the speed, filtering unused rules out of the Bootstrap stylesheet given a simple
HTML page takes ~1 second on a single core (no parallelism in **filtercss**). 

## License

MIT License