from setuptools import setup, find_packages
import os


HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as f:
    readme = f.read()

requirements = list()
with open(os.path.join(HERE, 'requirements.txt')) as f:
    for line in f:
        line = line.strip()
        if not line.startswith('#'):
            requirements.append(line)


setup(
    name='elPlan-prueba-despliegues',
    version='0.1.0',
    description='testing welcome student app',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    test_suite="tests",
    entry_points={
        'console_scripts': ['welcome = src.app:main']
    }
)
