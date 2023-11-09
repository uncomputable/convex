from setuptools import setup

setup(
    name="convex",
    version="0.1",
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "convex=main:main",
        ],
    },
)
