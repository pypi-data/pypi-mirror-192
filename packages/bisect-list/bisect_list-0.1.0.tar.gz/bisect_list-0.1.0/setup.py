# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bisect_list']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bisect-list',
    'version': '0.1.0',
    'description': 'Find bad values in a list, logarithmically (FAST)!',
    'long_description': '# bisect-list\n\nFind bad values in a list, logarithmically (FAST!)!\n\n![](animation.gif)\n\n# install\n\n```shell\npoetry add bisect-list\n```\n\n# usage\n\n## bisect_exception(values, func)\n\nLogarithmically removes items that don\'t trigger an exception.\n\nUseful for finding the minimal list of items that triggers an excetpion.\n\n```python\nfrom unittest.mock import MagicMock\n\nfrom bisect_list import bisect_exception\n\ndef error_3705_and_7399(values):\n    if 3705 in values and 7399 in values:\n        raise Exception(f"Never mix 2 with 5!")\n\nmock_func = MagicMock(side_effect=error_3705_and_7399)\n\nvalues = list(range(10_000))\nresult = bisect_exception(values, mock_func)\nassert result == [3705, 7399]\n\nassert mock_func.call_count == 53\n```\n\n---\n\n## bisect_same_exception(values, func)\n\nSame as `bisect_exception`, except makes sure the type of the exception is the same as when calling `func(values)` before starting the bisection.\n\n```python\nfrom bisect_list import bisect_same_exception\n\nclass SpecialException(Exception):\n    pass\n\ndef error_2_and_5(values):\n    if 2 in values and 5 in values:\n        raise SpecialException(f"Never mix 2 with 5!")\n    raise Exception("different exception")\n\nvalues = [1, 2, 3, 4, 5, 6, 7, 8, 9]\nresult = bisect_same_exception(values, error_2_and_5)\nassert result == [2, 5]\n```\n\n---\n\n## biest(values, test)\n\n```python\nfrom bisect_list import bisect\n\nresult = bisect(\n    [1, 2, 3, 4, 5, 6, 7, 8, 9],\n    test=lambda xs: 2 in xs and 8 in xs\n)\nassert result == [2, 8]\n```\n\n# license\n\nMIT\n',
    'author': 'Ryan Munro',
    'author_email': '500774+munro@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
