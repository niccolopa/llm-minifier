from setuptools import setup

setup(
    name="llm-minifier",
    version="1.0.0",
    py_modules=["llm_minifier", "cli"],
    entry_points={
        "console_scripts": [
            "llm-minify=cli:main",
        ],
    },
)