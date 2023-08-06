"""The setup script."""

from setuptools import setup, find_packages
import os


requirements = ['pandas', 'urllib3', 'bs4', 'selenium',
                'webdriver_manager', 'numpy']


setup(
    author="Lucas Abreu",
    author_email='lucasabreu@me.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="extract all the data like: price, address, features from imovelweb.com.br",
    install_requires=requirements,
    include_package_data=True,
    keywords='real_state_scrap',
    name='Scrap_realstate',
    packages=find_packages(include=['realstate_scrap', 'realstate_scrap.*']),
    version='0.1.0',
)
