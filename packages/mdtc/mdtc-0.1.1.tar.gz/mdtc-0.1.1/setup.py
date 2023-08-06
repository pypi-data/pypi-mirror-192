# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdtc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mdtc',
    'version': '0.1.1',
    'description': 'A model-driven configuration object for TOML or dict-based configs.',
    'long_description': '# Readme\n\nMDTC - Model-driven TOML Configuration.\n\nA lightweight config singleton meant for storing your application\'s config state no matter where or how many times it is instantiated.\nYou can pass this object around across your entire app and not worry about config mutations, unvalidated config values or lack of IDE completions.\nOriginally meant for use with TOML key/value-based configs, but any k/v object should work as long as it complies with the model.\n\nThe source documentation can be found [here](https://pm5k.github.io/mdtc/)\n\n## What is MDTC for?\n\n- Avoids having to use or chain `.get()` or retrieve config values via `cfg["foo"]["bar"]["baz"]`.\n- Code-completion-friendly via model-driven approach.\n- Custom configuration validation (either via Pydantic\'s interfaces or custom-built validators you define).\n- Immutable config state support. The config itself is immutable by default - you cannot replace `config.foo` with another value, for instance.\n- Supports nicer type hints instead of a huge TypeDict or another approach for a config dictionary loaded into Python.\n\n## What MDTC is not for\n\n- It is not meant to replace other methods of loading TOML or dict configs, it simply provides an alternative for housing your TOML config values.\n- It is not meant as "less code". The guarantees it provides require a different implementation approach, and won\'t always result in less upfront code.\n- Codebases using other approaches or small configs won\'t benefit from this approach as much.\n\n## Dependencies\n\nNone, just the Python standard library.\n\n## Examples\n\n### Simple Configuration\n\n```py title="main.py"\nimport tomllib # python3.11-only, use tomli for <=3.10\n\nfrom dataclasses import dataclass\nfrom mdtc import Config\n\n@dataclass\nclass FooCfg:\n    foo: str\n    bar: str\n\n    _name: str = "misc"\n    _key: str = "config.misc"\n\n\nclass MyConf(Config):\n    misc: FooCfg\n\ncfg = """\n[config.misc]\nfoo="bar"\nbar="baz"\n"""\n\ntoml = tomllib.loads(cfg)\n\nconfig = MyConf(toml)\n```\n\n### Pydantic Models in your Configuration\n\n```py title="main.py"\nimport tomllib # python3.11-only, use tomli for <=3.10\n\nfrom pydantic import BaseModel\nfrom mdtc import Config\n\n\nclass FooCfg(BaseModel):\n    _name: str = "misc"\n    _key: str = "config.misc"\n    \n    foo: str\n    bar: str\n\n\nclass MyConf(Config):\n    misc: FooCfg\n\n\ncfg = """\n[config.misc]\nfoo="bar"\nbar="baz"\n"""\n\ntoml = tomllib.loads(cfg)\n\nconfig = MyConf(toml)\n```\n\n### Pydantic `dataclass` Example\n\n```py title="main.py"\nimport tomllib # python3.11-only, use tomli for <=3.10\n\nfrom pydantic import Field, validator\nfrom pydantic.dataclasses import dataclass\n\nfrom mdtc import Config\n\n\n@dataclass\nclass FooCfg:\n    foo: str\n    bar: str = Field(title="A bar to get drinks in..")\n\n    _name: str = "misc"\n    _key: str = "config.misc"\n\n    @validator("foo")\n    def name_must_contain_space(cls, v):\n        if " " in v:\n            raise ValueError("must NOT contain a space!")\n        return v.title()\n\n\nclass MyConf(Config):\n    misc: FooCfg\n\n\ncfg = """\n[config.misc]\nfoo="bar"\nbar="baz"\n"""\n\ntoml = tomllib.loads(cfg)\n\nconfig = MyConf(toml)\n```\n\n## Contributing\n\n`Coming soon..`\n',
    'author': 'pm5k',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
