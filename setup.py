from setuptools import setup, find_packages

setup (
    name='Bluetooth-Shiny-Bot',
    version='0.1',
    description='Emulate a switch pro-controller over bluetooth to hunt for select shiny pokemon',
    packages=find_packages(),
    install_requires=['matplotlib', 'numpy', 'nxbt', 'opencv-python']
)