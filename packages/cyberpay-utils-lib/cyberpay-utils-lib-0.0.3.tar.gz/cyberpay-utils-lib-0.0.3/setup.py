from setuptools import find_packages, setup

setup(
    name="cyberpay-utils-lib",
    version="0.0.3",
    description="Cyberpay utils library",
    author="MADI SPACE",
    license="MIT",
    packages=find_packages(where="cyberpay_utils"),
    package_dir={"": "cyberpay_utils"},
    package_data={
        "cyberpay_utils.billing.proto": ["*.proto", "*.pyi"],
    },
    zip_safe=False,
)
