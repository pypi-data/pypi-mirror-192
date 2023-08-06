# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orkgnlp',
 'orkgnlp.annotation',
 'orkgnlp.annotation.agriner',
 'orkgnlp.annotation.csner',
 'orkgnlp.annotation.tdm',
 'orkgnlp.clustering',
 'orkgnlp.clustering.bioassays',
 'orkgnlp.clustering.predicates',
 'orkgnlp.common',
 'orkgnlp.common.config',
 'orkgnlp.common.service',
 'orkgnlp.common.tools',
 'orkgnlp.common.util',
 'orkgnlp.nli',
 'orkgnlp.nli.templates']

package_data = \
{'': ['*']}

install_requires = \
['huggingface-hub>=0.5.1,<0.6.0',
 'nltk==3.5',
 'numpy==1.21.6',
 'onnx==1.11.0',
 'onnxruntime==1.11.1',
 'overrides>=6.1.0,<7.0.0',
 'pandas==1.3.5',
 'protobuf==3.20.0',
 'sentence-transformers==2.2.2',
 'sentencepiece>=0.1.96,<0.2.0',
 'spacy==3.3.0',
 'torch==1.11.0',
 'transformers==4.19.3',
 'typing-extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['test = tests.unittests:main']}

setup_kwargs = {
    'name': 'orkgnlp',
    'version': '0.9.0',
    'description': 'Python package wrapping the ORKG NLP Services.',
    'long_description': '# ORKG NLP PyPI\n[![Documentation Status](https://readthedocs.org/projects/orkg-nlp-pypi/badge/?version=latest)](https://orkg-nlp-pypi.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/orkgnlp.svg)](https://badge.fury.io/py/orkgnlp)\n[![pipeline status](https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-pypi/badges/main/pipeline.svg)](https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-pypi/-/commits/main)\n\nPyPI package wrapping the ORKG NLP services.\n\nCheck our [Read the Docs](https://orkg-nlp-pypi.readthedocs.io/en/latest/) for more details!\n\nYour [contribution](https://orkg-nlp-pypi.readthedocs.io/en/latest/contribute.html) to `orkgnlp` will always be honored!',
    'author': 'Omar Arab Oghli',
    'author_email': 'omar.araboghli@outlook.com',
    'maintainer': 'Omar Arab Oghli',
    'maintainer_email': 'None',
    'url': 'http://orkg.org/about',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
