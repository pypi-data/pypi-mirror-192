# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['instainteracts', 'instainteracts.helpers']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=4.8.0,<5.0.0', 'webdriver-manager>=3.8.5,<4.0.0']

setup_kwargs = {
    'name': 'instainteracts',
    'version': '1.0.0',
    'description': 'Instainteracts is an automation tool for Instagram interactions',
    'long_description': "# InstaInteracts\nInstaInteracts is an automation tool for Instagram interactions (follow, like, comment).\n\n## Basic usage\n```py\nfrom instainteracts import InstaInteracts\n\nusername = '' # your username\npassword = '' # your password\nhashtag = 'insta' # hashtag to interact with\n\ninsta = InstaInteracts(username, password)\n\ninsta.comment_by_hashtag(\n    hashtag,\n    ['nice', 'hi'], # List of comments\n    only_recent=True, # Interact only with recent posts\n    limit=10 # limit of comments\n)\n\ninsta.follow_by_hashtag(\n    hashtag,\n    limit=2 # limit of follows\n)\n\ninsta.like_by_hashtag(\n    hashtag,\n    limit=5 # limit of likes\n)\n```",
    'author': 'Manuel',
    'author_email': 'hi@manugmg.anonaddy.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
