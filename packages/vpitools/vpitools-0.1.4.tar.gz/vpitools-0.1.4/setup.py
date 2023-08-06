from setuptools import setup, find_packages
setup(
    name='vpitools',
    version='0.1.4',
    description='Updated Curves View Function',
    url='https://vpi.pvn.vn/',
    author='DnA Teams',
    author_email='dna.teams@vpi.pvn.vn',
    license='MIT',
    # packages=['vpitools'],
    packages=find_packages(), include_package_data=True,
    zip_safe=False,
    install_requires=['matplotlib', 'seaborn', 'plotly', 'altair', 
                      'numpy', 'pandas',
                      ]
)
