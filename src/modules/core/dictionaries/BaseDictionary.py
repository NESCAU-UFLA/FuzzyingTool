## FuzzingTool
# 
# Authors:
#    Vitor Oriel C N Borges <https://github.com/VitorOriel>
# License: MIT (LICENSE.md)
#    Copyright (c) 2021 Vitor Oriel
#    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
## https://github.com/NESCAU-UFLA/FuzzingTool

from .Payloader import Payloader

from queue import Queue

class BaseDictionary(Payloader):
    """Class that handles with the program dictionary

    Attributes:
        payloads: The queue that contains all payloads inside the wordlist
        wordlist: The wordlist that contains the payloads backup
    """
    def __init__(self):
        """Class constructor"""
        super().__init__()
        self.__payloads = Queue()
        self._wordlist = []

    def __next__(self):
        """Gets the payload list ajusted with the console options

        @returns list: The payloads used in the request
        """
        ajustedPayload = [self.__payloads.get()]
        if self._prefix:
            ajustedPayload = [(prefix+payload) for prefix in self._prefix for payload in ajustedPayload]
        if self._suffix:
            ajustedPayload = [(payload+suffix) for suffix in self._suffix for payload in ajustedPayload]
        if self._uppercase:
            ajustedPayload = [payload.upper() for payload in ajustedPayload]
        elif self._lowercase:
            ajustedPayload = [payload.lower() for payload in ajustedPayload]
        elif self._capitalize:
            ajustedPayload = [payload.capitalize() for payload in ajustedPayload]
        return ajustedPayload
    
    def __len__(self):
        """Gets the wordlist length

        @returns int: The wordlist length
        """
        return len(self._wordlist)

    def isEmpty(self):
        """The payloads empty queue flag getter

        @returns bool: The payloads empty queue flag
        """
        return self.__payloads.empty()

    def reload(self):
        """Reloads the payloads queue with the wordlist content"""
        self.__payloads = Queue()
        for payload in self._wordlist:
            self.__payloads.put(payload)

    def setWordlist(self, sourceParam: str):
        """The wordlist setter

        @type sourceParam: str
        @param sourceParam: The source string of the wordlist
        """
        raise NotImplementedError("setWordlist method should be overrided")