from setuptools import find_packages,setup
from typing import List


HYPHEN_E_DOT="-e ."
def get_requirements(file_path:str)->List[str]:
    '''this function return the list of requrements'''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requrements=[req.replace("\n","") for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements=requirements.remove(HYPHEN_E_DOT)
    
    return requirements


setup(
    name="ForgeAi",
    version="0.0.1",
    Author="Ramakant",
    Author_email="ramakantkushwaha2006@gmail.com",
    Package=find_packages(),
    install_requires=get_requirements("requirements.txt")
    
)
