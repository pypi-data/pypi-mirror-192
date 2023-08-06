import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = fh.read()
    return [
        line.strip() for line in requirements.splitlines()
        if not line.startswith('#')
    ]

setuptools.setup(
    name="orbro-python-sdk",
    version="0.20",
    author="ORBRO",
    author_email="platform.dev@kong-tech.com",
    description="ORBRO-Connect SDK for Python(FastAPI/Flask)",
    license='Apache License 2.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.notion.so/ORBRO-Connect-7065dd4435264beebdeb52c7f7408820",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Topic :: Office/Business",
        "Framework :: FastAPI"
    ],
    keywords="orbro connect iot digitaltwin rtls",
    packages=['orbro_sdk', 'orbro_sdk.fastapi.api_router',
              'orbro_sdk.fastapi.dependencies', 'orbro_sdk.fastapi.middleware'],
    python_requires=">=3.7",
    install_requires=read_requirements()
)