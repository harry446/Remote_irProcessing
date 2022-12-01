from distutils.core import setup, Extension


def main():
    setup(name="irProcessing",
          version="1.0.0",
          description="Python interface for irProcessing",
          author="Joe Yu",
          author_email="j56yu@uwaterloo.ca",
          ext_modules=[Extension("irProcessing", ["irProcessing.c", "wiipointer.c"], ['./'])])


if __name__ == "__main__":
    main()
