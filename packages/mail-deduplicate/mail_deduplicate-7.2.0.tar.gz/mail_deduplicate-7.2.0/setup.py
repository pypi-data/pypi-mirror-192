# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mail_deduplicate', 'mail_deduplicate.tests']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.3,<2.0.0',
 'boltons>=21.0.0,<22.0.0',
 'click-extra>=3.4.0,<4.0.0',
 'click>=8.1.2,<9.0.0',
 'tabulate[widechars]>=0.9.0,<0.10.0']

extras_require = \
{':python_version < "3.10"': ['typing-extensions>=4.3.0,<5.0.0']}

entry_points = \
{'console_scripts': ['mdedup = mail_deduplicate.__main__:main']}

setup_kwargs = {
    'name': 'mail-deduplicate',
    'version': '7.2.0',
    'description': '📧 CLI to deduplicate mails from mail boxes.',
    'long_description': '<p align="center">\n  <a href="https://github.com/kdeldycke/mail-deduplicate/">\n    <img src="https://raw.githubusercontent.com/kdeldycke/mail-deduplicate/main/docs/images/mail-deduplicate-logo-header.png" alt="Mail Deduplicate">\n  </a>\n</p>\n\n[![Last release](https://img.shields.io/pypi/v/mail-deduplicate.svg)](https://pypi.python.org/pypi/mail-deduplicate)\n[![Python versions](https://img.shields.io/pypi/pyversions/mail-deduplicate.svg)](https://pypi.python.org/pypi/mail-deduplicate)\n[![Unittests status](https://github.com/kdeldycke/mail-deduplicate/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/kdeldycke/mail-deduplicate/actions/workflows/tests.yaml?query=branch%3Amain)\n[![Documentation status](https://github.com/kdeldycke/mail-deduplicate/actions/workflows/docs.yaml/badge.svg?branch=main)](https://github.com/kdeldycke/mail-deduplicate/actions/workflows/docs.yaml?query=branch%3Amain)\n[![Coverage status](https://codecov.io/gh/kdeldycke/mail-deduplicate/branch/main/graph/badge.svg)](https://codecov.io/gh/kdeldycke/mail-deduplicate/branch/main)\n[![DOI](https://zenodo.org/badge/9016537.svg)](https://zenodo.org/badge/latestdoi/9016537)\n\n**What is Mail Deduplicate?**\n\nProvides the `mdedup` CLI, an utility to deduplicate mails from a set of boxes.\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/kdeldycke/mail-deduplicate/main/docs/images/cli-coloured-header.png" alt="Mail Deduplicate">\n</p>\n\n## Features\n\n- Duplicate detection based on cherry-picked and normalized mail\n  headers.\n- Fetch mails from multiple sources.\n- Reads and writes to `mbox`, `maildir`, `babyl`, `mh` and `mmdf`\n  formats.\n- Deduplication strategies based on size, content, timestamp, file path\n  or random choice.\n- Copy, move or delete the resulting set of duplicates.\n- Dry-run mode.\n- Protection against false-positives with safety checks on size and content differences.\n- Supports macOS, Linux and Windows.\n- [Standalone executables](#executables) for Linux, macOS and Windows.\n- Shell auto-completion for Bash, Zsh and Fish.\n\n> ⚠️ **Warning**: Performances\n>\n> `mdedup` implementation is quite naive at the moment and everything resides in memory.\n>\n> If this is good enough for a volume of a couple of gigabytes, the more emails `mdedup` try to parse, the closer you\'ll reach the memory limits of your machine. In which case [`mdedup` will exit abrubtly](https://github.com/kdeldycke/mail-deduplicate/issues/362#issuecomment-1266743045), zapped by the [OOM killer](https://en.wikipedia.org/wiki/Out_of_memory) of your OS. Of course your mileage may vary depending on your hardware.\n>\n> You can influence implementation of this feature with pull requests, or [purchase of business support 🤝 and sponsorship 🫶](https://github.com/sponsors/kdeldycke).\n\n## Example\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/kdeldycke/mail-deduplicate/main/docs/images/cli-coloured-run.png">\n</p>\n\n## Installation\n\n### From sources\n\nEasiest way is to install `mdedup` from sources with [`pipx`](https://pypa.github.io/pipx/):\n\n```shell-session\n$ pipx install mail-deduplicate\n```\n\nOther\n[alternatives installation methods](https://kdeldycke.github.io/mail-deduplicate/install.html)\nare available in the documentation.\n\n### Executables\n\nStandalone executables of `mdedup`\'s latest version are available for several platforms and architectures:\n\n| Platform    | `x86_64`                                                                                                                           |\n| ----------- | ---------------------------------------------------------------------------------------------------------------------------------- |\n| **Linux**   | [Download `mdedup-linux-x64.bin`](https://github.com/kdeldycke/mail-deduplicate/releases/latest/download/mdedup-linux-x64.bin)     |\n| **macOS**   | [Download `mdedup-macos-x64.bin`](https://github.com/kdeldycke/mail-deduplicate/releases/latest/download/mdedup-macos-x64.bin)     |\n| **Windows** | [Download `mdedup-windows-x64.exe`](https://github.com/kdeldycke/mail-deduplicate/releases/latest/download/mdedup-windows-x64.exe) |\n',
    'author': 'Kevin Deldycke',
    'author_email': 'kevin@deldycke.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kdeldycke/mail-deduplicate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
