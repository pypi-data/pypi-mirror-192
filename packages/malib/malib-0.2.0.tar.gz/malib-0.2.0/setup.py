# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['malib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'malib',
    'version': '0.2.0',
    'description': '',
    'long_description': '# malib\n\nA few utilities that I find useful.\n\n\n## RateLimiter\n\n```py\nfrom malib import RateLimiter\n\n# call a function at most 10 times per minute\nrl = RateLimiter(max_calls=10, period=60) \n# call .wait() every time before calling the function\nrl.wait()\n```\n\n\n## Exact cover\n\nCode inspired by this [blog post](https://louisabraham.github.io/articles/exact-cover).\n```py\nfrom malib import exact_cover\n\npiece_to_constraints = {"A": {1}, "B": {2, 4}, "C": {2, 3, 5}, "D": {3, 5}}\nnext(exact_cover(piece_to_constraints))\n# ("A", "B", "D")\n```\n\n## Testing\n\n`pytest`\n\n',
    'author': 'Louis Abraham',
    'author_email': 'louis.abraham@yahoo.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
