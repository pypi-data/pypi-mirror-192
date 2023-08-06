from setuptools import setup
from pathlib import Path

BASE = Path(__file__).parent
LONG_DESCRIPTIONS = (BASE / "README.md").read_text()
setup(
    name="ChromaticColorBurst",
    version='1.0.2',
    description="You can now print styled TEXT to console/terminal without much of a hassel",
    long_description=LONG_DESCRIPTIONS,
    long_description_content_type="text/markdown",
    keywords='colored_text console terminal style styled_text',
    author='Sachin Acharya',
    author_email='acharyaraj71+ColorBurst@gmail.com',
    packages=['ColorBurst'],
    url='https://github.com/sachin-acharya-projects/ColorBurst',
    package_data={
        '': ['LISCENCE.md']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    include_package_data=True
)
# python .\setup.py sdist bdist_wheel