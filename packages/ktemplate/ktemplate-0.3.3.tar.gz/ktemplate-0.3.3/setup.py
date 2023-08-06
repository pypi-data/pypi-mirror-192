# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ktemplate']

package_data = \
{'': ['*'], 'ktemplate': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

entry_points = \
{'console_scripts': ['pump = pump:main']}

setup_kwargs = {
    'name': 'ktemplate',
    'version': '0.3.3',
    'description': 'a minimalist python html template lib',
    'long_description': '# kTemplate\n\n[![ci-badge]][ci-url] [![coverage-badge]][coverage-url] [![pypi-badge]][pypi-url] [![py-version]][py-url] [![MIT-badge]][MIT-url] [![black-badge]][black-url]\n\n> a minimalist python html template\n\n🔗 [source code]\n\n## Quick Start\n\n### Installation\n\n`pip install kTemplate`\n\n### Examples\n\n```python\nfrom kTemplate import (\n  div, img, # common html elements\n  element   # for creating custom element\n)\n\n# create common html element\n# `class` represents by `cls` due to python keyword\nhtml_str = div(img(src=\'url\'), cls=\'bar\')\n# <div class="bar"><img src="url"/></div>\n\n# create custom element\nmy_element = element(tag="MyElement", content="foo" props="bar")\n# <MyElement props="ar">foo</MyElement>\n```\n\nPlease refer to the docs for creating HTML [templates and components]\n\n## Documentation\n\nRead the [documentation] for more about:\n\n- usage details\n- function references\n- contributing\n- testing\n- changelog\n\n## Motivation\n\nWhen building web apps with python, no matter using Flask, FastAPI or Django, the go-to template is [Jinja]. This is a sensible choice when building web app. However it\'s a bit over-kill when creating simple website. Also, I am not a fan of Jinja\'s template syntax, eg. putting python loops in html with `{% ... %}` looks clumsy:\n\n```html\n<ul id="navigation">\n{% for item in navigation %}\n    <li><a href="{{ item.href }}">{{ item.caption }}</a></li>\n{% endfor %}\n</ul>\n```\n\nI prefer something like this instead:\n\n```python\nul(\n  id = "navigation",\n  content = [\n    li(\n      a(item.caption, href=item.href)\n    )\n    for item in navigation\n  ]  \n)\n```\n\nIts pure python, having full support of intellisense, type checking, and all language supports from the text editor. I feel much better DX with this approach.\n\nSeparation of concern sounds good, but it comes with a cost: adding another concern 🤪... So separating HTML with python is not always a good choice, especially in simple projects.\n\nMixing template logic within python eliminates the extra layer of complexity, which I think is a reasonable choice for small/medium size projects. There are libraries provide in-python html template, such as [Dominate] and [fast-html].\n\nDominate is a well designed lib and I\'ll certainly go for it for medium sized project. Their `with element_name` pattern is a brilliant use of python context manager, highly recommended 👍. However, for simple project, I\'m still looking for a simpler solution.\n\n`fast-html` come close to what I want. It uses python `generator` as element output to speed up the template concatenation process. This is a efficient technical choice, and I think that\'s why the author name it "fast" html. But still, when dealing with simple or even single page demo sites, pure text elements is what I am looking for instead of generator. Performance hit is negligible in that case.\n\nThat\'s why I create this text centric html template library, and share it on PyPi. I name it "k" template because... just after my initial 😜. Hope u find it useful.\n\n[Jinja]: https://jinja.palletsprojects.com\n[fast-html]: https://pypi.org/project/fast-html\n[Dominate]: https://pypi.org/project/dominate\n\n## Need Help?\n\nOpen a [github issue] or ping me on [Twitter ![twitter-icon]][Twitter]\n\n[github issue]: https://github.com/hoishing/kTemplate/issues\n[Twitter]: https://twitter.com/hoishing\n[twitter-icon]: https://api.iconify.design/logos/twitter.svg?width=20\n[ci-badge]: https://github.com/hoishing/kTemplate/actions/workflows/ci.yml/badge.svg\n[ci-url]: https://github.com/hoishing/kTemplate/actions/workflows/ci.yml\n[coverage-badge]: https://hoishing.github.io/kTemplate/assets/coverage-badge.svg\n[coverage-url]: https://hoishing.github.io/kTemplate/assets/coverage/\n[MIT-badge]: https://img.shields.io/github/license/hoishing/kTemplate\n[MIT-url]: https://opensource.org/licenses/MIT\n[pypi-badge]: https://img.shields.io/pypi/v/ktemplate\n[pypi-url]: https://pypi.org/project/ktemplate/\n[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg\n[black-url]: https://github.com/psf/black\n[py-version]: https://img.shields.io/pypi/pyversions/kTemplate\n[py-url]: https://python.org\n[documentation]: https://hoishing.github.io/kTemplate/\n[templates and components]: https://hoishing.github.io/kTemplate/usage/#templates-and-components\n[source code]: https://github.com/hoishing/kTemplate\n',
    'author': 'Kelvin Ng',
    'author_email': 'hoishing@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://hoishing.github.io/kTemplate',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
