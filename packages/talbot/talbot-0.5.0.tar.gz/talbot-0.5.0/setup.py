# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['talbot', 'talbot.metadata', 'talbot.readers', 'talbot.writers']

package_data = \
{'': ['*'], 'talbot': ['resources/schemas/*', 'resources/spdx/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'beautifulsoup4>=4.11,<5.0',
 'bibtexparser>=1.4,<2.0',
 'bleach>=6.0,<7.0',
 'citeproc-py-styles>0.1',
 'citeproc-py>=0.6,<0.7',
 'codecov>=2.1,<3.0',
 'datacite>=1.1,<2.0',
 'dateparser>=1.1.7,<2.0.0',
 'docutils>=0.19,<0.20',
 'jsonschema>=4.17,<5.0',
 'lxml>=4.9,<5.0',
 'pydash>=6.0,<7.0',
 'pytest-cov>=4.0,<5.0',
 'pytest-recording>=0.12,<0.13',
 'pytest>=7.2,<8.0',
 'requests>=2.28,<3.0',
 'simplejson>=3.18,<4.0',
 'sphinx-autodoc-typehints>=1.19,<2.0',
 'sphinxcontrib-issuetracker>=0.11,<0.12',
 'tqdm>=4.64,<5.0',
 'types-beautifulsoup4>=4.11,<5.0',
 'types-bleach>=6.0,<7.0',
 'types-dateparser>=1.1,<2.0',
 'types-requests>=2.28,<3.0',
 'vcrpy>=4.2,<5.0']

setup_kwargs = {
    'name': 'talbot',
    'version': '0.5.0',
    'description': 'Library for conversions of scholarly metadata',
    'long_description': '[![Build](https://github.com/front-matter/talbot/actions/workflows/build.yml/badge.svg)](https://github.com/front-matter/talbot/actions/workflows/build.yml)\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=front-matter_talbot&metric=coverage)](https://sonarcloud.io/summary/new_code?id=front-matter_talbot)\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=front-matter_talbot&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=front-matter_talbot)\n![GitHub](https://img.shields.io/github/license/front-matter/talbot?logo=MIT)\n\n# Talbot\n\nTalbot is a Python library to convert scholarly metadata, modelled after the [briard ruby gem](https://github.com/front-matter/briard). Talbot is work in progress, the first release on PyPi is\nplanned for March 2023.\n\n## Installation\n\nDev version\n\n    pip install git+https://github.com/front-matter/talbot.git#egg=talbot\n\nOr build it yourself locally\n\n    git clone https://github.com/front-matter/talbot.git\n    cd Talbot\n    make install\n\n## Supported Metadata Formats\n\nTalbot reads and/or writes these metadata formats:\n\n| Format                                                                                           | Name          | Content Type                           | Read    | Write   |\n| ------------------------------------------------------------------------------------------------ | ------------- | -------------------------------------- | ------- | ------- |\n| [CrossRef Unixref XML](https://www.crossref.org/schema/documentation/unixref1.1/unixref1.1.html) | crossref_xml      | application/vnd.crossref.unixref+xml   | later | planned |\n| [Crossref](https://api.crossref.org)                                                             | crossref | application/vnd.crossref+json          | yes     | no      |\n| [DataCite XML](https://schema.datacite.org/)                                                     | datacite_xml      | application/vnd.datacite.datacite+xml  | later | later |\n| [DataCite](https://api.datacite.org/)                                                            | datacite | application/vnd.datacite.datacite+json | yes     | yes |\n| [Schema.org (in JSON-LD)](http://schema.org/)                                                    | schema_org    | application/vnd.schemaorg.ld+json      | yes     | yes     |\n| [RDF XML](http://www.w3.org/TR/rdf-syntax-grammar/)                                              | rdf_xml       | application/rdf+xml                    | no      | later   |\n| [RDF Turtle](http://www.w3.org/TeamSubmission/turtle/)                                           | turtle        | text/turtle                            | no      | later   |\n| [Citeproc JSON](https://citationstyles.org/)                                                     | citeproc      | pplication/vnd.citationstyles.csl+json | yes | yes     |\n| [Formatted text citation](https://citationstyles.org/)                                           | citation      | text/x-bibliography                    | no      | yes     |\n| [Codemeta](https://codemeta.github.io/)                                                          | codemeta      | application/vnd.codemeta.ld+json       | yes | later |\n| [Citation File Format (CFF)](https://citation-file-format.github.io/)                            | cff           | application/vnd.cff+yaml               | later | later |\n| [JATS](https://jats.nlm.nih.gov/)                                                                | jats          | application/vnd.jats+xml               | later   | later   |\n| [CSV](ttps://en.wikipedia.org/wiki/Comma-separated_values)                                       | csv           | text/csv                               | no      | later   |\n| [BibTex](http://en.wikipedia.org/wiki/BibTeX)                                                    | bibtex        | application/x-bibtex                   | later | yes     |\n| [RIS](http://en.wikipedia.org/wiki/RIS_(file_format))                                            | ris           | application/x-research-info-systems    | later | yes     |\n\n_Planned_: we plan to implement this format for the first public release.  \n_Later_: we plan to implement this format in a later release.\n\n## Documentation\n\nDocumentation (work in progress) for using the library is available at [Front Matter Documentation](https://docs.front-matter.io/talbot/).\n\n## Meta\n\n-   Please note that this project is released with a [Contributor Code of Conduct](https://github.com/front-matter/talbot/blob/main/CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.\n-   License: [MIT](https://github.com/front-matter/talbot/blob/main/LICENSE)\n',
    'author': 'Martin Fenner',
    'author_email': 'martin@front-matter.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
