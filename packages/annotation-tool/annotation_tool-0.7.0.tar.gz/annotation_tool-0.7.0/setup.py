# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['annotation_tool',
 'annotation_tool.annotation',
 'annotation_tool.annotation.manual',
 'annotation_tool.annotation.retrieval',
 'annotation_tool.annotation.retrieval.retrieval_backend',
 'annotation_tool.data_model',
 'annotation_tool.dialogs',
 'annotation_tool.file_cache',
 'annotation_tool.media',
 'annotation_tool.media.backend',
 'annotation_tool.media.backend.type_specific_player',
 'annotation_tool.media_reader',
 'annotation_tool.network',
 'annotation_tool.network.LARa',
 'annotation_tool.qt_helper_widgets',
 'annotation_tool.utility']

package_data = \
{'': ['*']}

modules = \
['main']
install_requires = \
['PyOpenGL-accelerate>=3.1.6,<4.0.0',
 'PyOpenGL>=3.1.6,<4.0.0',
 'PyQt6>=6.4.0,<7.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'distinctipy>=1.2.2,<2.0.0',
 'fcache>=0.4.7,<0.5.0',
 'filetype>=1.2.0,<2.0.0',
 'numpy>=1.23.5,<1.24.0',
 'opencv-python>=4.5.3.56,<4.6.0.0',
 'pyqtgraph>=0.12.4,<0.13.0',
 'scipy>=1.10.0,<2.0.0',
 'sortedcontainers>=2.4.0,<3.0.0',
 'torch>=1.12.0,<1.13.0']

entry_points = \
{'console_scripts': ['annotation-tool = main:start']}

setup_kwargs = {
    'name': 'annotation-tool',
    'version': '0.7.0',
    'description': 'Tool for annotating time series data from sources such as IMUs, MoCap, Videos and more.',
    'long_description': '<div align="center">\n\n![PyPI](https://img.shields.io/pypi/v/annotation-tool)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/annotation-tool)\n![PyPI - License](https://img.shields.io/pypi/l/annotation-tool?color=brightgreen)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/annotation-tool)\n\n</div>\n\n# Installation\n\nAll stable versions can be installed from [PyPI] by using [pip] or your favorite package manager\n\n    pip install annotation-tool\n\nYou can get pre-published versions from the [TestPyPI] repository by running\n\n    pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ annotation-tool\n\nAfter installation the annotation tool can be run as simple as\n\n    annotation-tool\n\n# Development\n\n**Requirements:**\n- Python 3.8 or higher\n- [poetry] 1.2 or higher\n- [make]\n\nFor installing the development environment run\n\n```bash\nmake setup\n```\n\nWe are using [commitizen] to automate the version bumping and changelog generation. In order for this to work properly, contributors need to adhere to the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) styling. This will be enforced using [pre-commit] hooks. To easier write commit messages that adhere to this style, we recommend to use `cz commit` (will be installed by [poetry] alongside the other development dependencies). Run `cz example` to see the format of an example commit message.\n\n[commitizen]: https://commitizen-tools.github.io/commitizen/\n[make]: https://www.gnu.org/software/make/\n[pip]: https://pypi.org/project/pip/\n[poetry]: https://python-poetry.org/\n[pre-commit]: https://pre-commit.com/\n[pypi]: https://pypi.org/\n[testpypi]: https://test.pypi.org/project/annotation-tool/\n',
    'author': 'Fernando Moya Rueda',
    'author_email': 'fernando.moya@cs.tu-dortmund.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/wilfer9008/annotation-tool',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
