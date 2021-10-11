from setuptools import setup

setup(
    name='js_lib',
    version='0.0.1',
    description='js pip install',
    url="https://github.com/MeluvRose/N3XX_Modules.git",
    author='jinskim',
    author_email='asfd',
    license='JS',
    packages=['js_lib'],
    zip_safe=False,
    install_requires=[
        "beautifulsoup4==4.10.0",
        "selenium==3.141.0"
    ]
)
