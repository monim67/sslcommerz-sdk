from setuptools import setup


def get_long_description():
    with open("README.md") as file:
        return file.read()


setup(
    name="sslcommerz-sdk",
    version="1.0.0",
    description="Sslcommerz SDK for python",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/monim67/sslcommerz-sdk",
    author="Munim Munna",
    author_email="monim67@yahoo.com",
    license="MIT",
    keywords="sslcommerz",
    packages=["sslcommerz_sdk"],
    install_requires=["requests>=2.20"],
    python_requires=">=3",
    classifiers=[
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
    ],
)
