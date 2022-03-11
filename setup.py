import setuptools
import re

# versioning ------------
VERSIONFILE="benfordslaw/__init__.py"
getversion = re.search( r"^__version__ = ['\"]([^'\"]*)['\"]", open(VERSIONFILE, "rt").read(), re.M)
if getversion:
    new_version = getversion.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

# Setup ------------
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     install_requires=['matplotlib','numpy','scipy','pandas','wget'],
     python_requires='>=3',
     name='benfordslaw',
     version=new_version,
     author="Erdogan Taskesen",
     author_email="erdogant@gmail.com",
     description="benfordslaw is to test if an empirical (observed) distribution differs significantly from a theoretical (expected, Benfords) distribution.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://erdogant.github.io/benfordslaw",
	 download_url = 'https://github.com/erdogant/benfordslaw/archive/'+new_version+'.tar.gz',
     packages=setuptools.find_packages(), # Searches throughout all dirs for files to include
     include_package_data=True, # Must be true to include files depicted in MANIFEST.in
     license_files=["LICENSE"],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
