# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torch_uncertainty',
 'torch_uncertainty.baselines',
 'torch_uncertainty.baselines.batched',
 'torch_uncertainty.baselines.masked',
 'torch_uncertainty.baselines.mimo',
 'torch_uncertainty.baselines.packed',
 'torch_uncertainty.baselines.standard',
 'torch_uncertainty.datamodules',
 'torch_uncertainty.datasets',
 'torch_uncertainty.layers',
 'torch_uncertainty.metrics',
 'torch_uncertainty.models',
 'torch_uncertainty.models.resnet',
 'torch_uncertainty.models.wideresnet',
 'torch_uncertainty.routines',
 'torch_uncertainty.transforms']

package_data = \
{'': ['*']}

install_requires = \
['einops>=0.6.0,<0.7.0',
 'pytorch-lightning>=1.9.0,<2.0.0',
 'scipy>=1.10.0,<2.0.0',
 'tensorboard>=2.11.2,<3.0.0',
 'timm>=0.6.12,<0.7.0',
 'torchinfo>=1.7.1,<2.0.0',
 'torchvision>=0.14.1,<0.15.0']

setup_kwargs = {
    'name': 'torch-uncertainty',
    'version': '0.1.0',
    'description': 'A PyTorch Library for benchmarking and leveraging efficient predictive uncertainty quantification techniques.',
    'long_description': '# Torch Uncertainty\n\n[![tests](https://github.com/ENSTA-U2IS/torch-uncertainty/actions/workflows/run-tests.yml/badge.svg?branch=main&event=push)](https://github.com/ENSTA-U2IS/torch-uncertainty/actions/workflows/run-tests.yml) [![Code Coverage](https://img.shields.io/codecov/c/github/ENSTA-U2IS/torch-uncertainty.svg)](https://codecov.io/gh/ENSTA-U2IS/torch-uncertainty) [![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)\n\n_Torch Uncertainty_ is a package designed to help you leverage uncertainty quantification techniques and make your neural networks more reliable. It is based on PyTorch Lightning to handle multi-GPU training and inference and automatic logging through tensorboard.\n\n---\n\nThis package provides a multi-level API, including:\n- ready-to-train baselines on research datasets, such as CIFAR and ImageNet\n- baselines available for training on your datasets\n- layers available for use in your networks\n\n## Installation\n\nThe package can be installed from PyPI or from source.\n\n### From PyPI (available soon)\n\nInstall the package via pip: `pip install torch-uncertainty`\n\n### From source\n\n#### Installing Poetry\n\nInstallation guidelines for poetry are available on <https://python-poetry.org/docs/>. They boil down to executing the following command:\n\n`curl -sSL https://install.python-poetry.org | python3 -`\n\n#### Installing the package\n\nClone the repository:\n\n`git clone https://github.com/ENSTA-U2IS/torch-uncertainty.git`\n\nCreate a new conda environment and activate it with:\n\n`conda create -n uncertainty && conda activate uncertainty`\n\nInstall the package using poetry:\n\n`poetry install torch-uncertainty` or, for development, `poetry install torch-uncertainty --with dev`\n\nDepending on your system, you may encounter errors. If so, kill the process and add `PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring` at the beginning of every `poetry install` commands.\n\n#### Contributing\n\nIn case that you would like to contribute, install from source and add the pre-commit hooks with `pre-commit install`\n\n## Getting Started and Documentation\n\nPlease find the documentation at [torch-uncertainty.github.io](https://torch-uncertainty.github.io).\n\nA quickstart is available at [torch-uncertainty.github.io/quickstart](https://torch-uncertainty.github.io/quickstart.html).\n\n## Implemented baselines\n\nTo date, the following baselines are implemented:\n\n- Deep Ensembles\n- Masksembles\n- Packed-Ensembles\n\n\n## Awesome Torch repositories\n\nYou may find a lot of information about modern uncertainty estimation techniques on the [Awesome Uncertainty in Deep Learning](https://github.com/ENSTA-U2IS/awesome-uncertainty-deeplearning).\n\n## References\n\n',
    'author': 'ENSTA U2IS',
    'author_email': 'olivier.laurent@ensta-paris.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
