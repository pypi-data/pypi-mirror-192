from setuptools import setup
from setuptools import find_packages


setup(
    name='humai_internal_tools',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'mercadopago',
        'requests',
        'unidecode',
        'pydantic',
        'python-dotenv'
    ],
    author='Humai Dev Team',
    author_email='perez.moleroc@gmail.com',
    description='Internal tools for private usage.',
    long_description_content_type="text/markdown",
    long_description="",
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
