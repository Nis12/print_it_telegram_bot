from setuptools import setup, find_packages

setup(
    name="PrintItBot",
    version="1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'printitbot = printitbot.main:main'
        ]
    },
    install_requires=[
        "requests",
        "python-telegram-bot"
    ],
)