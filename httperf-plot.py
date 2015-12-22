# -*- coding: utf-8 -*-

""" httperf-plot

.. moduleauthor:: limseok <gtolarc@gmail.com>
"""

import argparse
import re
import subprocess

from plot import Canvas


def parse_args():
    parser = argparse.ArgumentParser(description='httperf-plot is a python wrapper around httperf')

    parser.add_argument('--server', metavar='S',
                        dest='--server', action='store',
                        help='specifies the IP hostname S of the server')
    parser.add_argument('--port', metavar='N',
                        dest='--port', action='store',
                        help='specifies the port number N on which the web server is listening for HTTP requests')
    parser.add_argument('--uri', metavar='S',
                        dest='--uri', action='store',
                        help='specifies that URI S should be accessed on the server')
    parser.add_argument('--timeout', metavar='X',
                        dest='--timeout', action='store',
                        help='specifies the amount of time X that httperf is willing to wait for a server reaction')
    parser.add_argument('--rate', metavar='X',
                        dest='--rate', action='store',
                        help='specifies the fixed rate X at which connections or sessions are created')
    parser.add_argument('--num-conns', metavar='N',
                        dest='--num-conns', action='store',
                        help='specifies the total number of connections N to create')
    parser.add_argument('--num-calls', metavar='N',
                        dest='--num-calls', action='store',
                        help='specifies the total number of calls N to issue on each connection before closing it')
    parser.add_argument('--method', metavar='S',
                        dest='--method', action='store',
                        help='specifies the method S that should be used when issuing an HTTP request')
    parser.add_argument('--add-header', metavar='S',
                        dest='--add-header', action='store',
                        help='specifies to include string S as an additional request header')
    parser.add_argument('--wsesslog', metavar='N,X,F',
                        dest='--wsesslog', action='store',
                        help='specifies the following parameters: N is the number of sessions to initiate, '
                             'X is the user think-time (in seconds) that separates consecutive call bursts, '
                             'and many aspects of user sessions can be specified in an input file F')

    parser.add_argument('--ramp-up', metavar='X,N',
                        dest='--ramp-up', action='store',
                        help='specifies the ramp-up rate X, times N (httperf-plot parameter)')

    return vars(parser.parse_args())


def httperf_once(args):
    rst = {}

    out_bytes = subprocess.check_output(['httperf'] + ['='.join(arg) for arg in args.items() if arg[1] is not None])
    out_bytes_str = out_bytes.decode()
    print(out_bytes_str)

    rst['Number of requests'] = int(re.findall(r'(Total: connections \d+ requests )(\d+)', out_bytes_str)[0][1])
    rst['Rate'] = int(args['--rate'])
    rst['Request rate'] = float(re.findall(r'(Request rate: )(\d+\.\d+)', out_bytes_str)[0][1])
    rst['Response time'] = float(re.findall(r'(Reply time \[ms\]: response )(\d+\.\d+)', out_bytes_str)[0][1])
    rst['Response status 1xx'] = int(re.findall(r'(1xx=)(\d+)', out_bytes_str)[0][1])
    rst['Response status 2xx'] = int(re.findall(r'(2xx=)(\d+)', out_bytes_str)[0][1])
    rst['Response status 3xx'] = int(re.findall(r'(3xx=)(\d+)', out_bytes_str)[0][1])
    rst['Response status 4xx'] = int(re.findall(r'(4xx=)(\d+)', out_bytes_str)[0][1])
    rst['Response status 5xx'] = int(re.findall(r'(5xx=)(\d+)', out_bytes_str)[0][1])

    return rst


def httperf_plot(data):
    parse_data = [(datum['Rate'], datum['Request rate']) for datum in data]
    a = Canvas(title='Rate - Request rate', xlab='Rate', ylab='Request rate',
               xrange=(0, max([datum['Rate'] for datum in data])),
               yrange=(-5, max([datum['Request rate'] for datum in data]) + 5))
    a.plot(parse_data).save('plot1.png')

    parse_data = [(datum['Rate'], datum['Response time']) for datum in data]
    b = Canvas(title='Rate - Response time', xlab='Rate', ylab='Response time',
               xrange=(0, max([datum['Rate'] for datum in data])),
               yrange=(-5, max([datum['Response time'] for datum in data]) + 5))
    b.plot(parse_data).save('plot2.png')

    parse_data = [(datum['Rate'],
                   (datum['Response status 2xx'] + datum['Response status 3xx']) / datum['Number of requests'] * 100.0)
                  for datum in data]
    c = Canvas(title='Rate - Success rate', xlab='Rate', ylab='Success rate',
               xrange=(0, max([datum['Rate'] for datum in data])),
               yrange=(-5, 100 + 5))
    c.plot(parse_data).save('plot3.png')

    Canvas.show()


if __name__ == '__main__':
    args = parse_args()
    plot_data = []

    if args['--ramp-up'] is not None:
        ramp_up = args['--ramp-up'].split(',')
        del args['--ramp-up']

        for i in range(int(ramp_up[1])):
            plot_data.append(httperf_once(args))
            args['--rate'] = str(int(args['--rate']) + int(ramp_up[0]))

        httperf_plot(plot_data)
    else:
        httperf_once(args)
