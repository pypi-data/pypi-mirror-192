from setuptools import setup, find_packages

setup(
    name='vcs_p_pack',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'parse_work = package.vcs_p:parse_work',
        ],
    },
    install_requires=[
        'psutil == 5.9.4',
        'setuptools == 56.0.0'
    ],
)
