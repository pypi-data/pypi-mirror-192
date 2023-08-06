from setuptools import setup, find_packages

setup(
    name = 'ajab-gg',
    version = '0.0.5',
    author='OKB',
    author_email = 'aliahmad@gmail.com',
    description = 'This is a powerful library for building self robots in Rubika',
    keywords = ['rubika'],
    long_description = 'OK',
    python_requires="~=3.7",
    long_description_content_type = 'text/markdown',
    url = 'https://web.rubika.ir',
    packages = find_packages(),
    install_requires = ['requests','ujson','urllib3','pycryptodome','rubiran'],
    classifiers = [
    	"Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ]
)