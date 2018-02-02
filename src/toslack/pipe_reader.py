# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
# Copyright (c) 2018 Taro Sato
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import time
from queue import Empty
from queue import Queue
from threading import Thread


class PipeReader:
    """Non-blocking pipe reader."""

    def __init__(self):
        self._finished = False
        self._start()

    def _start(self):
        self._queue = Queue()
        t = Thread(target=self._enqueue_output,
                   args=(sys.stdin, self._queue))
        t.daemon = True
        t.start()

    def _enqueue_output(self, out, queue):
        for line in iter(out.readline, ''):
            queue.put(line)
        out.close()
        self._finished = True

    def read(self, wait=3):
        """Read from pipe.

        Args:
            wait (float): Wait in seconds before quit when nothing is
                read from pipe.

        Returns:
            unicode: Text read from pipe.

        """
        last_read = time.time()
        out = ''
        while 1:
            time.sleep(0)
            try:
                line = self._queue.get_nowait()
            except Empty:
                t = time.time()
                if self._finished or t - last_read > wait:
                    break
                else:
                    continue
            else:
                out += line
                last_read = time.time()
        return out
