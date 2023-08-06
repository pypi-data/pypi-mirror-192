from setuptools import setup, find_packages


setup(
    name='cfnpipeline',
    version='0.0.3',
    license='MIT',
    author="Stealthy",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='example project',
    install_requires=[
          'scikit-learn',
      ],

)
