from setuptools import find_namespace_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="oap-rq",
    version="0.0.2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Caleb Carvalho",
    author_email="caleb.carvalho@gmail.com",
    platform="python >=3.8",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=["python-json-logger"],
    extras_require={
        "dev": ["black", "isort", "flake8", "pytest", "fakeredis", "pytest-asyncio"]
    },
    zip_safe=False,
    entry_points={},
)
