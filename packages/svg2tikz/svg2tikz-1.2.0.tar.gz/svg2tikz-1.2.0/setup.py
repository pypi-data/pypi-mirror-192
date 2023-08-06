# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['svg2tikz',
 'svg2tikz.extensions',
 'svg2tikz.inkex',
 'svg2tikz.inkex.elements',
 'svg2tikz.inkex.tester']

package_data = \
{'': ['*']}

install_requires = \
['inkex>=1.2.2+dairiki.1,<2.0.0', 'lxml>=4.9.2,<5.0.0']

setup_kwargs = {
    'name': 'svg2tikz',
    'version': '1.2.0',
    'description': 'Tools for converting SVG graphics to TikZ/PGF code',
    'long_description': '# SVG2TikZ (Inkscape 1.x.x compatible)\n[![Documentation Status](https://readthedocs.org/projects/svg2tikz/badge/?version=latest)](https://svg2tikz.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/svg2tikz.svg)](https://badge.fury.io/py/svg2tikz)\n\nSVG2TikZ, formally known as Inkscape2TikZ ,are a set of tools for converting SVG graphics to TikZ/PGF code.\nThis project is licensed under the GNU GPL  (see  the [LICENSE](/LICENSE) file).\n\n## Documentation and installation\n`SVG2TikZ` is now available on pypi so you can install it with if you want to use it with a command line. But the `inkex` package is not on pypi so you need first to add an extra url to repository:\n\n```\nexport PIP_EXTRA_INDEX_URL=https://gitlab.com/api/v4/projects/40060814/packages/pypi/simple\n```\nThen you can install the package:\n\n```\npip install svg2tikz\n```\nIt is also true if you install the package from this repository.\n\n\nAll the informations to install (as an inkscape extension) and use `SVG2TikZ` can be found in our [Documentation](https://svg2tikz.readthedocs.io/en/latest).\n\n## Changes, Bug fixes and Known Problems from the original\n\n### V1.2.0\n- Adding option to set document unit `input-unit` and the output unit `output-unit`\n- Now the tikz output used the unit define by `output-unit`\n- Now the default behaviour will read the height of the svg and use the bottom left corner as reference\n- This option can be disabled with --noreversey\n\n\n### V1.1.1\n- Supporting svg encoded in utf-8\n- Simple `Symbol` handling\n- Simple Arrow handling\n\n### V1.1\n- Publishing the package to Pypi\n- Publishing the document to ReadTheDocs\n- Fixing the translate error from matrix\n\n### V1.0\n- Now images can also be exported to tikz\n- Added a variable `/def /globalscale` to the output tikz document (standalone and tikz figure)\n- `/globalscale` when changed will scale the tikzfigure by transforming the vector coordinates.\n- `/globalscale` when changed will scale the tikzfigure by scaling the embedded images\n- The path element was not exported in correct coordinates. This is fixed\n- Added an entry to specify the path to be removed from absolute paths in the images. This is useful to work in a latex project directly\n\n## Known Problems\n- Currently only images that are "linked" in svg are exported. Base64 embed is not yet supported so avoid choosing embed option\n- Grouped elements will not work. So ungroup everything\n',
    'author': 'ldevillez',
    'author_email': 'louis.devillez@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
