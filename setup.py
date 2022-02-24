from setuptools import setup

setup(
    name='Pyntel4004-cli',
    version='0.0.1-alpha',
    py_modules='4004cli',
    install_requires=[
        'Click'
        'Pyntel4004',
    ],
    entry_points='''
        [console_scripts]
        4004=4004cli:cli
    ''',
)
