# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mypy_json_report']
entry_points = \
{'console_scripts': ['mypy-json-report = mypy_json_report:main']}

setup_kwargs = {
    'name': 'mypy-json-report',
    'version': '1.0.0',
    'description': 'Generate a JSON report from your mypy output',
    'long_description': '# Mypy JSON Report\n\nA JSON report of your mypy output\nthat helps you push towards full type coverage of your project.\n\n## Quickstart\n\nInstall with pip.\n```\npip install mypy-json-report\n```\n\nPipe the output of mypy through the `mypy-json-report` CLI app.\nStore the output to a file, and commit it to your git repo.\n\n```\nmypy . --strict | mypy-json-report parse --output-file mypy-ratchet.json\ngit add mypy-ratchet.json\ngit commit -m "Add mypy errors ratchet file"\n```\n\nNow you have a snapshot of the mypy errors in your project.\nCompare against this file when making changes to your project to catch regressions and improvements.\n\n## Example output\n\nIf mypy was showing you errors like this:\n\n```\nexample.py:8: error: Function is missing a return type annotation\nexample.py:8: note: Use "-> None" if function does not return a value\nexample.py:58: error: Call to untyped function "main" in typed context\nexample.py:69: error: Call to untyped function "main" in typed context\nFound 3 errors in 1 file (checked 3 source files)\n```\n\nThen the report would look like this:\n\n```json\n{\n  "example.py": {\n    "Call to untyped function \\"main\\" in typed context": 2,\n    "Function is missing a return type annotation": 1\n  }\n}\n```\n\nErrors are grouped by file.\nTo reduce churn,\nthe line on which the errors occur is removed\nand repeated errors are counted.\n\n\n## Ratchet file\n\nThe `--diff-old-report FILENAME` flag serves two purposes.\n\n1. It prints new (and adjacent, and similar) errors to STDERR.\n   This is useful for seeing what errors need to be fixed before committing.\n\n1. It will error when the ratchet file doesn\'t match the new report.\n   This is helpful for catching uncommitted changes in CI.\n\n## Example usage\n\nYou could create a GitHub Action to catch regressions (or improvements).\n\n```yaml\n---\nname: Mypy check\n\non: [push]\n\njobs:\n  build:\n    runs-on: ubuntu-latest\n\n  mypy:\n    steps:\n      - name: Checkout code\n        uses: actions/checkout@v2\n\n      - name: Set up Python\n        uses: actions/setup-python@v2\n        with:\n          python-version: "3.10"\n\n      - name: Install Python dependencies\n        run: |\n          pip install mypy mypy-json-report\n\n      - name: Run mypy\n        run: |\n          mypy . --strict | mypy-json-report parse --diff-old-report mypy-ratchet.json --output-file mypy-ratchet.json\n```\n',
    'author': 'Charlie Denton',
    'author_email': 'charlie@meshy.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/memrise/mypy-json-report',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
