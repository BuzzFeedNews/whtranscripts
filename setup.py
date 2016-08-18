import sys
from setuptools import setup, find_packages

setup(
    name="whtranscripts",
    version="0.1.0",
    description="whtranscripts helps you fetch and parse transcripts from the American Presidency Project's press-briefing and presidential-news-conference transcripts.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.5",
    ],
    keywords="white house news conferences press briefings american presidency project",
    author="John Templon",
    author_email="john.templon@buzzfeed.com",
    url="http://github.com/buzzfeednews/whtranscripts/",
    download_url="https://github.com/BuzzFeedNews/whtranscripts/tarball/0.1",
    license="MIT",
    packages=find_packages(exclude=["test",]),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        "requests",
        "lxml",
        "cssselect",
        "six"
    ],
    tests_require=[
        "nose",
        "pandas",
    ],
    test_suite="test",
    entry_points={
        "console_scripts": [
        ]
    }
)
