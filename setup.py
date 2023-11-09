from setuptools import setup

setup(
    name="convex",
    version="1.0",
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "convex=main:main",
        ],
    },
)
