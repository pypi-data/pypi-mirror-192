import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redis-workers",
    version="0.1.1",
    author="Onur Cetinkol",
    author_email="realiti44@gmail.com",
    description="A tool that simplifies Redis usage for repeating tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/realiti4/redis-worker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    packages=["redis_workers"],
    install_requires=["redis"],
)
