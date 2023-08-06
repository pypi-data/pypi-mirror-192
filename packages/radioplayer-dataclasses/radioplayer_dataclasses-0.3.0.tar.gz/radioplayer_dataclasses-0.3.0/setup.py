# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataclasses']

package_data = \
{'': ['*']}

install_requires = \
['xsdata>=22.12,<23.0']

setup_kwargs = {
    'name': 'radioplayer-dataclasses',
    'version': '0.3.0',
    'description': 'Python dataclasses for radioplayer generated from XSD',
    'long_description': '# Python Radioplayer Dataclasses\n\nClasses for generating [radioplayer](https://radioplayer.co.uk) compatible data. Generated using [xsdata](https://xsdata.readthedocs.io/).\n\n## Installation\n\n```bash\npip install radioplayer-dataclasses\n```\n\n## Usage\n\nThe `radioplayer.dataclasses` module may be used to build radioplayer compatible structures.\nSerializing is done using the `xsdata` library.\n\n```python\n>>> from radioplayer.dataclasses import *\n>>> epg = Epg(lang="en")\n>>> epg\nEpg(programme_groups=[], schedule=[], alternate_source=[], lang=\'en\', system=<SystemType.DAB: \'DAB\'>)\n\n>>> from xsdata.formats.dataclass.serializers import XmlSerializer\n>>> from xsdata.formats.dataclass.serializers.config import SerializerConfig\n>>>\n>>> config = SerializerConfig(\n...     pretty_print=True,\n...     xml_declaration=False,\n... )\n>>> serializer = XmlSerializer(config=config)\n>>> xml = serializer.render(epg, ns_map={None: Epg.Meta.namespace})\n>>> print(xml.strip())\n<epg xmlns="http://www.radioplayer.co.uk/schemas/11/epgSchedule" xml:lang="en" system="DAB"/>\n\n```\n\nAdditional examples are available in the `tests/` directory.\n\n## Development\n\n### Getting Started\n\n```bash\n# setup a dev env\npython -mvenv env\n. env/bin/activate\n\n# install a modern poetry version\npython -mpip install \'poetry>=1.2.0\'\n\n# install deps and dev version\npoetry install\n```\n\n### Loading XSD files\n\n```bash\nmkdir schemas\npushd schemas/\ncurl -L -O http://www.w3.org/2001/xml.xsd\ncurl -L -O https://radioplayer.co.uk/schemas/11/epgSchedule_11.xsd\ncurl -L -O https://radioplayer.co.uk/schemas/11/epgDataTypes_11.xsd\ncurl -L -O https://radioplayer.co.uk/schemas/11/rpDataTypes_11.xsd\ncurl -L -O https://radioplayer.co.uk/schemas/11/epgSI_11.xsd\npopd\n```\n\nSome touchups where made to the files to make them validate where necessary.\n\n### Generating dataclasses\n\n```bash\npoetry run xsdata -c .xsdata.xml schemas/\n```\n\n### Running tests\n\n```bash\npoetry run pytest\n```\n\n## Release Management\n\nThe CI/CD setup uses semantic commit messages following the [conventional commits standard](https://www.conventionalcommits.org/en/v1.0.0/).\nThere is a GitHub Action in [.github/workflows/semantic-release.yaml](./.github/workflows/semantic-release.yaml)\nthat uses [go-semantic-commit](https://go-semantic-release.xyz/) to create new\nreleases.\n\nThe commit message should be structured as follows:\n\n```\n<type>[optional scope]: <description>\n\n[optional body]\n\n[optional footer(s)]\n```\n\nThe commit contains the following structural elements, to communicate intent to the consumers of your library:\n\n1. **fix:** a commit of the type `fix` patches gets released with a PATCH version bump\n1. **feat:** a commit of the type `feat` gets released as a MINOR version bump\n1. **BREAKING CHANGE:** a commit that has a footer `BREAKING CHANGE:` gets released as a MAJOR version bump\n1. types other than `fix:` and `feat:` are allowed and don\'t trigger a release\n\nIf a commit does not contain a conventional commit style message you can fix\nit during the squash and merge operation on the PR.\n\nOnce a commit has landed on the `main` branch a release will be created and automatically published to [pypi](https://pypi.org/)\nusing the GitHub Action in [.github/workflows/release.yaml](./.github/workflows/release.yaml) which uses [poetry](https://python-poetry.org/)\nto publish the package to pypi.\n\n## License\n\nThis application is free software: you can redistribute it and/or modify it under\nthe terms of the GNU Affero General Public License as published by the Free\nSoftware Foundation, version 3 of the License.\n\n## Copyright\n\nCopyright (c) 2022 [Radio Bern RaBe](http://www.rabe.ch)\n',
    'author': 'RaBe IT-Reaktion',
    'author_email': 'it@rabe.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/radiorabe/python-radioplayer-dataclasses',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
