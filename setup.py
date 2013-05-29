from sys import version_info
from setuptools import setup, find_packages

basename = "anice"
version = "0.1"
pyversion = "%s.%s" % (version_info.major, version_info.minor)

setup(
    name = basename,
    version = version,
    packages = find_packages(),
    zip_safe = False,
    test_suite = 'test_plugins',
    author = "Spycher Hess",
    author_email = "hess_1234@gmx.net",
    description = "Anice's homepage",
    keywords = "art design",
    url = "https://github.com/mmcgill/mc3p",
    install_requires = ("WTForms", "flask", "PIL", "SQLAlchemy")
)