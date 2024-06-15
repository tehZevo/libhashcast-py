from setuptools import setup, find_packages

setup(name="libhashcast",
    version="0.0.0",
    install_requires = [
        "pynacl",
        "pyyaml",
        "git+https://github.com/tehzevo/protopost-python",
    ],
    packages=find_packages()
)