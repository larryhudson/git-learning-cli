from setuptools import setup, find_packages

setup(
    name="git-learning-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    py_modules=['cli'],  # Add this line
    entry_points={
        "console_scripts": [
            "git-learn=cli:cli",
        ],
    },
)
