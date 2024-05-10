from setuptools import setup

setup(
    name="convex",
    version="1.2",
    py_modules=["convex"],
    entry_points={
        "console_scripts": [
            "convex=convex:main",
        ],
    },
)
