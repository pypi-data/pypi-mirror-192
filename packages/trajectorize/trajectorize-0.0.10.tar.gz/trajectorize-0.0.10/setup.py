#!/usr/bin/env python

from pathlib import PurePath
from setuptools import setup

if __name__ == "__main__":
    # Make a relative path for the cffi module
    ext_dir = PurePath("src", "trajectorize", "c_ext_utils",
                       "build_c_extension.py:ffi")
    setup(cffi_modules=[str(ext_dir)])
