# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['social_arsenal', 'social_arsenal.files', 'social_arsenal.util']

package_data = \
{'': ['*'], 'social_arsenal': ['sorting_rules/*']}

install_requires = \
['exif>=1.5.0,<2.0.0',
 'filedate>=2.0,<3.0',
 'piexif>=1.1.3,<2.0.0',
 'pillow>=9.4.0,<10.0.0',
 'pyexiftool>=0.5.5,<0.6.0',
 'pypdf>=3.4.1,<4.0.0',
 'pytesseract>=0.3.10,<0.4.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'rich-argparse-plus>=0.3.1.4,<0.4.0.0',
 'rich>=13.0.1,<14.0.0']

entry_points = \
{'console_scripts': ['sort_screenshots = social_arsenal:sort_screenshots']}

setup_kwargs = {
    'name': 'social-arsenal',
    'version': '0.2.3',
    'description': 'Sort screenshots based on rules or through individual review.',
    'long_description': '# Social Arsenal\nSometimes someone is being a clown on the internet. Somewhere on your hard drive is the perfect screenshot to prove to the world that the clown in question is a fool, a hypocrite, a criminal, or worse. But then - horrors - you can\'t find the screenshot! It has been lost in your vast archive of screenshots of clowns clowning themselves on the internet.\n\nSocial Arsenal solves this.\n\n### What It Do\n\nIt sorts screenshots, PDFs, etc. based on their name and/or their textual contents into folders based on a list of rules. The contents of the tweet/reddit post/whatever are prepended to the filename and the `ImageDescription` EXIF tag is set to the OCR text. For example this screenshot of a tweet by a noteworthy cryptocurrency "reporter"[^1] on the eve of FTX\'s implosion:\n\n![](doc/larry_cermak_on_alameda_and_ftx.png)\n\nWould be renamed from `Screen Shot 2023-02-17 at 7.11.37 PM.png` to\n\n```\nTweet by @lawmaster: "I will say though before this thread gets taken over: 1. I do believe Alameda has the size to easily buy Binance\\\'s FIT OTC 2. I think the chance of FTX insolvency is near" Screen Shot 2023-02-17 at 7.11.37 PM.png\n```\n\nOther stuff that happens:\n* Files that match multiple patterns will be copied to multiple destination folders.\n* The `ImageDescription` EXIF tag will be written (for images)\n* All timestamps will be preserved.\n* If the file is not modified or renamed it will merely be moved.\n* If modifications are to be made then the original file will be moved into a `Processed/` directory after it has been handled.\n\nNote that obviously this works on screenshots that are more substantive than just self-clowning screenshots. Note also that videos are not OCRed and can only be moved based on filename matches.\n\n### Quick Start\n```sh\n# Installation with pipx is preferred if you have it but you can also use pip which comes standard\n# on almost all systems. pipx is only a noticeably better answer if you\'re a python programmer who\n# is concerned about side effects of pip upgrading system python packages.\npip install social arsenal\n\n# Get help\nsort_screenshots -h\n\n# Dry run with default cryptocurrency sort rules (dry runs don\'t actually move anything, they just show you what)\nsort_screenshots\n\n# Execute default cryptocurrency sort rules against ~/Pictures/Screenshots\nsort_screenshots --execute\n\n# Sort a different directory of screenshots\nsort_screenshots --screenshots-dir /Users/hrollins/Pictures/get_in_the_van/tourphotos --execute\n\n# Sort with custom rules\nsort_screenshots --rules-csv /Users/hrollins/my_war.csv --execute\n```\n\n# Setup\nIf you want to use the popup window to manually tag you may need to install:\n* Python TK: `brew install python-tk@3.10` (if you don\'t have [homebrew](https://brew.sh/) you need to install it to run `brew install`)\n\nNot required for standard PNG, JPG, etc. images but you may optionally install `exiftool` for other file types.\n* ExifTool: `brew install exiftool` or download from https://exiftool.org\n\n\n# Usage\nHelp screen:\n![](doc/sort_screenshots_help.png)\n\n### Custom Sorting Rules\nThe default is to sort cryptocurrency related content but you can define your own CSV of rules with two columns `folder` and `regex`. The value in `folder` specifies the subdirectory to sort into and `regex` is the pattern to match against. See [the default crypto related configuration](social_arsenal/sorting_rules/crypto.csv) for an example. An explanation of regular expressions is beyond the scope of this README but many resources are available to help. if you\'re not good at regexes just remember that any alphanumeric string is a regex that will match that string. [pythex](http://pythex.org/) is a great website for testing your regexes.\n\n\n[^1]: Perhaps notable that the "reporter" in question for years maintained a private list of the blockchain addresses of Sam Bankman-Fried\'s various scams as part of his commitment to "unrivaled transparency".\n',
    'author': 'Michel de Cryptadamus',
    'author_email': 'michel@cryptadamus.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/michelcrypt4d4mus/screenshot_sorter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
