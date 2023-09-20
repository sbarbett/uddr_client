from setuptools import setup, find_packages

setup(
    name="uddr_client", 
    version="0.2.5",  
    description="A Python client for the UDDR API.", 
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown', 
    author="Shane Barbetta", 
    author_email="shane@barbetta.me",  
    url="https://github.com/sbarbett/uddr_client", 
    license="MIT", 
    classifiers=[ 
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    package_dir={"": "src"},  
    packages=find_packages(where="src"),  
    python_requires=">=3.7", 
    install_requires=[
        "pandas>=2.0.2",
        "xmltodict>=0.13.0",
        "python-decouple>=3.8",
        "requests>=2.25.1",
    ],
)
