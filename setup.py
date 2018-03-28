from setuptools import setup


with open('README.rst') as f:
    readme = f.read()

setup(
    name='zipencrypt',
    version='0.1.3',
    description='Encryption for zipfile',
    long_description=readme,
    url='https://github.com/norcuni/zipencrypt',
    author='Jonathan Koch',
    author_email='devthat@mailbox.org',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
    keywords='zipfile encryption zip password write writestr',
    packages=['zipencrypt'],
)
