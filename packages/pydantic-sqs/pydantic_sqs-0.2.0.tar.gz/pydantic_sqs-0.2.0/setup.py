# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_sqs']

package_data = \
{'': ['*']}

install_requires = \
['aiobotocore>=2.4.0,<3.0.0', 'pydantic>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-sqs',
    'version': '0.2.0',
    'description': 'Send and receive AWS SQS messages directly to pydantic objects',
    'long_description': '# pydantic-sqs\n\nConvert your pydantic models to and from AWS SQS messages.\n\n<p align="center">\n    <a href="https://github.com/andrewthetechie/pydantic-sqs" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/andrewthetechie/pydantic-sqs" alt="Latest Commit">\n    </a>\n    <img src="https://img.shields.io/badge/license-MIT-green">\n    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/andrewthetechie/pydantic-sqs?label=Latest%20Release">\n    <br />\n    <a href="https://github.com/andrewthetechie/pydantic-sqs/issues"><img src="https://img.shields.io/github/issues/andrewthetechie/pydantic-sqs" /></a>\n    <img alt="GitHub Workflow Status Test and Lint (branch)" src="https://img.shields.io/github/workflow/status/andrewthetechie/pydantic-sqs/Tests/main?label=Tests">\n    <br />\n    <a href="https://pypi.org/project/pydantic-sqs" target="_blank">\n        <img src="https://img.shields.io/pypi/v/pydantic-sqs" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/pydantic-sqs">\n</p>\n\n## Main Dependencies\n\n- [Python +3.7](https://www.python.org)\n- [pydantic](https://github.com/samuelcolvin/pydantic/)\n- [aiobotocore](https://github.com/aio-libs/aiobotocore)\n\n## Getting Started\n\n```python\nfrom pydantic_sqs import SQSModel, SQSQueue\nfrom pydantic import Field\nimport asyncio\nfrom pprint import pprint\nimport os\n\n\nclass ThisModel(SQSModel):\n    foo: str = Field(..., description="Foo")\n\n\nclass ThatModel(SQSModel):\n    bar: str = Field(..., description="bar")\n\n\nasync def main():\n    queue_kwargs = {\n        "queue_url": os.environ.get("SQS_QUEUE_URL"),\n        "endpoint_url": os.environ.get("SQS_ENDPOINT_URL", None),\n        "use_ssl": os.environ.get("SQS_USE_SSL", "true").lower() == "true",\n    }\n    if queue_kwargs["endpoint_url"] is None:\n        del queue_kwargs["endpoint_url"]\n\n    queue = SQSQueue(**queue_kwargs)\n\n    queue.register_model(ThisModel)\n    queue.register_model(ThatModel)\n\n    this_thing = ThisModel(foo="1234")\n    that_thing = ThatModel(bar="5678")\n    await this_thing.to_sqs()\n    await that_thing.to_sqs()\n\n    new_things = await queue.from_sqs(max_messages=10, wait_time_seconds=90)\n    pprint(new_things)\n    for thing in new_things:\n        await thing.delete_from_queue()\n\n    print("deleted all the messages we got from the queue")\n    pprint(new_things)\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\n### Examples\n\nExamples are in the [examples/](./examples) directory of this repo.\n\n### Installation\n\nInstall the package\n\n    pip install pydantic-sqs\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide](./CONTRIBUTING.rst)\n\n## License\n\nLicensed under the [MIT License](./LICENSE)\n',
    'author': 'Andrew Herrington',
    'author_email': 'andrew.the.techie@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/andrewthetechie/pydantic-sqs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
