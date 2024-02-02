from setuptools import find_packages,setup
from typing import List

HYPHN_E_DOT ='-e .'
def get_requirements(file_path:str)->List[str]:
   '''
   this function  will return list of requirement packages 
   '''
   requirements=[]
   with open(file_path) as file_obj:
      requirements=file_obj.readlines()
      requirements=[req.replace("\n"," ")for req in requirements]

      if HYPHN_E_DOT in requirements:
         requirements.remove(HYPHN_E_DOT)


   return requirements

setup(
name='MlProject',
version='0.0.1',
author='Suvarna',
packages= find_packages(),
install_requires=get_requirements('requirements.txt')


)