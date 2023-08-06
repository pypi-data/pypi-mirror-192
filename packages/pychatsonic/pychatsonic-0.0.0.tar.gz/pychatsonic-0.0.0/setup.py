from setuptools import setup

setup(name='pychatsonic',
      description='Python adapter for chatsonic api',
      packages=['pychatsonic'],
      author_email='weirdoo145@gmail.com',
      zip_safe=False,
      requires=["requests"],
      long_description="./readme.md")