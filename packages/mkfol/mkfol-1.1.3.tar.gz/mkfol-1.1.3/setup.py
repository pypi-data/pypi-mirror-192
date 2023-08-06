import setuptools
setuptools.setup(
    name='mkfol',
    version='1.1.3',
    packages=["mkfol"],
    entry_points={
        'console_scripts': ['mkfol=mkfol.mkfol:mkfol']
    },
    author='Sulthan Abiyyu Hakim',
    author_email="sabiyyuhakim@student.ub.ac.id",
    description='Folder maker based on template',
    install_requires=[
        'setuptools',
    ],
    python_requires='>=3.5',
)
