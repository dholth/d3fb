import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['pyramid', 'pyramid_debugtoolbar', 'ewsclient']

setup(name='d3fb',
      version='0.0',
      description='Render Exhange free/busy information with d3.js',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Daniel Holth',
      author_email='dholth@gmail.com',
      url='http://bitbucket.org/dholth/d3fb',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="d3fb",
      entry_points = """\
      [paste.app_factory]
      main = d3fb:main
      """,
      paster_plugins=['pyramid'],
      )

