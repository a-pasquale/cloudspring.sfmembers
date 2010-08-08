from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='cloudspring.sfmembers',
      version=version,
      description="A project to synchronize SalesForce accounts and contacts with Plone.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Andrew Pasquale',
      author_email='andrew@elytra.net',
      url='https://cloudspring.svn.beanstalkapp.com/cloudspring_sfmembers/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['cloudspring'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'plone.app.dexterity',
          'collective.autopermission',
          'plone.app.z3cform',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
