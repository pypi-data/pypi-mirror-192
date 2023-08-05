from setuptools import setup, find_packages


setup(
    name="zs_ebay_sdk",
    version="0.0.1",
    author="Zonesmart",
    author_email="kamil@zonesmart.ru",
    packages=find_packages(include=["ebay_sdk", "ebay_sdk.*"]),
)
