# Setuptools must go above distutils
# https://stackoverflow.com/a/53356077/5332072
from setuptools.command.install import install

import distutils.command.install as orig
from distutils.command.build import build
from distutils.core import Extension, setup



# Customize installation according to https://stackoverflow.com/a/21236111
class CustomBuild(build):
    def run(self):
        self.run_command("build_ext")
        build.run(self)


class CustomInstall(install):
    def run(self):
        self.run_command("build_ext")
        orig.install.run(self)


include_dirs = ["./include"]
extra_compile_args = ["-O2", "-std=c++11"]
# extra_compile_args = ['-g', '-std=c++11', '-O0', '-Wall']


extensions = [
    Extension(
        name="pyrfr._regression",
        sources=["pyrfr/regression.i"],
        include_dirs=include_dirs,
        swig_opts=["-c++", "-modern", "-py3", "-features", "nondynamic"]
        + ["-I{}".format(s) for s in include_dirs],
        extra_compile_args=extra_compile_args,
    ),
    Extension(
        name="pyrfr._util",
        sources=["pyrfr/util.i"],
        include_dirs=include_dirs,
        swig_opts=["-c++", "-modern", "-py3", "-features", "nondynamic"]
        + ["-I{}".format(s) for s in include_dirs],
        extra_compile_args=extra_compile_args,
    ),
]

print(extensions)

setup(
    name="pyrfr",
    version="0.9.0",
    author="Stefan Falkner, Matthias Feurer, Rene Sass, Eddie Bergman",
    author_email="sfalkner@cs.uni-freiburg.de",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
    ],
    packages=["pyrfr"],
    ext_modules=extensions,
    python_requires=">=3.7",
    package_data={"pyrfr": ["docstrings.i"]},
    py_modules=["pyrfr"],
    cmdclass={"build": CustomBuild, "install": CustomInstall},
    long_description="# Pyrfr\nhttps://github.com/automl/random_forest_run",
    long_description_content_type="text/markdown",
    url="https://github.com/automl/random_forest_run",
)
