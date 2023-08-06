# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['preprocessingtweet']

package_data = \
{'': ['*']}

install_requires = \
['emot>=3.1,<4.0',
 'gensim>=4.3.0,<5.0.0',
 'nltk>=3.8.1,<4.0.0',
 'scipy>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'preprocessingtweet',
    'version': '0.1.4',
    'description': 'Preprocessing tweets prior to NLP pipeline',
    'long_description': '# preprocessingTweet\nPreprocessing tweets prior to use in Transformers\n',
    'author': 'Olivier R. Philippe',
    'author_email': 'olivier.philippe@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
