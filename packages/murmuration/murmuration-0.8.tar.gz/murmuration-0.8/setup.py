from setuptools import setup, find_packages


version = '0.8'
with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='murmuration',
      version=version,
      description="encryption primitives for use with aws",
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'License :: OSI Approved :: BSD License',
          'Topic :: Security :: Cryptography',
          'Topic :: Utilities',
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='aws python encryption cryptography kms',
      author='Preetam Shingavi',
      author_email='p.shingavi@yahoo.com',
      url='https://github.com/angry-penguins/murmuration',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'boto3',
          'pycryptodome>=3.7.3',
      ])
