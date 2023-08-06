from distutils.core import setup, Extension
setup(name='VectorizeList',
      version='1.0',
      ext_modules = [Extension('VectorizeList', ['VectorizeList.c'])],
      license="GNU3",
      description="Vectorize a list of strings into ints",
      author="Julien Calenge",
      author_email="julien.calenge@epitech.eu",
      url="https://github.com/jclge/VectorizeList",
      )
