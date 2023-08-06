
__author__="Abhishek Pawaskar"
from setuptools import setup

def description_reader():
    with open("README.md", "r") as file:
        return file.read()

setup(name='mongograph',
        version='0.0.4',
        author='Abhishek Pawaskar',
        author_email="Abhishek99rp@gmail.com",
        description='Build Graphs On MongoDB Easily',
        long_description=description_reader(),
        long_description_content_type='text/markdown',
        url='https://github.com/AbhishekPawaskar/MongoGraph.git',
        keywords='mongograph, grepheasy, graph_easy, GRAPH_EASY',
        python_requires=">=3.10",
        platforms=["Windows", "Linux"],
        install_requires=['pymongo==4.3.3','dnspython==2.3.0'],
        packages=['mongograph','mongograph.mongo_wrapper'],
        setup_requires=['wheel'],
        classifiers=['Development Status :: 4 - Beta', 
                     'License :: OSI Approved :: Apache Software License', 
                     'Programming Language :: Python :: 3.10', 
                     'Topic :: Database :: Database Engines/Servers'],
        include_package_data=True)