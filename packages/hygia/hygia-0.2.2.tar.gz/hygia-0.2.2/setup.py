# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dicts',
 'hygia',
 'hygia.data_pipeline',
 'hygia.data_pipeline.annotate_data',
 'hygia.data_pipeline.augment_data',
 'hygia.data_pipeline.feature_engineering',
 'hygia.data_pipeline.model',
 'hygia.data_pipeline.pre_process_data',
 'hygia.parser',
 'hygia.paths',
 'zipcode']

package_data = \
{'': ['*']}

install_requires = \
['altair==4.2.0',
 'attrs==22.2.0',
 'bpemb==0.3.4',
 'certifi==2022.12.7',
 'charset-normalizer==3.0.1',
 'contourpy==1.0.6',
 'coverage==7.0.2',
 'cycler==0.11.0',
 'entrypoints==0.4',
 'exceptiongroup==1.1.0',
 'fonttools==4.38.0',
 'gensim==3.8.3',
 'idna==3.4',
 'importlib-resources==5.10.2',
 'iniconfig==1.1.1',
 'jinja2==3.1.2',
 'joblib==1.2.0',
 'jsonschema==4.17.3',
 'kiwisolver==1.4.4',
 'markupsafe==2.1.1',
 'matplotlib==3.6.2',
 'numpy==1.24.1',
 'packaging==23.0',
 'pandas==1.5.2',
 'pillow==9.4.0',
 'pkgutil-resolve-name==1.3.10',
 'pluggy==1.0.0',
 'pyparsing==3.0.9',
 'pyrsistent==0.19.3',
 'pytest-cov==4.0.0',
 'pytest==7.2.0',
 'python-dateutil==2.8.2',
 'pytz==2022.7',
 'pyyaml==6.0',
 'requests==2.28.2',
 'scikit-learn==1.2.0',
 'scipy==1.9.3',
 'sentencepiece==0.1.97',
 'six==1.16.0',
 'smart-open==6.3.0',
 'threadpoolctl==3.1.0',
 'tomli==2.0.1',
 'toolz==0.12.0',
 'tqdm==4.64.1',
 'urllib3==1.26.14',
 'whatlies==0.7.0',
 'wheel==0.38.4',
 'zipp==3.11.0']

setup_kwargs = {
    'name': 'hygia',
    'version': '0.2.2',
    'description': 'A short description of the package.',
    'long_description': '<p align="center">\n    <img src="./assets/img/horizontal_logo.PNG" alt="hygia-logo" style="width:500px;"/>\n</p>\n\n# A powerful Python ML playground toolkit\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/hygia.svg)](https://pypi.org/project/hygia/)\n[![License](https://img.shields.io/pypi/l/hygia.svg)](https://github.com/hygia-org/hygia/blob/main/LICENSE)\n[![Coverage](https://codecov.io/github/hygia-org/hygia/coverage.svg?branch=main)](https://codecov.io/gh/hygia-org/hygia)\n\n<!-- [![Package Status](https://img.shields.io/pypi/status/hygia.svg)](https://pypi.org/project/hygia/) -->\n\n## What is it?\n\nHygia is a Python package that provides fast, flexible, and expressive data pipeline to make working with Machine Learning data easy and intuitive. The library is designed to make it easy for developers and data scientists to work with a wide range of data sources, perform data preprocessing, feature engineering, and train models with minimal effort.\n\nOne of the key features of Hygia is its support for configuration through YAML files. With the help of a configuration file, users can easily specify the steps they want to run in their data pipeline, including extracting data from various sources, transforming the data, and loading it into the pipeline for processing. This not only makes it easier to automate the pipeline, but also enables users to compare and share their results with others.\n\nIn addition, Hygia is designed to support the ETL (Extract, Transform and Load) process, making it an ideal solution for developers and data scientists looking to scale and automate their workflows. With its fast, flexible, and expressive data pipeline configuration, Hygia makes it easy to organize and manage all your ML model, saving time, effort and allowing you to focus on the most important aspects of your work.\n\n## Main Features\n\n- Configure data pipeline through a YAML file\n- Execute through command line or python import\n- Pack the solution into a Python\'s Package Manager\n- Visualize results in customized dashboards\n- Test on different databases\n\n## Check the documentation\n\nIf you\'re looking to use the Hygia library and get a better understanding of how it works, you can check out the comprehensive documentation available at [Hygia Documentation](https://hygia-org.github.io/hygia/). This website provides a wealth of information on the library\'s capabilities and how to use it.\n\nIn addition to the documentation, we also have a number of boilerplates available at [Examples](https://github.com/hygia-org/hygia/tree/main/examples). These boilerplates provide hands-on examples and practical explanations of using the library and the .yaml file, making it easier for you to get started with using Hygia. Whether you\'re a seasoned data scientist or just starting out, these resources will help you get the most out of the library.\n\n## Where to get it\n\nThe source code is currently hosted on GitHub at: `https://github.com/hygia-org`\n\n## Become a part of our growing community\n\nAre you looking for a way to contribute to an open-source project and make a difference in the field of data science? Then consider joining the Hygia community! Hygia is a powerful and versatile Python library for data pipeline and experimentation, and we\'re always looking for new contributors to help us improve and expand it.\n\nIf you\'re interested in contributing, be sure to check out our community [Contribution Guide](https://github.com/hygia-org/hygia/blob/main/CONTRIBUTING.md) and [Code of Conduct](https://github.com/hygia-org/hygia/blob/main/CODE_OF_CONDUCT.md). These resources will give you an idea of what kind of contributions are welcome, as well as the standards we expect from our contributors.\n\nAnd if you have any questions or want to get started, don\'t hesitate to reach out! You can create an issue on our GitHub repository, or send an email to isaque.alves@ime.usp.br. We\'re always happy to hear from potential contributors, and we\'re looking forward to working with you!\n\n\n\n## Installation from sources\n\nFor experienced users of the library who are already a part of our community, we have put together a comprehensive [Installation Guide](https://github.com/hygia-org/hygia/blob/main/instalation_guide.md) to make the most of the features and functionalities offered by the Hygia library.',
    'author': 'PDA-FGA',
    'author_email': 'rocha.carla@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PDA-FGA/Playground',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
