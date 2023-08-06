from setuptools import setup, find_packages

setup(
    name='pycodegrade',
    version='0.0.1',
    description='PYPI pycodegrade for Python',
    author='teddylee777',
    author_email='teddylee777@gmail.com',
    url='https://github.com/teddylee777/pycodegrade',
    install_requires=['pyairtable', 'pandas', 'scikit-learn', 'matplotlib', 'seaborn'],
    packages=find_packages(exclude=[]),
    keywords=['pycodegrade', 'codegrade', 'python'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)