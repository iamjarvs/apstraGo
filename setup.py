from setuptools import setup
from setuptools import find_packages

setup(
    name='apstraGo',
    version='1.1.0',
    description='Python wrapper for Apstra OS',
    author='Adam Jarvis',
    url='https://github.com/iamjarvs/apstraGo',
    install_requires=['requests', 'PyYAML', 'cerberus', 'rich'],
    keywords='apstra juniper',
    packages=['apstraGo'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
    package_data={
        'apstraGo': ['data/*.py'],
    },
    entry_points={
        'console_scripts': [
            'apstraGo-auto = apstraGo.apstraGoAuto:main',
            'apstraGo-yaml = apstraGo.apstraGoYaml:main'
        ]      
    }
)
