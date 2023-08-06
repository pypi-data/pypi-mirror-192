from setuptools import setup, find_packages
with open('garastem/README.md') as readme_file:
    README = readme_file.read()

with open('garastem/HISTORY.md') as history_file:
    HISTORY = history_file.read()

import time
setup_args = dict(
    name='garastem',
    version='0.0.{}'.format(int(time.time())),
    description='GaraSTEM Library',
    # long_description_content_type="text/markdown",
    # long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=['garastem'],
    author='Curly Nguyen',
    author_email='curly.saigonese@gmail.com',
    keywords=['GaraSTEM', 'GRobot', 'GIoT'],
    url='https://github.com/curlyz/garastem',
    download_url='https://pypi.org/project/garastem/'
)

install_requires = [
    'bleak',
    'termcolor'
]

print("find_packages()", find_packages())

import os
if __name__ == '__main__':
    os.system('rm -rf dist')
    setup(**setup_args, install_requires=install_requires)