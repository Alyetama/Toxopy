from distutils.core import setup

setup(
    name='toxopy',
    packages=['toxopy'],
    version='0.6.4',
    license='MIT',
    description='Object-specific python package to run automated tasks in the Chase Lab.',
    author='fcatus',
    author_email='f.catus@pm.me',
    url='https://github.com/bchaselab/toxopy',
    install_requires=["pandas", "dlcu", "numpy", "tqdm", "scipy",
                      "matplotlib", "seaborn", "rich", "dirtyR", "rdp", "pca"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
