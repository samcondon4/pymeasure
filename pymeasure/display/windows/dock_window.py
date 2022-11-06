#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2022 PyMeasure Developers
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

from ..widgets.dock_widget import DockWidget
from ..widgets.log_widget import LogWidget
from .managed_window import ManagedWindowBase

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class DockWindow(ManagedWindowBase):
    """
    Display experiment output with multiple docking windows with
    :class:`~pymeasure.display.widgets.dock_widget.DockWidget` class.

    :param procedure_class: procedure class describing the experiment (see
        :class:`~pymeasure.experiment.procedure.Procedure`)
    :param x_axis: the data column(s) for the x-axis of the plot. This may be string or a list
        of strings from the data columns of the procedure.
    :param y_axis: the data column(s) for the y-axis of the plot. This may be string or a list
        of strings from the data columns of the procedure.
    :param num_plots: the number of plots you want displayed in the DockWindow tab
    :param \\**kwargs: optional keyword arguments that will be passed to
        :class:`~pymeasure.display.windows.managed_window.ManagedWindowBase`
    """

    def __init__(self, procedure_class, x_axis=None, y_axis=None, num_plots=1, *args, **kwargs):

        self.x_axis = x_axis
        self.y_axis = y_axis
        self.num_plots = num_plots

        self.log_widget = LogWidget("Experiment Log")
        self.dock_widget = DockWidget("Dock Tab", procedure_class, self.x_axis, self.y_axis,
                                      num_plots=num_plots)

        if "widget_list" not in kwargs:
            kwargs["widget_list"] = ()
        kwargs["widget_list"] = kwargs["widget_list"] + (self.dock_widget, self.log_widget)

        super().__init__(procedure_class, **kwargs)

        measure_quantities = []
        # Expand x_axis if it is a list
        if isinstance(self.x_axis, list):
            measure_quantities += [*self.x_axis]
        else:
            measure_quantities.append(self.x_axis)

        # Expand y_axis if it is a list
        if isinstance(self.y_axis, list):
            measure_quantities += [*self.y_axis]
        else:
            measure_quantities.append(self.y_axis)

        self.browser_widget.browser.measured_quantities.update(measure_quantities)

        logging.getLogger().addHandler(self.log_widget.handler)  # needs to be in Qt context?
        log.setLevel(self.log_level)
        log.info("DockWindow connected to logging")
