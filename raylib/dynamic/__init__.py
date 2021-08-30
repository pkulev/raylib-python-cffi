"""
This is an attempt at a CFFI dynamic (ABI) binding.  It was failing in the exactly same place the ctypes binding fails, accessing
materials of a model.  But now it __seems__ to work
"""

#  Copyright (c) 2021 Richard Smith and others
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0.
#
#  This Source Code may also be made available under the following Secondary
#  licenses when the conditions for such availability set forth in the Eclipse
#  Public License, v. 2.0 are satisfied: GNU General Public License, version 2
#  with the GNU Classpath Exception which is
#  available at https://www.gnu.org/software/classpath/license.html.
#
#  SPDX-License-Identifier: EPL-2.0 OR GPL-2.0 WITH Classpath-exception-2.0

from cffi import FFI
import itertools
import os
import pathlib
import platform

MODULE = pathlib.Path(__file__).parent.parent

def raylib_library_path():
    '''Return the full path of the raylib shared library
    If the environment variable "USE_EXTERNAL_RAYLIB" is set (no value required)
    then the library will be loaded from the system library paths.
    '''
    def so_path():
        return str(MODULE / 'dynamic') if not 'USE_EXTERNAL_RAYLIB' in os.environ else ''
    def so_name():
        '''Returns the appropriate for the library on the current platform.'''
        lib_filenames = {
            'Windows': 'libraylib.dll',
            'Linux': 'libraylib.so',
            'Darwin': 'libraylib.dylib',
        }
        if platform.system() not in lib_filenames:
            raise ValueError('Unrecognised system "{}"'.format(platform.system()))
        return lib_filenames.get(platform.system())

    return os.path.join(so_path(), so_name())


ffi = FFI()
ffi.cdef(open(MODULE / "raylib_modified.h").read().replace('RLAPI ', ''))

try:
    raylib_fname = raylib_library_path()
    raylib = ffi.dlopen(raylib_fname)
    print('LOADED DYNAMICALLY SHARED LIB "{}"'.format(raylib_fname))
except Exception as e:
    print(e)
