from setuptools import setup


def get_long_description():
    with open("README.rst") as file:
        return file.read()


setup(
    name="sslcommerz-sdk",
    version="1.0.2",
    description="Sslcommerz SDK for python",
    long_description=get_long_description(),
    long_description_content_type="text/x-rst",
    url="https://github.com/monim67/sslcommerz-sdk",
    author="Munim Munna",
    author_email="6266677+monim67@users.noreply.github.com",
    license="MIT",
    keywords="sslcommerz python sdk",
    packages=[
        "sslcommerz_sdk",
        "sslcommerz_sdk.contrib.django_app",
        "sslcommerz_sdk.contrib.django_app.migrations",
        "sslcommerz_sdk.orm_adapters",
    ],
    install_requires=[
        "requests>=2.22",
        "marshmallow>=3.0.0",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
    ],
)
