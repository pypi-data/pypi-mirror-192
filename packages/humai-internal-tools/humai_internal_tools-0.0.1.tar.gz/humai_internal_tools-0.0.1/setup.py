from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Internal tools for private usage.'

setup(
    name='humai_internal_tools',
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'mercadopago',
        'requests',
        'unidecode',
        'pydantic',
        'dotenv'
    ],
    author='Humai Dev Team',
    author_email='perez.moleroc@gmail.com',
    description=DESCRIPTION,
    url='https://github.com/institutohumai/humai_internal_tools',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
