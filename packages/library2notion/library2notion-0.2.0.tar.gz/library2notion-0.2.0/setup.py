# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['library2notion']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'csv2notion>=0.3.7,<0.4.0',
 'epub-meta>=0.0.7,<0.0.8',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pypdf2>=2.11.2,<3.0.0']

entry_points = \
{'console_scripts': ['library2notion = library2notion.library2notion:main']}

setup_kwargs = {
    'name': 'library2notion',
    'version': '0.2.0',
    'description': '',
    'long_description': '# library2notion\n\n[![PyPI version](https://img.shields.io/pypi/v/library2notion?label=version)](https://pypi.python.org/pypi/library2notion)\n[![Python Version](https://img.shields.io/pypi/pyversions/library2notion.svg)](https://pypi.org/project/library2notion/)\n\nA way to upload all your digital library in format .PDF or .EPUB to [Notion.so](https://notion.so). This tools will upload to a database in Notion relevant information from a digital library in order to make it easier to find books, add comments, filter by type or category and keep track of read ones.\n\nThis tool makes use of **csv2notion**, a tool created by [vzhd1701](https://github.com/vzhd1701/csv2notion).\n\n## Installation\n\n### Using portable binary\n\n[**Download the latest binary release**](https://github.com/helguera/library2notion/releases/latest).\n\n### With [Homebrew](https://brew.sh/) (Recommended for macOS)\n\n```bash\n$ brew install helguera/tap/library2notion\n```\n\n### With [PIPX](https://github.com/pypa/pipx) (Recommended for Linux & Windows)\n\n```shell\n$ pipx install library2notion\n```\n\n### With PIP\n\n```bash\n$ pip install --user library2notion\n```\n\n**Python 3.7 or later required.**\n\n### From source\n\nThis project uses [poetry](https://python-poetry.org/) for dependency management and packaging. You will have to install it first. See [poetry official documentation](https://python-poetry.org/docs/) for instructions.\n\n```shell\n$ git clone https://github.com/helguera/library2notion.git\n$ cd library2notion/\n$ poetry install\n$ poetry run library2notion\n```\n\n## Usage\n\n```plain\n$ library2notion --help\nusage: library2notion [-h] -p PATH [-l LOGFILEPATH] [-e EXTENSIONS [EXTENSIONS ...]] [-t NOTIONTOKEN] [-u NOTIONDBURL] [-f] [-o OUTPUTFOLDER]\n\nImport/Merge your digital library collection in .PFD or .EPUB format to Notion.\n\ngeneral options:\n  -p, --Path PATH                    Path where to start looking for books. It will also check all subfolders\n  -l, --LogFilePath LOGFILEPATH      Location of the log file if exists. If not, a new one will be created in the specified location\n  -e, --Extensions EXTENSIONS        List of extensions to be taken into account. At this moment .PDF, .EPUB and .PAPER are supported.\n  -t, --NotionToken NOTIONTOKEN      Notion token, stored in token_v2 cookie for notion.so\n  -u, --NotionDbUrl NOTIONDBURL      Notion DB URL\n  -f, --ForceUpload FORCEUPLOAD      Force upload to Notion (if token and db url are provided) ignoring the log file. If no Notion data is provided it will generate the .csv file.\n  -o, --OutputFolder OUTPUTFOLDER    Folder to store .csv, .xlsx, and deleted.json files. If not provided it will use \'./\'\n  -h, --help                         show this help message and exit\n```\n\n### Input\n\nYou must pass a starting path for the application to start searching for books with the `--Path` option. Also, a log file is needed if you have already executed the tool before. It can be passed with the `--LogFilePath` option. This log file will contain the status of previous execution so books that have already been scanned and upload won\'t be affected. If this log file is not provided, a new one will be created.\n\nOptionally you can specify what book extensions you want the application to analyze with the option `--Extensions`. At this moment .PDF and .EPUB are supported.\n\nIf you want the application to upload the data to Notion, you must provide a URL to an existing Notion database with the `--NotionDbUrl` option; The URL must link to a database view, not a page.\n\nThe tool also requires you to provide a `token_v2` cookie for the Notion website through `--NotionToken` option.\n\n**Important notice**. `token_v2` cookie provides complete access to your Notion account. Handle it with caution.\n\n### Metadata\n\nThe tool will extract the following data to upload to Notion:\n\n- **File Name**: is the full path to the file. It is used as primary key of the table in Notion, so it can\'t be duplicated.\n- **Title**: title of the book.\n- **Tags**: the categories of the book. They are generated automatically from the path. For example, if the path is `./Tech Books/Programming/Python/mybook.pdf`, the tags will be `Tech Books`, `Programming`, `Python`.\n- **Author**: the author or authors of the book.\n- **Publisher**: the publisher of the book.\n- **Formats**: the available formats of the book. A book available in multiple formats will only appear once in the database.\n- **ISBN**: the ISBN.\n\n### Columns\n\nThe tool will create a column per metadata extracted. Also, the following ones, which will be empty because they are only intended to be used in Notion, will be created:\n\n- **Priority**: allows to select a priority and filter by that property in Notion.\n- **Status**: the status of the book (reading, not started, on hold...)\n- **Comments**: if we need to add some comments to the book\n\n### Paper Books\n\nWith update 0.2.0, the tool supports physical books. You just have to create a `.paper` file in a folder per physical book that you want to add with the following content:\n\n```json\n{\n    "Title": "",\n    "Author": "",\n    "Publisher": "",\n    "ISBN": ""\n}\n```\n\n### Log File\n\nThe log file is a json file that contains info about the books that have already been uploaded to Notion. It will be automatically generated the first time the application is used. In next executions, if one or more files has been added to the path, the log file must be provided so the tool knows that only those new books have to be scanned and uploaded.\n\n### Deleted Books\n\nIf a book is deleted from the path, the tool will detect it the next time it is executed (only, of course, if a log file is provided). This will generate a `deleted.json` file in the ouput folder with the deleted books. But, **really important**, the book will not be deleted from Notion. That has to be done manually.\n\n## csv2notion\n\nThis tool analizes books and creates a .csv file with the results. The task of uploading the data to Notion is performed by the tool [csv2notion](https://github.com/vzhd1701/csv2notion).\n\n## Getting help\n\nIf you found a bug or have a feature request, please [open a new issue](https://github.com/helguera/library2notion/issues/new/choose).\n\nIf you have a question about the program or have difficulty using it, you are welcome to [the discussions page](https://github.com/helguera/library2notion/discussions). You can also mail me directly at [javier@javierhelguera.com](mailto:javier@javierhelguera.com), I\'m always happy to help.',
    'author': 'helguera',
    'author_email': 'javier@javierhelguera.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
