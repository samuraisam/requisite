import sys, os
from setuptools import setup

version = "0.1.3"

setup(name='requisite',
      version=version,
      description='Requisite downloads python packages from a requirements.txt '
                  'file and uploads them to your private PyPI server',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools'
      ],
      keywords='easy_install distutils setuptools egg virtualenv pip',
      author='Samuel Sutch',
      author_email='sam@altertap.com',
      url='http://github.com/samuraisam/requisite',
      license='MIT',
      packages=['requisite','requisite.scripts'],
      install_requires=['pip'],
      entry_points=dict(console_scripts=['req=requisite:main', 'req-%s=requisite:main' % sys.version[:3]]),
      zip_safe=False)
