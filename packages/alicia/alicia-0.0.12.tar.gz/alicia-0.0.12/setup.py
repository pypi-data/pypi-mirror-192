# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'dependencies': 'src/dependencies',
 'features': 'src/features',
 'features.comparer': 'src/features/comparer',
 'features.torchvision_downloader': 'src/features/torchvision_downloader',
 'features.trainer': 'src/features/trainer',
 'libs': 'src/libs',
 'models': 'src/modules/models',
 'modules': 'src/modules',
 'modules.models': 'src/modules/models',
 'modules.transforms': 'src/modules/transforms',
 'transforms': 'src/modules/transforms'}

packages = \
['commands',
 'dependencies',
 'features',
 'features.comparer',
 'features.torchvision_downloader',
 'features.trainer',
 'libs',
 'models',
 'modules',
 'modules.models',
 'modules.transforms',
 'transforms']

package_data = \
{'': ['*']}

modules = \
['main']
install_requires = \
['better-abc>=0.0.3,<0.0.4',
 'click>=8.1,<9.0',
 'loading-display>=0.2,<0.3',
 'matplotlib>=3.6,<4.0',
 'numpy>=1.24,<2.0',
 'pillow>=9.4,<10.0',
 'plotext>=5.2,<6.0',
 'termcolor>=2.2,<3.0',
 'torch>=1.13,<2.0',
 'torchvision>=0.14,<0.15',
 'wcmatch>=8.4,<9.0']

entry_points = \
{'console_scripts': ['alicia = main:call']}

setup_kwargs = {
    'name': 'alicia',
    'version': '0.0.12',
    'description': 'A CLI to download, train, test, predict and compare an image classifiers.',
    'long_description': '\n.. image:: https://img.shields.io/pypi/v/alicia.svg\n    :alt: PyPI-Server\n    :target: https://pypi.org/project/alicia/\n\n.. image:: https://pepy.tech/badge/alicia/month\n    :alt: Monthly Downloads\n    :target: https://pepy.tech/project/alicia\n\n\n================================================\n                   AlicIA\n================================================\n::\n\n  Usage: alicia [OPTIONS] COMMAND [ARGS]...\n\n    A CLI to download, train, test, predict and compare an image classifiers.\n\n    Supporting mostly all torch-vision neural networks and datasets.\n\n    This will also identify cute 🐱 or a fierce 🐶, also flowers or what type of\n    🏘️ you should be.\n\n  Options:\n    -v, --verbose\n    -g, --gpu\n    --version      Show the version and exit.\n    --help         Show this message and exit.\n\n  Commands:\n    compare   Compare the info, accuracy, and step speed two (or more by...\n    create    Creates a new model for a given architecture.\n    download  Download a MNIST dataset with PyTorch and split it into...\n    info      Display information about a model architecture.\n    predict   Predict images using a pre trained model, for a given folder...\n    test      Test a pre trained model.\n    train     Train a given architecture with a data directory containing a...\n\n\n.. image:: https://github.com/aemonge/alicia/raw/main/docs/DallE-Alicia-logo.png\n    :alt: DallE-Alicia-logo\n\nInstall and usage\n================================================\n::\n\n    pip install alicia\n    alicia --help\n\n\nIf you just want to see a quick showcase of the tool, download and run [showcase.sh](./showcase.sh)\n\nFeatures\n-----------------------------------------------\n\nTo see the full list of features, and option please refer to `alicia --help`\n\n* Download common torchvision datasets\n* Train, test and predict using different custom-made and torch-vision models.\n* Get information about each model.\n* Compare models training speed, accuracy, and meta information.\n* Tested with MNIST and FashionMNIST.\n* View results in the console, or with matplotlib\n\nReferences\n-----------------------------------------------\n\nUseful links found and used while developing this\n\n* (https://medium.com/analytics-vidhya/creating-a-custom-dataset-and-dataloader-in-pytorch-76f210a1df5d)\n* (https://stackoverflow.com/questions/51911749/what-is-the-difference-between-torch-tensor-and-torch-tensor)\n* (https://deepai.org/dataset/mnist)\n* (https://medium.com/fenwicks/tutorial-1-mnist-the-hello-world-of-deep-learning-abd252c47709)\n',
    'author': 'aemonge',
    'author_email': 'andres@aemonge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/alicia/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
