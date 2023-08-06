from setuptools import setup, find_packages
# 若Discription.md中有中文 須加上 encoding="utf-8"
#with open("Discription.md", "r",encoding="utf-8") as f:
#    long_description = f.read()
    
setup(
    name = "peiapi",
    version = "0.0.3",
    author = "pei-jan",
    author_email="orangepower856@hotmail.com",
    description="call trade function",
    packages=find_packages(),
    #license=
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    #url="https://github.com/seanbbear/VerdictCut",                                         packages=setuptools.find_packages(),     
    #classifiers=[
    #    "Programming Language :: Python :: 3",
    #    "License :: OSI Approved :: MIT License",
    #    "Operating System :: OS Independent",
    #],
    #python_requires='>=3.6'
    )