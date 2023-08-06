# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['colors', 'colors.palettes']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4,<5',
 'click>=8,<9',
 'lxml>=4,<5',
 'pillow>=9,<10',
 'requests>=2,<3']

entry_points = \
{'console_scripts': ['colors = colors:cli']}

setup_kwargs = {
    'name': 'we-love-colors',
    'version': '2.0.0b0',
    'description': 'PANTONE®, RAL®, Dulux®, Copic® and Prismacolor® color palettes for Scribus, GIMP & Inkscape, the Python way',
    'long_description': "# We love colors!\n[![License](https://badgen.net/badge/license/MIT/blue)](https://codeberg.org/Fundevogel/we-love-colors/src/branch/main/LICENSE) [![PyPI](https://badgen.net/pypi/v/gesetze)](https://pypi.org/project/gesetze) [![Build](https://ci.codeberg.org/api/badges/Fundevogel/we-love-colors/status.svg)](https://codeberg.org/Fundevogel/we-love-colors/issues)\n\nThis library provides an easy way to generate [*color palettes*](https://www.etymonline.com/search?q=Palette):\n\n> In computer graphics, a palette is a finite set of colors.\n> — Wikipedia article '[Palette (Computing)](https://en.wikipedia.org/wiki/Palette_(computing))'\n\n.. often referred to as *Swatches* (as branded by [Adobe Inc.](https://www.adobe.com)):\n\n> *Swatches* are named colors, tints, gradients, and patterns.\n> — [Adobe Illustrator](https://helpx.adobe.com/illustrator/using/using-creating-swatches.html)\n\n.. featuring the following (proprietary) color spaces:\n\n- [PANTONE®](https://www.pantone.com)\n- [RAL®](https://www.ral-farben.de)\n- [Dulux®](https://www.dulux.com.au)\n- [Copic®](https://www.copicmarker.com)\n- [Prismacolor®](https://www.prismacolor.com)\n\nFor now, `we-love-colors` creates master palettes for use in\n\n- [Scribus](https://www.scribus.net) (XML)\n- [GIMP](https://www.gimp.org) and [Inkscape](https://inkscape.org) (GPL)\n- [AutoCAD](https://www.autodesk.com/products/autocad) (ACB)\n- [LibreOffice](https://www.libreoffice.org) (SOC)\n\n\n## Installation\n\nIt's available from [PyPi](https://pypi.org/project/gesetze) using `pip`:\n\n```text\npip install colors\n```\n\n\n## Getting started\n\nUsing this library is straightforward  - otherwise, `--help` is your friend:\n\n```bash\n$ colors fetch --help\nUsage: colors fetch [OPTIONS] [BRANDS]...\n\n  BRANDS: pantone | ral | dulux | copic | prismacolor\n\nOptions:\n  -p, --palette [acb|gpl|soc|xml]  Palette format(s).\n  -v, --version                    Show the version and exit.\n  -h, --help                       Show this message and exit.\n```\n\nUsing its `fetch` command is fairly easy, like that:\n\n```bash\n# Example 1 - Gotta fetch 'em `all`:\n$ colors fetch\n\n# Example 2 - Only specific palettes:\n$ colors fetch copic dulux\n\n# Example 3 - Only GPL files for GIMP:\n$ colors fetch copic dulux -p gpl\n```\n\n## FAQ\n\n**Q: But where do all those files go?**\n**A:** That depends, ..\n- .. `.xml` files may be loaded individually with `Edit - Colours & Fills - Solid Colours - Import` (Scribus)\n- .. `.soc` files belong here:\n  - `~\\AppData\\Roaming\\libreoffice\\3\\user` (Windows + PowerShell, otherwise `%userprofile%`)\n  - `~/Library/Application Support/libreoffice/4/user/config` (Mac)\n  - `~/.config/libreoffice/4/user/config` (Linux)\n- .. installing `.gpl` files boils down to:\n  - moving them to any path specified in `Edit - Preferences - Folders - Palettes` (GIMP)\n  - moving them to `palettes` under directory specified in `Edit - Preferences - System - User Config` (Inkscape)\n- .. installing `.acb` files is [pretty straightforward](https://knowledge.autodesk.com/support/autocad/learn-explore/caas/CloudHelp/cloudhelp/2016/ENU/AutoCAD-Core/files/GUID-17E00AB3-3065-4F1B-A1C3-C4963396D2CB-htm.html)\n\n\n## Color samples\n\nIf you are looking for a quick way to browse PANTONE® colors, check out the [Pantone Finder](https://github.com/picorana/Pantone_finder) package or [visit their website](https://picorana.github.io/Pantone_finder) to get started.\n\nFor all included colors, there are preview files, to be found in the `examples` folder: Open up `index.html`, generated with `examples.py` (for its PHP version, just `php -S localhost:8000`).\n\nWhen clicking a color tile, its hex value is copied to your clipboard - brought to you by [clipboard.js](https://github.com/zenorocha/clipboard.js).\n\n\n## Copyright\n\nWhenever mentioned throughout this project, PANTONE® and related trademarks are the property of [Pantone LLC](https://www.pantone.com), a division of [X-Rite](https://www.xrite.com), a [Danaher](https://www.danaher.com) company.\n\nThe same applies to ..\n- Copic® and related trademarks of [Too Marker Corporation](https://www.toomarker.co.jp/en)\n- Dulux® and related trademarks of [AkzoNobel N.V.](https://www.akzonobel.com) (worldwide) and [DuluxGroup](https://www.dulux.com.au) (Australia & New Zealand)\n- Natural Colour System® and related trademarks of [NCS Colour AB](https://ncscolour.com)\n- Prismacolor® and related trademarks of [Berol Corporation](http://www.berol.co.uk), owned by [Sanford L.P.](http://www.sanfordb2b.com), a [Newell Brands](https://www.newellbrands.com) company.\n- RAL® and related trademarks of [RAL gGmbH](https://www.ral-farben.de) (non-profit LLC) and [RAL Deutsches Institut für Gütesicherung und Kennzeichnung e. V.](https://www.ral.de)\n\nWe assume neither ownership nor intellectual property of any kind - color codes (and names), sRGB and/or hexadecimal values are publically available on the internet.\n\n\n## Similar projects\n\n- For Scribus, there's also the (currently unmaintained) package [`SwatchBooker`](http://www.selapa.net/swatchbooker)\n\n\n**Happy coding!**\n\n\n:copyright: Fundevogel Kinder- und Jugendbuchhandlung\n",
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
