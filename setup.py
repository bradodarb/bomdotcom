from setuptools import setup, find_packages

setup(name='bomdotcom',
      version='1.0.0',
      description='Parses CSV data into dtructured data and ranks results',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3'
      ],
      keywords='dict list path dot notation',
      author='Brad Murry',
      author_email="bmurryrrumb@gmail.com",
      license='MIT',
      packages=find_packages(exclude=['test*']),
      include_package_data=True,
      package_dir={'.': ''},
      install_requires=[
          'structlog == 18.2.0',
          'python-json-logger == 0.1.9'
      ],
      zip_safe=False)
