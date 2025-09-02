from setuptools import setup

setup(
    name='industrious',
    version='0.0.2',
    description='A random assortment of utilities based around my personal stack workflow',
    url='https://github.com/hell-of-the-devil/industrious',
    author='Hell of the Devil',
    author_email='me@hell-of-the-devil.me',
    license='BSD 2-clause',
    packages=['industrious'],
    install_requires=[
        "rich"
    ],

    classifiers=[
        'Development Status :: 2 - Core functionality implementation',
        'Operating System :: POSIX :: Linux :: Windows',
        'Programming Language :: Python :: 3+',
    ],
)