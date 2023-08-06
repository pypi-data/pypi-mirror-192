from setuptools import setup
import subprocess


def get_version():
    # If a VERSION.txt exists, we use its content as version number.
    try:
        with open('VERSION.txt', 'r') as version_file:
            return version_file.read()
    except IOError:
        print("Using git hash")

    # Else we're a git-build, so we use the git hash.
    # Format it to be PEP440 compliant for pip/wheel compatibility.
    gitTag = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').strip()
    return "9999.dev0+git{:s}".format(gitTag)


setup(name='dv',
      version=get_version(),
      description='Library to connect to DV event based vision software',
      url='https://gitlab.com/inivation/dv/dv-python/',
      author='iniVation AG',
      author_email='support@inivation.com',
      license='AGPLv3',
      packages=['dv', 'dv.fb'],
      install_requires=['flatbuffers', 'numpy', 'lz4', 'zstd', 'deprecated'],
      python_requires='>=3',
      zip_safe=False)
