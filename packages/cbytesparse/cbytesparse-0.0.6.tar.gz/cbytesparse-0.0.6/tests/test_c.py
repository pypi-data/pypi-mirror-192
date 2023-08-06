# Copyright (c) 2020-2023, Andrea Zoppi.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import importlib
import inspect
import sys
from typing import Type

import pytest
from _buffers import *
from _common import *

# noinspection PyUnresolvedReferences
from cbytesparse.c import BytesMethods as _BytesMethods  # isort:skip
# noinspection PyUnresolvedReferences
from cbytesparse.c import InplaceView as _InplaceView  # isort:skip
# noinspection PyUnresolvedReferences
from cbytesparse.c import Memory as _Memory  # isort:skip
# noinspection PyUnresolvedReferences
from cbytesparse.c import bytesparse as _bytesparse  # isort:skip


# Patch inspect.isfunction() to allow Cython functions to be discovered
def _patch_inspect_isfunction():  # pragma: no cover
    isfunction_ = inspect.isfunction

    def isfunction(obj):
        return (isfunction_(obj)
                or type(obj).__name__ == 'cython_function_or_method')

    isfunction.isfunction_ = isfunction_
    inspect.isfunction = isfunction


_patch_inspect_isfunction()


def _load_cython_tests():  # pragma: no cover
    # List of Cython modules containing tests
    cython_test_modules = ['_test_c']

    for mod in cython_test_modules:
        try:
            # For each callable in `mod` with name `test_*`,
            # set the result as an attribute of this module.
            mod = importlib.import_module(mod)

            for name in dir(mod):
                item = getattr(mod, name)

                if callable(item) and name.startswith('test_'):
                    setattr(sys.modules[__name__], name, item)

        except ImportError:
            pass


_load_cython_tests()


class TestBytesMethods(BytesMethodsSuite):
    BytesMethods: Type['_BytesMethods'] = _BytesMethods


class TestInplaceView(InplaceViewSuite):
    BytesMethods: Type['_InplaceView'] = _InplaceView


class TestMemory(BaseMemorySuite):
    Memory: Type['_Memory'] = _Memory
    ADDR_NEG: bool = False

    def test___sizeof__(self):
        Memory = self.Memory
        memory = Memory.from_blocks([[1, b'AB'], [5, b'x'], [7, b'123']])
        assert memory.__sizeof__() > 0
        assert memory.__sizeof__() > 6


class TestBytesparse(BaseBytearraySuite, BaseMemorySuite):
    bytesparse: Type['_bytesparse'] = _bytesparse

    # Reuse some of BaseMemorySuite methods
    Memory: Type['_Memory'] = _bytesparse
    ADDR_NEG: bool = False
