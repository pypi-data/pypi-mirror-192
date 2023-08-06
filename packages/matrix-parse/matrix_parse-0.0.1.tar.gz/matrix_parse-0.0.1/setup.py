from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]

setup(
    name="matrix_parse",
    version="0.0.1",
    description="Parse matrix by url",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    url="",
    author="Ilia Artnaiev",
    author_email="ilya.artnaev@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="parse matrix",
    packages=find_packages(),
    install_requires=["httpx", "asyncio", "parameterized"]
)
