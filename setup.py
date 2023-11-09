from setuptools import setup

setup(
    name="convex",
    version="1.0",
    scripts=["convex.py"],
    entry_points={
        "console_scripts": [
            "convex=convex:main",
        ],
    },
)
