from distutils.core import setup

setup(
    name='toxopy',
    packages=['toxopy'],
    version='0.6.3',
    license='MIT',
    description='Object-specific python package to run automated tasks in the Chase Lab.',
    author='fcatus',
    author_email='f.catus@pm.me',
    url='https://github.com/bchaselab/toxopy',
    download_url='https://github.com/bchaselab/Toxopy/archive/0.6.2.tar.gz',
    install_requires=["pandas", "dlcu", "numpy", "tqdm", "scipy",
                      "matplotlib", "seaborn", "rich", "dirtyR", "rdp", "pca"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
