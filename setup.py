from setuptools import setup


with open('README.rst') as f:
    readme = f.read()

setup(
    name='zipencrypt',
    version='0.3.1',
    description='Encryption for zipfile',
    long_description=readme,
    url='https://github.com/devthat/zipencrypt',
    author='Jonathan Koch',
    author_email='devthat@mailbox.org',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: System :: Archiving :: Compression',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    keywords='zipfile encryption zip password write writestr',
    packages=['zipencrypt'],
    license_files = ('LICENSE.txt',),
)
