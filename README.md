httperf-plot
============

httperf-plot is a python wrapper around httperf


## requirements

* httperf
* python3
* pip
* matplotlib

ubuntu:
```
sudo apt-get install httperf python3 python3-dev python3-pip python3-matplotlib
```


## matplotlib in OSX

```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```


## usage

```
usage: httperf-plot.py [-h] [--server S] [--port N] [--uri S] [--timeout X]
                       [--rate X] [--num-conns N] [--num-calls N] [--method S]
                       [--add-header S] [--wsesslog N,X,F] [--ramp-up X,N]

httperf-plot is a python wrapper around httperf

optional arguments:
  -h, --help        show this help message and exit
  --server S        specifies the IP hostname S of the server
  --port N          specifies the port number N on which the web server is
                    listening for HTTP requests
  --uri S           specifies that URI S should be accessed on the server
  --timeout X       specifies the amount of time X that httperf is willing to
                    wait for a server reaction
  --rate X          specifies the fixed rate X at which connections or
                    sessions are created
  --num-conns N     specifies the total number of connections N to create
  --num-calls N     specifies the total number of calls N to issue on each
                    connection before closing it
  --method S        specifies the method S that should be used when issuing an
                    HTTP request
  --add-header S    specifies to include string S as an additional request
                    header
  --wsesslog N,X,F  specifies the following parameters: N is the number of
                    sessions to initiate, X is the user think-time (in
                    seconds) that separates consecutive call bursts, and many
                    aspects of user sessions can be specified in an input file
                    F
  --ramp-up X,N     specifies the ramp-up rate X, times N (httperf-plot
                    parameter)
```
