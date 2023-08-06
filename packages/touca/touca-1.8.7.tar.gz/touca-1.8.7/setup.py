# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['touca',
 'touca.cli',
 'touca.cli.plugins',
 'touca.cli.results',
 'touca.plugins']

package_data = \
{'': ['*'], 'touca.cli': ['profiles/*']}

install_requires = \
['certifi>=2022.12.7,<2023.0.0',
 'flatbuffers>=23.1.4,<24.0.0',
 'rich>=12.6.0,<13.0.0',
 'touca-fbs>=0.0.3,<0.0.4',
 'urllib3>=1.26.14,<2.0.0']

entry_points = \
{'console_scripts': ['touca = touca.cli.__main__:main']}

setup_kwargs = {
    'name': 'touca',
    'version': '1.8.7',
    'description': 'Touca SDK for Python',
    'long_description': '# Touca Python SDK\n\n[![PyPI](https://img.shields.io/pypi/v/touca?color=blue)](https://pypi.org/project/touca/)\n[![License](https://img.shields.io/pypi/l/touca?color=blue)](https://github.com/trytouca/trytouca/blob/main/sdk/python/LICENSE)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/touca)](https://pypi.org/project/touca)\n[![Build Status](https://img.shields.io/github/actions/workflow/status/trytouca/trytouca/build.yml?branch=main)](https://github.com/trytouca/trytouca/actions/workflows/build.yml?query=branch:main+event:push)\n[![Documentation Status](https://readthedocs.org/projects/touca-python/badge/?version=latest)](https://touca-python.readthedocs.io)\n[![Code Coverage](https://img.shields.io/codecov/c/github/trytouca/trytouca)](https://app.codecov.io/gh/trytouca/trytouca)\n\n## Install\n\n```bash\npip install touca\n```\n\nWe support Python v3.7 and newer.\n\n## Sneak Peak\n\n> For a more thorough guide of how to use Touca SDK for Python, refer to our\n> [documentation website](https://touca.io/docs).\n\nLet us imagine that we want to test a software workflow that takes the username\nof a student and provides basic information about them.\n\n```py\ndef test_find_student():\n    alice = find_student("alice")\n    assert alice.fullname == "Alice Anderson"\n    assert alice.dob == date(2006, 3, 1)\n    assert alice.gpa == 3.9\n```\n\nWe can use unit testing in which we hard-code expected values for each input.\nBut real-world software is complex:\n\n- We need a large number of test inputs to gain confidence that our software\n  works as expected.\n- Describing the expected behavior of our software for each test input is\n  difficult.\n- When we make intentional changes to the behavior of our software, updating our\n  expected values is cumbersome.\n\nTouca is effective in testing software workflows that need to handle a large\nvariety of inputs or whose expected behavior is difficult to hard-code.\n\n```py\nimport touca\nfrom students import find_student\n\n@touca.workflow(testcases=["alice", "bob", "charlie"])\ndef students_test(username: str):\n    student = find_student(username)\n    touca.check("fullname", student.fullname)\n    touca.check("dob", student.dob)\n    touca.check("gpa", student.gpa)\n```\n\nThis is slightly different from a typical unit test:\n\n- Touca tests do not use expected values.\n- Touca tests do not hard-code input values.\n\nWith Touca, we describe how we run our code under test for any given test case.\nWe can capture values of interesting variables and runtime of important\nfunctions to describe the behavior and performance of our workflow for that test\ncase.\n\n![Sample Test Output](https://touca.io/docs/external/assets/touca-run-python.dark.gif)\n\nNow if we make changes to our workflow under test, we can rerun this test and\nlet Touca automatically compare our captured data points against those of a\nprevious baseline version and report any difference in behavior or performance.\n\n## Documentation\n\n- [Documentation Website](https://touca.io/docs): If you are new to Touca, this\n  is the best place to start.\n- [Python SDK API Reference](https://touca.io/docs/external/sdk/python/index.html):\n  Auto-generated source code documentation for Touca Python SDK with explanation\n  about individual API functions.\n- [Python Examples](https://github.com/trytouca/trytouca/tree/main/examples/python):\n  Sample Python projects that show how to use Touca in various real-world\n  use-cases.\n\n## Community\n\nWe hang on [Discord](https://touca.io/discord). Come say hi! We love making new\nfriends. If you need help, have any questions, or like to contribute or provide\nfeedback, that\'s the best place to be.\n\n## Contributing\n\nWe welcome all forms of contributions, from adding new features to improving\ndocumentation and sharing feedback.\n\n- [Code of Conduct](https://touca.io/docs/contributing/conduct/)\n- [Contributing Guide](https://touca.io/docs/contributing/)\n- [Good First Issues](https://touca.io/docs/contributing/good-first-issues/)\n\n## FAQ\n\n- Should I install Touca as a development dependency?\n\n  Yes, unless you like to capture data-points that are not accessible through\n  your software\'s public API. Touca data capturing functions (e.g. `touca.check`\n  and `touca.scoped_timer`) are no-op in production environments. They only work\n  when called from a `@touca.workflow` context.\n\n- How is Touca making money?\n\n  Touca is open-source software that you can self-host for free. Touca, Inc.\n  operates [Touca Cloud](https://app.touca.io): a managed cloud instance of\n  Touca with additional enterprise-ready features. We have a free plan and\n  leverage usage-based pricing to charge for storage and service. Visit our\n  [pricing page](https://touca.io/pricing) to learn more.\n\n## License\n\nThis repository is released under the Apache-2.0 License. See\n[`LICENSE`](https://github.com/trytouca/trytouca/blob/main/sdk/python/LICENSE).\n',
    'author': 'Touca, Inc.',
    'author_email': 'hello@touca.io',
    'maintainer': 'Pejman Ghorbanzade',
    'maintainer_email': 'pejman@touca.io',
    'url': 'https://touca.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
