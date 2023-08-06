# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['animate_puml']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=9.4.0,<10.0.0',
 'py-executable-checklist==1.4.0',
 'pygifsicle>=1.0.7,<2.0.0',
 'pytest>=7.2.0,<8.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'rich>=13.0.0,<14.0.0']

entry_points = \
{'console_scripts': ['animate-puml = animate_puml.app:main']}

setup_kwargs = {
    'name': 'animate-puml',
    'version': '0.4.0',
    'description': 'Simple animation of PlantUML diagrams',
    'long_description': '# PlantUML Animation\n\n[![PyPI](https://img.shields.io/pypi/v/animate-puml?style=flat-square)](https://pypi.python.org/pypi/animate-puml/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/animate-puml?style=flat-square)](https://pypi.python.org/pypi/animate-puml/)\n[![PyPI - License](https://img.shields.io/pypi/l/animate-puml?style=flat-square)](https://pypi.python.org/pypi/animate-puml/)\n\nSimple animation for PlantUML diagrams.\n\n![](assets/security-puml.gif)\n\n---\n\n**Documentation**: [https://namuan.github.io/animate-puml](https://namuan.github.io/animate-puml)\n\n**Source Code**: [https://github.com/namuan/animate-puml](https://github.com/namuan/animate-puml)\n\n**PyPI**: [https://pypi.org/project/animate-puml/](https://pypi.org/project/animate-puml/)\n\n---\n\n## Pre-requisites\n\n- [PlantUML](https://plantuml.com/)\n  ```shell\n  brew install plantuml\n  ```\n\n## Installation\n\n```sh\npip install animate-puml\n```\n\n## How it works\n\n## Sample PlantUML Document\n\n```puml\n@startuml\n\n\' scale 1000 width\n\n!$disabled = "<color:lightgray><size:14>"\n\nrectangle "<size:20>Client" as Client #LightCyan\nrectangle "AUTH" as Auth\nrectangle "API_GATEWAY" as APIG\n\nrectangle GCP #LightCyan {\n    node "ServiceA" as ServiceA\n    node "ServiceB" as ServiceB\n    node "ServiceC" as ServiceC\n    queue "Kafka" as Queue\n}\n\n\' start\nClient -right[#lightgray]-> Auth : $disabled Get Token\nClient -right[#lightgray]-> APIG : $disabled Pass token\nAPIG -up[#lightgray]-> Auth : $disabled Validate token\nAPIG -right[#lightgray]-> ServiceA : $disabled Pass token\nServiceA -up[#lightgray]-> Auth : $disabled Validate token\nServiceA -right[#lightgray]-> ServiceB : $disabled Pass token\nServiceB -up[#lightgray]-> Auth : $disabled Validate token\nServiceA -down[#lightgray]-> Queue : $disabled Pass token\nQueue -down[#lightgray]-> ServiceC : $disabled Pass token\nServiceC -up[#lightgray]-> Auth : $disabled Validate token\n\' end\n\n@enduml\n```\n\n## Acknowledgements\n\n- [PlantUML](https://plantuml.com/)\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * Python 3.7+\n  * [Poetry](https://python-poetry.org/)\n\n* Create a virtual environment and install the dependencies\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n```sh\npoetry shell\n```\n\n### Validating build\n```sh\nmake build\n```\n\n### Release process\nA release is automatically published when a new version is bumped using `make bump`.\nSee `.github/workflows/build.yml` for more details.\nOnce the release is published, `.github/workflows/publish.yml` will automatically publish it to PyPI.\n\n### Disclaimer\n\nThis project is not affiliated with PlantUML.\n',
    'author': 'namuan',
    'author_email': 'github@deskriders.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://namuan.github.io/animate-puml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<4.0',
}


setup(**setup_kwargs)
