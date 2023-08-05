from setuptools import setup, find_packages

setup(
    name='PySubdiv',
    version='0.0.0',
    packages=find_packages(),
    install_requires=['pyvista==0.36.1',
                      'jedi>=0.18.2',
                      'networkx>=2.6.3',
                      'numpy>=1.21.4',
                      'QtPy~=2.0.0',
                      'PyQt5~=5.15.6',
                      'vtk~=9.2.2',
                      'scipy>=1.7.2',
                      'pyvistaqt~=0.9.0',
                      'easygui~=0.98.3',
                      'pymeshlab==2022.2.post2',
                      'meshio',
                      'pyswarms>=1.3.0'],
    long_description='file : README.md',
    url='',
    include_package_data=True,
    license='GNU',
    author='Simon Bernard,  S. Mohammad Moulaeifard, Mosaku Adeniyi',
    author_email='simon.bernard@rwth-aachen.de, Mohammad.Moulaeifard@cgre.rwth-aachen.de, adeniyi.mosaku@rwth-aachen.d',
    description='An Open-source, Python-based software for fitting subdivision surfaces'
)
