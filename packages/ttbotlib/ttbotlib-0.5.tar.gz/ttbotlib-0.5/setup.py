import re
import pathlib
from setuptools import setup


try:
    version = re.findall(r"^__version__ = '([^']+)'\r?$",
        (pathlib.Path(__file__).parent / 'ttbot' / '__init__.py').read_text('utf-8'), re.M)[0]
except IndexError:
    raise RuntimeError('Unable to determine version.')


setup(
    version=version,
    packages=['ttbot'],

    install_requires=[
        'httpx<1.0',
        'uvicorn',
        'ttutils',
    ],

    setup_requires=[
        'pytest-runner',
    ],

    tests_require=[
        'pytest',
        'pytest-asyncio',
        'pytest-cov==2.10',
        'pytest-flake8',
        'pycodestyle==2.8',
        'flake8<5.0',
        'flake8-print',
        'flake8-blind-except',
        'flake8-builtins',
        'flake8-isort',
        'coverage',
    ]
)
