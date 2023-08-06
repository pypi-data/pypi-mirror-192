# from setuptools import setup
# setup(
#     name='sourshadow',
#     version='1.0.2',
#     author='Edmond Legaspi',
#     description='This is an example project',
#     long_description='This is a longer description for the project',
#     url='https://medium.com/@gmyrianthous',
#     keywords='sample, example, setuptools',
#     python_requires='>=3.7, <4',
#     install_requires=['pandas'],
#     # entry_points={
#     #     'runners': [
#     #         'sample=sample:main',
#     #     ]
#     # }
# )


import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sourshadow',
    version='1.0.4',
    author='Edmond Legaspi',
    author_email = "legaspi.edmond@gmail.com",
    description = "short package description",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://medium.com/@gmyrianthous",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "sourshadow"},
    packages = setuptools.find_packages(where="sourshadow"),
    python_requires = ">=3.7"
)