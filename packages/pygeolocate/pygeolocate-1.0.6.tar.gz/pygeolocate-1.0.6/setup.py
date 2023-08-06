from setuptools import setup, find_packages

VERSION = '1.0.6'
DESCRIPTION = 'An easy way to find a countries coordinates by name'
LONG_DESCRIPTION = 'An easy way to find a countries coordinates by name'

setup(
    name="pygeolocate",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Isabelle",
    author_email="scrumpy@weeb.email",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='location, geolocation, geolocate',
    classifiers= [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)