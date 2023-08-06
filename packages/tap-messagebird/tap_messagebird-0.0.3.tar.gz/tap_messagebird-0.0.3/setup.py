# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_messagebird', 'tap_messagebird.tests']

package_data = \
{'': ['*'], 'tap_messagebird': ['schemas/*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.17.0,<0.18.0']

extras_require = \
{'s3': ['fs-s3fs>=1.1.1,<2.0.0']}

entry_points = \
{'console_scripts': ['tap-messagebird = '
                     'tap_messagebird.tap:TapMessagebird.cli']}

setup_kwargs = {
    'name': 'tap-messagebird',
    'version': '0.0.3',
    'description': '`tap-messagebird` is a Singer tap for Messagebird, built with the Meltano Singer SDK.',
    'long_description': "# `tap-messagebird`\n\nMessagebird tap class.\n\nBuilt with the [Meltano Singer SDK](https://sdk.meltano.com).\n\n## Capabilities\n\n* `catalog`\n* `discover`\n* `about`\n* `stream-maps`\n* `schema-flattening`\n\n## Settings\n\n| Setting             | Required | Default | Description |\n|:--------------------|:--------:|:-------:|:------------|\n| api_key             | True     | None    | The token to authenticate against the API service. Test keys are not supported for Conversations see https://support.messagebird.com/hc/en-us/articles/360000670709-What-is-the-difference-between-a-live-key-and-a-test-key- |\n| start_date          | False    | now -3 years | When to pull records starting at what date. ISO8601 format of date, defaults to 3 years ago. |\n| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |\n| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |\n| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |\n| flattening_max_depth| False    | None    | The max depth to flatten schemas. |\n\nA full list of supported settings and capabilities is available by running: `tap-messagebird --about`\n\n\n## Installation\n\nInstall from PyPi:\n\n```bash\npipx install tap-messagebird\n```\n\n\n### Configure using environment variables\n\nThis Singer tap will automatically import any environment variables within the working directory's\n`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching\nenvironment variable is set either in the terminal context or in the `.env` file.\n\n### Source Authentication and Authorization\n\nNote that Conversations do not work without a Production API key\n\n## Usage\n\nYou can easily run `tap-messagebird` by itself or in a pipeline using [Meltano](https://meltano.com/).\n\n### Executing the Tap Directly\n\n```bash\ntap-messagebird --version\ntap-messagebird --help\ntap-messagebird --config CONFIG --discover > ./catalog.json\n```\n\n## Developer Resources\n\nFollow these instructions to contribute to this project.\n\n### Initialize your Development Environment\n\n```bash\npipx install poetry\npoetry install\n```\n\n### Create and Run Tests\n\nCreate tests within the `tap_messagebird/tests` subfolder and\n  then run:\n\n```bash\npoetry run pytest\n```\n\nYou can also test the `tap-messagebird` CLI interface directly using `poetry run`:\n\n```bash\npoetry run tap-messagebird --help\n```\n\n### Testing with [Meltano](https://www.meltano.com)\n\n_**Note:** This tap will work in any Singer environment and does not require Meltano.\nExamples here are for convenience and to streamline end-to-end orchestration scenarios._\n\nNext, install Meltano (if you haven't already) and any needed plugins:\n\n```bash\n# Install meltano\npipx install meltano\n# Initialize meltano within this directory\ncd tap-messagebird\nmeltano install\n```\n\nNow you can test and orchestrate using Meltano:\n\n```bash\n# Test invocation:\nmeltano invoke tap-messagebird --version\n# OR run a test `elt` pipeline:\nmeltano elt tap-messagebird target-jsonl\n```\n\n### SDK Dev Guide\n\nSee the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to\ndevelop your own taps and targets.\n",
    'author': 'Meltano',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
