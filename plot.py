# -*- coding: utf-8 -*-

""" plot

.. moduleauthor:: limseok <gtolarc@gmail.com>
"""

# import matplotlib
#
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg


class Canvas(object):
    def __init__(self, title='', xlab='x', ylab='y', xrange=None, yrange=None):
        self.fig = plt.figure()
        self.fig.set_facecolor('white')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title(title)
        self.ax.set_xlabel(xlab)
        self.ax.set_ylabel(ylab)
        if xrange:
            self.ax.set_xlim(xrange)
        if yrange:
            self.ax.set_ylim(yrange)
        self.legend = []

    @staticmethod
    def show():
        plt.show()

    def save(self, filename='plot.png'):
        FigureCanvasAgg(self.fig).print_png(open(filename, 'wb'))

    def plot(self, data, color='green', style='-', width=2, legend=None, xrange=None):
        if callable(data) and xrange:
            x = [xrange[0] + 0.01 * i * (xrange[1] - xrange[0]) for i in range(0, 101)]
            y = [data(p) for p in x]
        else:
            x, y = [p[0] for p in data], [p[1] for p in data]
        q = self.ax.plot(x, y, linestyle=style, linewidth=width, color=color)
        if legend:
            self.legend.append((q[0], legend))
            legend = self.ax.legend([e[0] for e in self.legend],
                                    [e[1] for e in self.legend])
            legend.get_frame().set_alpha(0.5)
        return self
