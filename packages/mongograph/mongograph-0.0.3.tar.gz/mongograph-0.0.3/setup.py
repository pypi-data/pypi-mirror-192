from setuptools import setup
with open("README.md", "r") as file:
    long_description = file.read()

setup(name='mongograph',
        version='0.0.3',
        author='Abhishek Pawaskar',
        description='Build Graphs On MongoDB Easily',
        long_description='Conduct CRUD operations on Graph DataBase on Top of MongoDB',
        long_description_content_type='text/markdown',
        url='https://github.com/AbhishekPawaskar/MongoGraph',
        keywords='mongograph,grepheasy, graph_easy, GRAPH_EASY',
        python_requires=">=3.10",
        platforms=["Windows", "Linux"],
        install_requires=['pymongo==4.3.3','dnspython==2.3.0'],
        packages=['mongograph','mongograph.mongo_wrapper'],
        setup_requires=['wheel'])