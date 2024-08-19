from setuptools import setup, find_packages

setup(
    name="budanov_blacklist",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "colorama==0.4.6",
        "prompt_toolkit==3.0.47",
        "wcwidth==0.2.13",
    ],
    entry_points={
        'console_scripts': [
            'run-bot=budanov_blacklist.main:main',
        ],
    },
    author="project_team_01",
    author_email="project_team_01@gmail.com",
    description="Budanov bot",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shulc0690/AddressBook_Bot_Neoversity",
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
