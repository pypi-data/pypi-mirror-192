from setuptools import setup, find_packages


VERSION = "0.1.0"
DESCRIPTION = "Capital.com API wrapper"
LONG_DESCRIPTION = "A package that allows to make API calls to capital.com."

# Setting up
setup(
    name="python-capital",
    version=VERSION,
    author="Iuri Campos",
    # author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["requests", "pycryptodome"],
    keywords=["CFDs", "python", "capital.com"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
