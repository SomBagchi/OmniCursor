from setuptools import setup, find_packages

setup(
    name="ai-chat-assistant",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "mss>=9.0.1",
        "Pillow>=10.0.0",
        "pyobjc>=10.0.0",
        "numpy>=1.24.0",
        "pyobjc-framework-Quartz>=10.0.0"
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-mock>=3.10.0",
            "pytest-cov>=4.0.0"
        ]
    },
    python_requires=">=3.8",
) 
