from setuptools import setup, find_packages

setup(
    name="writeguard_langchain",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests", "langchain>=0.0.300"],
    author="Terry Simmons",
    description="LangChain tool wrapper for WriteGuard secure write API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/writeguard",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)