# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scenedataset']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'decord>=0.6.0',
 'ffmpeg-python>=0.2.0',
 'ffmpeg>=1.4',
 'loguru>=0.6.0',
 'matplotlib>=3.6.3,<4.0.0',
 'opencv-python>=4.7.0.68',
 'scenedetect>=0.6.1',
 'scipy>=1.10.0,<2.0.0',
 'torch-fidelity>=0.3.0,<0.4.0',
 'torch>=1.13.1',
 'torchmetrics[image]>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'scenedataset',
    'version': '0.1.0',
    'description': 'PyTorch dataset which uses PySceneDetect to split videos into scenes',
    'long_description': '# scenedataset\n\nPyTorch dataset which uses PySceneDetect to split videos into scenes\n\n## Installation\n\n```bash\n$ pip install scenedataset\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`scenedataset` was created by Farid Abdalla. It is licensed under the terms of the BSD 3-Clause license.\n\n## Credits\n\n`scenedataset` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Farid Abdalla',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
