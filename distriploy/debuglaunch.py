#!/usr/bin/env python
# -*- coding: utf-8 vi:et
#
# Caller to be able to debug the module via Pycharm
# source: https://stackoverflow.com/questions/28955520/intellij-pycharm-cant-debug-python-modules

import sys
import os
import runpy
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
runpy.run_module('distriploy', run_name="__main__", alter_sys=True)