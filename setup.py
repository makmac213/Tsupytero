import tsupytero

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name=tsupytero.__app_name__,
    version=tsupytero.__version__,
    description=tsupytero.__description__,
    author=tsupytero.__author__,
    author_email=tsupytero.__author_email__,
    packages=['tsupytero'],
    install_requires=['requests', 'matplotlib'],
    url=tsupytero.__app_url__,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'License :: Freeware',
    ),
    download_url=tsupytero.__download_url__,
)