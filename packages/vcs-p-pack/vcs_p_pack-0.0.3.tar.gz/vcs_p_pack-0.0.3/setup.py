from setuptools import setup, find_packages

setup(
    name='vcs_p_pack',
    version='0.0.3',
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'parse_work=package.vcs_p:parse_work'
        ]
    },
    package_dir={"": "package"},
    packages=find_packages(where="package"),
)
