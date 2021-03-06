# Copyright (c) 2021 Vitor Oriel <https://github.com/VitorOriel>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

def plugin_meta(cls):
    metadata = ['__author__', '__params__', '__desc__', '__type__', '__version__']
    classAttr = vars(cls)
    for meta in metadata:
        if meta not in classAttr:
            raise Exception(f"Metadata {meta} not specified in plugin {cls.__name__}")
    if not cls.__author__:
        raise Exception(f"Author cannot be empty on plugin {cls.__name__}")
    if cls.__params__:
        if not (type(cls.__params__) is dict):
            raise Exception(f"The parameters must be a dictionary on plugin {cls.__name__}")
        paramDictKeys = cls.__params__.keys()
        for key in ['metavar', 'type']:
            if key not in paramDictKeys:
                raise Exception(f"Key {key} must be in parameters dict on plugin {cls.__name__}")
            if not cls.__params__[key]:
                raise Exception(f"Value of {key} cannot be empty in parameters dict on plugin {cls.__name__}")
        if cls.__params__['type'] is list:
            if 'cli_list_separator' not in paramDictKeys:
                raise Exception(f"The key 'cli_list_separator' must be present when parameter type is list on plugin {cls.__name__}")
            if not cls.__params__['cli_list_separator']:
                raise Exception(f"Value of 'cli_list_separator' cannot be blank on {cls.__name__}")
    if not cls.__desc__:
        raise Exception(f"Description cannot be blank on plugin {cls.__name__}")
    if not cls.__version__:
        raise Exception(f"Version cannot be blank on plugin {cls.__name__}")
    return cls