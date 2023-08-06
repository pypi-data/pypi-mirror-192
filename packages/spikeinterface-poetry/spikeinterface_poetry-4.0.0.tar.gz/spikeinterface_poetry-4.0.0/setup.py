# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spikeinterface_poetry']

package_data = \
{'': ['*']}

install_requires = \
['spikeinterface[full,widgets]>=0.97.0,<0.98.0']

extras_require = \
{'all-sorters': ['PyQt5>=5.15.6,<6.0.0',
                 'tridesclous>=1.6.5,<2.0.0',
                 'loky>=3.0.0,<4.0.0',
                 'spyking-circus>=1.1.0,<2.0.0',
                 'herdingspikes>=0.3.99,<0.4.0',
                 'mountainsort4>=1.0.0,<2.0.0',
                 'Cython',
                 'klusta>=3.0.16,<4.0.0',
                 'klustakwik2>=0.2.7,<0.3.0'],
 'docker': ['docker'],
 'herdingspikes': ['herdingspikes>=0.3.99,<0.4.0'],
 'jupyter': ['jupyter>=1.0.0,<2.0.0'],
 'klusta': ['Cython', 'klusta>=3.0.16,<4.0.0', 'klustakwik2>=0.2.7,<0.3.0'],
 'mountainsort': ['mountainsort4>=1.0.0,<2.0.0'],
 'phy': ['phy'],
 'singularity': ['spython'],
 'spyking-circus': ['PyQt5>=5.15.6,<6.0.0', 'spyking-circus>=1.1.0,<2.0.0'],
 'spython': ['spython'],
 'tridesclous': ['PyQt5>=5.15.6,<6.0.0',
                 'tridesclous>=1.6.5,<2.0.0',
                 'pyopencl>=2022.1,<2023.0',
                 'loky>=3.0.0,<4.0.0']}

setup_kwargs = {
    'name': 'spikeinterface-poetry',
    'version': '4.0.0',
    'description': 'Poetry packaging with extras for working with spikeinterface',
    'long_description': "# The poetry of Spikeinterface\n\nThis package integrates [spikeinterface](https://spikeinterface.readthedocs.io/en/latest/) into poetry packaging to ensure stability.\n\nMy personal experience is that installing `spikeinterface` is smoother this way.\n\n## Installation\n\nRun the following in shell:\n```shell\npip install spikeinterface-poetry\n```\n\nYou can install spikesorters such as `tridesclous`, `spyking-circus`, `herdingspikes`, `klusta`, `mountainsort` easily:\n```shell\npip install spikeinterface-poetry[<spike sorter name>]\n```\nYou can also install `phy`, `docker`, and `spython` (singularity) the same way as above.\n\n## Important remarks\n\nThis package is maintained solely by me, and not the original authors of `spikeinterface`. Please don't make any issues related to the packaging in the `spikeinterface` repository. Should you have any problems running any of the spikesorters, contact the author of that spike sorter.\n\nI also can't and don't guarantee that every component of spikeinterface to work as intended by the original authors. This is the nature of downstream packaging by a 3rd party. This should be less of an issue once poetry has been added to `spikeinterface`.\n",
    'author': 'Can H. Tartanoglu',
    'author_email': 'canhtart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/caniko/spikeinterface_poetry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
