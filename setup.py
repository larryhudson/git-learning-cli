from setuptools import setup, find_packages

setup(
    name="git-learning-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    py_modules=['cli', 'git_commands', 'completed_scenarios'],
    package_data={
        'scenarios': ['*.py'],
    },
    entry_points={
        "console_scripts": [
            "git-learn=cli:cli",
        ],
    },
)
