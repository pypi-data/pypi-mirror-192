from setuptools import setup, find_packages
import os

with open('README.md') as readme_file:
    README = readme_file.read()


setup_args = dict(
    name='torch-model-compression',
    version='0.1.2',
    description='Model Compression',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n',
    license='MIT',
    packages=find_packages(),
    author='Sathyaprakash',
    author_email='snaray17@ucsc.edu',
    keywords=['Pruning', 'Compression', 'Model Pruning'],
    url='https://github.com/satabios/tomoco',
    download_url='https://pypi.org/project/tomoco/'
)


if __name__ == '__main__':
    lib_folder = os.path.dirname(os.path.realpath(__file__))
    requirement_path = lib_folder + './requirements.txt'
    install_requires = []

    if os.path.isfile(requirement_path):
        with open(requirement_path) as f:
            install_requires = f.read().splitlines()
    print(install_requires)
    setup(name="torch-model-compression", install_requires=install_requires)