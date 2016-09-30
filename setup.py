from setuptools import setup

import flask_csp

setup(
  name = 'flask-csp',
  packages = ['flask_csp'],
  include_package_data = True,
  version = '0.9',
  description = 'Flask Content Security Policy header support',
  long_description = """
Add a Content Security Policy header to your Flask application. 

Mitigate the risk of cross-site scripting attacks by whitelisting trusted origins with a Content Security Policy. 
""",
  license='MIT',
  author = 'Tristan Waldear',
  author_email = 'trwaldear@gmail.com',
  url = 'https://github.com/twaldear/flask-csp',
  keywords = ['flask', 'csp', 'header'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Framework :: Flask',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ]
)
