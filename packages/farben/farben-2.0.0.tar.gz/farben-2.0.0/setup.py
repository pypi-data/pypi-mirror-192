# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['farben', 'farben.palettes']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4,<5',
 'click>=8,<9',
 'lxml>=4,<5',
 'pillow>=9,<10',
 'requests>=2,<3']

entry_points = \
{'console_scripts': ['farben = farben:cli']}

setup_kwargs = {
    'name': 'farben',
    'version': '2.0.0',
    'description': 'PANTONE®, RAL®, Dulux®, Copic®, NCS® and Prismacolor® color palettes for Scribus, GIMP, AutoCAD, Inkscape & LibreOffice',
    'long_description': "# farben\n[![License](https://badgen.net/badge/license/MIT/blue)](https://codeberg.org/Fundevogel/farben/src/branch/main/LICENSE) [![PyPI](https://badgen.net/pypi/v/farben)](https://pypi.org/project/farben) [![Build](https://ci.codeberg.org/api/badges/Fundevogel/farben/status.svg)](https://codeberg.org/Fundevogel/farben/issues)\n\nThis library provides an easy way to generate **color palettes**:\n\n> In computer graphics, a palette is a finite set of colors.\n> — Wikipedia article '[Palette (Computing)](https://en.wikipedia.org/wiki/Palette_(computing))'\n\n.. often referred to as **Swatches** (as branded by [Adobe Inc.](https://www.adobe.com)):\n\n> *Swatches* are named colors, tints, gradients, and patterns.\n> — [Adobe Illustrator](https://helpx.adobe.com/illustrator/using/using-creating-swatches.html)\n\n.. featuring the following (proprietary) color spaces:\n\n- [PANTONE®](https://www.pantone.com)\n- [RAL®](https://www.ral-farben.de)\n- [Dulux®](https://www.dulux.com.au)\n- [Copic®](https://www.copicmarker.com)\n- [NCS®](https://ncscolour.com)\n- [Prismacolor®](https://www.prismacolor.com)\n\nFor now, `farben` creates master palettes for use in\n\n- [Scribus](https://www.scribus.net) (XML)\n- [GIMP](https://www.gimp.org) (GPL)\n- [AutoCAD](https://www.autodesk.com/products/autocad) (ACB)\n- [Inkscape](https://inkscape.org) (GPL)\n- [LibreOffice](https://www.libreoffice.org) (SOC)\n\n\n## Installation\n\nIt's available from [PyPi](https://pypi.org/project/farben):\n\n```bash\n# Using 'pip'\npip install farben\n\n# Using 'poetry'\npoetry add farben\n```\n\n\n## Getting started\n\nUsing this library is straightforward  - otherwise, `--help` is your friend:\n\n```text\n$ farben fetch --help\nUsage: farben [OPTIONS] COMMAND [ARGS]...\n\n  PANTONE®, RAL®, Dulux®, Copic®, NCS® and Prismacolor® color palettes for\n  Scribus, GIMP, AutoCAD, Inkscape & LibreOffice.\n\nOptions:\n  -v, --version  Show the version and exit.\n  -h, --help     Show this message and exit.\n\nCommands:\n  fetch  BRANDS: pantone | ral | dulux | copic | ncs | prismacolor\n```\n\nUsing its `fetch` command is fairly easy, like that:\n\n```bash\n# Example 1\n# - all brands\n# - all palettes\n$ farben fetch\n\n# Example 2\n# - all brands\n# - only specific palette(s)\n$ farben fetch -p gpl\n$ farben fetch -p gpl -p acb\n\n# Example 3\n# - only specific brand(s)\n$ farben fetch copic\n$ farben fetch copic dulux\n```\n\n.. you get the idea!\n\n\n## FAQ\n\n**Q: But where do all those files go?**\n**A:** That depends, ..\n- .. `.xml` files may be loaded individually with `Edit - Colours & Fills - Solid Colours - Import` (Scribus)\n- .. `.soc` files belong here:\n  - `~\\AppData\\Roaming\\libreoffice\\3\\user` (Windows + PowerShell, otherwise `%userprofile%`)\n  - `~/Library/Application Support/libreoffice/4/user/config` (Mac)\n  - `~/.config/libreoffice/4/user/config` (Linux)\n- .. installing `.gpl` files boils down to:\n  - moving them to any path specified in `Edit - Preferences - Folders - Palettes` (GIMP)\n  - moving them to `palettes` under directory specified in `Edit - Preferences - System - User Config` (Inkscape)\n- .. installing `.acb` files is [pretty straightforward](https://knowledge.autodesk.com/support/autocad/learn-explore/caas/CloudHelp/cloudhelp/2016/ENU/AutoCAD-Core/files/GUID-17E00AB3-3065-4F1B-A1C3-C4963396D2CB-htm.html)\n\n\n## Color samples\n\nIf you are looking for a quick way to browse PANTONE® colors, check out the [Pantone Finder](https://github.com/picorana/Pantone_finder) package or [visit their website](https://picorana.github.io/Pantone_finder) to get started.\n\nOnce you retrieved color palettes, you can\n\n- view them using PHP like this: `cd examples/{brand} && php -S localhost:8000`\n- view static HTML page like this: `cd examples && python build.py`\n\nWhen clicking on a color tile, its hex value is copied to your clipboard (powered by [clipboard.js](https://github.com/zenorocha/clipboard.js)).\n\n\n## Copyright\n\nWhenever mentioned throughout this project, PANTONE® and related trademarks are the property of [Pantone LLC](https://www.pantone.com), a division of [X-Rite](https://www.xrite.com), a [Danaher](https://www.danaher.com) company.\n\nThe same applies to ..\n- RAL® and related trademarks of [RAL gGmbH](https://www.ral-farben.de) (non-profit LLC) and [RAL Deutsches Institut für Gütesicherung und Kennzeichnung e. V.](https://www.ral.de)\n- Dulux® and related trademarks of [AkzoNobel N.V.](https://www.akzonobel.com) (worldwide) and [DuluxGroup](https://www.dulux.com.au) (Australia & New Zealand)\n- Copic® and related trademarks of [Too Marker Corporation](https://www.toomarker.co.jp/en)\n- Natural Colour System® and related trademarks of [NCS Colour AB](https://ncscolour.com)\n- Prismacolor® and related trademarks of [Berol Corporation](http://www.berol.co.uk), owned by [Sanford L.P.](http://www.sanfordb2b.com), a [Newell Brands](https://www.newellbrands.com) company.\n\nWe assume neither ownership nor intellectual property of any kind - color codes (and names), sRGB and/or hexadecimal values are publically available on the internet.\n\n\n## Similar projects\n\n- For Scribus, there's also the (currently unmaintained) package [`SwatchBooker`](http://www.selapa.net/swatchbooker)\n\n\n**Happy coding!**\n\n\n:copyright: Fundevogel Kinder- und Jugendbuchhandlung\n",
    'author': 'Fundevogel',
    'author_email': 'maschinenraum@fundevogel.de',
    'maintainer': 'Martin Folkers',
    'maintainer_email': 'hello@twobrain.io',
    'url': 'https://fundevogel.de',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
