from setuptools import setup

setup(
    name="convex",
    version="1.1",
    scripts=["convex.py"],
    entry_points={
        "console_scripts": [
            "convex=convex:main",
        ],
    },
)
