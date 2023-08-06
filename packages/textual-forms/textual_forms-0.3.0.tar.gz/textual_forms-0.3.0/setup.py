# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['textual_forms']

package_data = \
{'': ['*']}

install_requires = \
['textual>=0.11']

setup_kwargs = {
    'name': 'textual-forms',
    'version': '0.3.0',
    'description': 'Dynamic forms for Textual TUI Framework',
    'long_description': '# Textual Forms\n\n[![Python Versions](https://shields.io/pypi/pyversions/textual-inputs)](https://www.python.org/downloads/)\n[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n[![Downloads](https://pepy.tech/badge/textual-forms)](https://pepy.tech/project/textual-forms)\n[![Downloads](https://pepy.tech/badge/textual-forms/month)](https://pepy.tech/project/textual-forms)\n\nDynamic forms for [Textual](https://github.com/willmcgugan/textual) TUI framework.\n\n> #### Note: This library is still very much WIP 🧪. This means that breaking changes can be introduced at any point in time.\n\n## About\n\nTextual Forms aims to make it easy to add forms to your Textual-powered applications.\n\n### Development Requirements\n\n* python >=3.7,<4\n* poetry\n* textual >=0.11.0\n\n## Install\n\n```bash\npip install textual-forms\n```\n\n## Forms\n\n`textual_forms.forms.Form`\n\n## Buttons\n\n`textual_forms.buttons.Button`\n\n## Fields\n\n`textual_forms.fields.StringField`\n\n`textual_forms.fields.NumberField`\n\n`textual_forms.fields.IntegerField`\n\n### Custom fields and validators\n\n```python\nfrom __future__ import annotations\n\nfrom typing import Any\n\nfrom textual_forms.fields import Field\nfrom textual_forms.validators import FieldValidator\n\n\nclass UUIDValidator(FieldValidator):\n    def validate(self, value: str, rules: dict[str, Any]) -> tuple[bool, str | None]:\n        return True, None\n\n\nclass UUIDField(Field):\n    validator = UUIDValidator()\n\n    def __init__(\n        self,\n        name: str,\n        *,\n        value: str | None = None,\n        required: bool = False,\n        placeholder: str | None = None,\n        **kwargs,\n    ):\n        data: dict[str, Any] = {\n            "name": name,\n            "value": value,\n            "required": required,\n            "placeholder": placeholder,\n            "rules": {},\n        }\n        super().__init__(data, **kwargs)\n```\n\n---\n\n## Example\n\n```python\nfrom rich.table import Table\nfrom textual.app import App, ComposeResult\nfrom textual.widgets import Static\n\nfrom textual_forms.forms import Form\nfrom textual_forms.fields import StringField, IntegerField\nfrom textual_forms.buttons import Button\n\n\nclass BasicTextualForm(App):\n    def compose(self) -> ComposeResult:\n        yield Static(id="submitted-data")\n        yield Static("Order for beers")\n        yield Form(\n            fields=[\n                StringField("name"),\n                IntegerField("age", required=True, min_value=21),\n            ],\n            buttons=[\n                Button(\n                    "Submit",\n                    enabled_on_form_valid=True,\n                )\n            ],\n        )\n\n    def on_form_event(self, message: Form.Event) -> None:\n        if message.event == \'submit\':\n            table = Table(*message.data.keys())\n            table.add_row(*message.data.values())\n            self.query_one(\'#submitted-data\').update(table)\n\n\nif __name__ == \'__main__\':\n\n    BasicTextualForm().run()\n\n```\n\n**Initial render**\n<img width="1004" alt="Screenshot 2022-11-15 at 3 49 46 PM" src="https://user-images.githubusercontent.com/7029352/202023490-e6494105-a102-4d9d-9072-90872ecad41a.png">\n\n**Valid form**\n<img width="1006" alt="Screenshot 2022-11-15 at 3 51 15 PM" src="https://user-images.githubusercontent.com/7029352/202023592-1a16f742-6af2-4e88-a9d3-7b84339fd231.png">\n\n**Invalid form**\n<img width="1006" alt="Screenshot 2022-11-15 at 3 51 39 PM" src="https://user-images.githubusercontent.com/7029352/202023734-76ae0b55-01b4-48a4-8a34-7c972d7a7df9.png">\n\n## Contributing\n\nTBD\n',
    'author': 'Lemuel Boyce',
    'author_email': 'lemuelboyce@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rhymiz/textual-forms',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
