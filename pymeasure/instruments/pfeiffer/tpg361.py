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

import logging
from pymeasure.instruments import Instrument

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class TPG361(Instrument):

    pressure = Instrument.measurement(
        'PR1', """Read pressure value."""
    )

    ethernet_config = Instrument.control(
        'ETH', 'ETH ,%s', """Configuration parameters for the ethernet interface."""
    )

    def __init__(self, resourceName, **kwargs):
        super().__init__(
            resourceName,
            "Pfeiffer TPG361",
            write_termination='\r',
            read_termination='\r\n',
            **kwargs
        )

    def ask(self, command, query_delay=0.1):
        """Write a command to the instrument and return the read response.

        :param command: Command string to be sent to the instrument.
        :param query_delay: Delay between writing and reading in seconds.
        :returns: String returned by the device without read_termination.
        """
        # - write the command --------------------------------- #
        self.write(command)
        self.wait_for(query_delay)

        # - read the acknowledgement -------------------------- #
        ack = self.read()

        # - send the enquiry byte and read the response ------- #
        self.write('\x05')
        self.wait_for(query_delay)
        resp = self.read()
        self.wait_for(query_delay)

        # - ensure the read buffer is clean ------------------- #
        try:
            self.read()
        except Exception:
            pass

        return resp
