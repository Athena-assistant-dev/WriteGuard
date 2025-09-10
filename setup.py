from setuptools import setup, find_packages

setup(
    name="writeguard",
    version="0.0.2",
    author="Terry Simmons",
    author_email="your-email@example.com",
    description="Secure, versioned, and auditable file write system.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/writeguard",
    packages=find_packages(where="app/v0.0.2"),
    package_dir={"": "app/v0.0.2"},
    entry_points={
        "console_scripts": [
            "writeguard=writeguard_cli:main"
        ]
    },
    include_package_data=True,
    install_requires=[
        "flask",
        "python-dotenv",
        "pyyaml",
        "redbaron",
        "jsonpatch",
        "pillow",
        "python-docx",
        "python-pptx",
        "openpyxl",
        "ruamel.yaml"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)