from setuptools import setup, find_packages
import os

version = '1.2'

setup(name='actionbar.panel',
      version=version,
      description="Provides a (old) facebook style action panel at the bottom of your  Plone site",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone panel actionbar',
      author='JC Brand, Syslab.com GmbH',
      author_email='brand@syslab.com',
      url='http://plone.org/products/actionbar.panel',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['actionbar'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
