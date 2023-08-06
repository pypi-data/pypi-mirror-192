from setuptools import setup, find_packages

setup(
    name='mr_encryption',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'Pillow==8.3.2',
        'click==8.0.1',
    ],
    entry_points={
        'console_scripts': [
            'mr-encrypt=mr_encryption.cli:encrypt',
            'mr-decrypt=mr_encryption.cli:decrypt',
        ],
    },
)
