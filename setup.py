import sys
from setuptools import setup, find_packages

with open('colorlogging/version.py') as f:
    exec(f.read())

if len(set(('test', 'easy_install')).intersection(sys.argv)) > 0:
    import setuptools

setup(
    name="colorlogging",
    version=__version__,
    description="Simple color logging.",
    maintainer='Jerome B Chouinard',
    maintainer_email='jerome@pigeonland.net',
    url='http://github.com/jbchouinard/colorlogging',
    packages=find_packages(exclude=['tests', 'test_*']),
    package_data={'colorlogging': ['data/*'],
                  },
    license='MIT',
    download_url='https://github.com/jbchouinard/colorlogging/archive/%s.tar.gz' % __version__,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
