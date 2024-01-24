#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2023 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import socket
from pymeasure.adapters import Adapter


class UDPAdapter(Adapter):
    """ Adapter class to support the UDP networking protocol.
    """

    def __init__(self, resource_name, preprocess_reply=None, log=None, **kwargs):
        """ Initialize the UDP adapter.

        :param resource_name: String value in the format: 'IP::PORT'
        """
        super().__init__(preprocess_reply=preprocess_reply, log=log)
        self.resource_name = resource_name
        self.ip, port = self.resource_name.split('::')
        self.port = int(port)
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _write_bytes(self, content, **kwargs):
        self.connection.sendto(content, (self.ip, self.port))

    def _read_bytes(self, count, break_on_termchar=None, **kwargs):
        response, _ = self.connection.recvfrom(1024)
        return response

