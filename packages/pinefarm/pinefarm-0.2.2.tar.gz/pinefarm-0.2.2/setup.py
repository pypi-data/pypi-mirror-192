# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pinefarm', 'pinefarm.cli', 'pinefarm.external', 'pinefarm.external.mg5']

package_data = \
{'': ['*'],
 'pinefarm': ['confs/*'],
 'pinefarm.external.mg5': ['cuts_code/*', 'cuts_variables/*', 'patches/*']}

install_requires = \
['PyYAML>=6.0.0,<7.0.0',
 'a3b2bbc3ced97675ac3a71df45f55ba>=6.4.0,<7.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'eko[box]>=0.12.0,<0.13.0',
 'lhapdf-management>=0.2,<0.3',
 'lz4>=4.0.2,<5.0.0',
 'more-itertools>=8.10.0,<9.0.0',
 'pandas>=1.3.0,<2.0.0',
 'pineappl>=0.5.7,<0.6.0',
 'pkgconfig>=1.5.5,<2.0.0',
 'pygit2==1.9.2',
 'requests>=2.26.0,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'tomli>=2.0.1,<3.0.0',
 'yadism[box]>=0.12.3,<0.13.0']

entry_points = \
{'console_scripts': ['pinefarm = pinefarm:command']}

setup_kwargs = {
    'name': 'pinefarm',
    'version': '0.2.2',
    'description': 'Generate PineAPPL grids from PineCards.',
    'long_description': '# Pinefarm\n\nGenerate the corresponding PineAPPL grids.\n\n## Installation\n\nThere is no released version currently.\n\n### Dev\n\nFor development you need the following tools:\n\n- `poetry`, follow [installation\n  instructions](https://python-poetry.org/docs/#installation)\n- `poetry-dynamic-versioning`, used to manage the version (see\n  [repo](https://github.com/mtkennerly/poetry-dynamic-versioning))\n- `pre-commit`, to run maintenance hooks before commits (see\n  [instructions](https://pre-commit.com/#install))\n\nSee [below](.github/CONTRIBUTING.md#non-python-dependencies) for a few more\ndependencies (already available on most systems).\n\n## Documentation\n\nThe documentation is not deployed at the moment.\nIn order to generate it install the project in development, and then do:\n\n```sh\npoetry shell\ncd docs\nmake html\nmake view\n```\n',
    'author': 'Alessandro Candido',
    'author_email': 'candido.ale@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NNPDF/runcards',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
