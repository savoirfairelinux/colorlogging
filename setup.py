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
    maintainer='Savoir-faire Linux',
    maintainer_email='support@savoirfairelinux.com',
    url='http://github.com/savoirfairelinux/colorlogging',
    packages=find_packages(exclude=['tests', 'test_*']),
    package_data={'colorlogging': ['data/*'],
                  },
    license='MIT',
    download_url='https://github.com/savoirfairelinux/colorlogging/archive/%s.tar.gz' % __version__,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
