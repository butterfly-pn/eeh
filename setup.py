"""Info about the aplication"""

from setuptools import setup

setup(name='EEH',
      version="0.1.0",
      description="Elektroniczna ewidencja harcerzy",
      author="Patryk Niedźwiedziński <pniedzwiedzinski19@gmail.com>",
      install_requires=['flask', 'flask-login', 'flask-sqlalchemy', 'flask-mail', 'uwsgi']
      )
