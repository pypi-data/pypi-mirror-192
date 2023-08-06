from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='mongograph',
        version='0.0.2',
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