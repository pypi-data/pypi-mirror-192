from setuptools import setup, find_packages

setup(
    name='vcs_p_pack',
    version='0.0.4',
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'parse_work=vcs_pack.vcs_p:parse_work'
        ]
    },
    package_dir={"": "vcs_pack"},
    packages=find_packages(where="vcs_pack"),
)
