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
from pyvisa.constants import StopBits, Parity
from pymeasure.instruments import Instrument
from pymeasure.instruments.lakeshore.lakeshore_base import LakeShoreTemperatureChannel

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class LakeShore218(Instrument):
    """ Represents the Lakeshore 218 temperature monitor and provides a high-level interface for
    interacting with the instrument.
    """

    i_ch = Instrument.ChannelCreator(
        LakeShoreTemperatureChannel,
        [0, 1, 2, 3, 4, 5, 6, 7, 8],
        prefix='input_'
    )

    def __init__(self, adapter, **kwargs):
        kwargs.setdefault('name', 'Lakeshore Model 218 Temperature Controller')
        kwargs.setdefault('read_termination', '\r\n')
        super().__init__(
            adapter,
            data_bits=7,
            parity=Parity.odd,
            stop_bits=StopBits.one,
            **kwargs
        )
