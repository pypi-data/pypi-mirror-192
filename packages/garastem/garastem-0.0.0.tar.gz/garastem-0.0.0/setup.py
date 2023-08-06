from setuptools import setup, find_packages
with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='garastem',
    version='0.0.0',
    description='GaraSTEM Library',
    # long_description_content_type="text/markdown",
    # long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
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

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)