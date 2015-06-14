# altweb100
altweb100 re-implements a small subset of the official [Web100]{http://www.web100.org/} user-space functionality. This code is likely to be obsolete very soon. I hope it is useful to someone else, but before using altweb100, consider:

* Using the official [Web100 tools]{http://www.web100.org/download/}.
* Switching to [Web10G]{http://www.web10g.org/} and it's associated tools.
* Using [TCP\_INFO]{https://code.google.com/p/ndt/wiki/TCP_INFOvsWeb100Web10g} instead.

# Why?
I needed instrumentation of Linux TCP behaviour and already had machines with Web100-patched Linux kernels on our lab servers. The effort to switch to the new Web10G patch was a distraction I couldn't afford at the time (I tried, but chickened out after getting a kernel Oops).

More specifically, I wanted Web100 variables logged for new connections *matching a particular src/dst port/IP tuple* and this is not something the existing Web100 tools could do. I also needed the logging to start very soon after connection establishment. Unfortunately the existing Web100 userspace library did not have the functions I needed to implement a new logging tool, and I simply could not get the netlink API for web100 to work, so I wrote my own library for parsing **/proc/web100/header** and **/proc/web100/PID/read**.

# Usage
Run **logweb100.py** as root with the following 6 parameters: **source-ip**, **source-port**, **dest-ip**, **dest-port**, **output-dir** and **samle-period**. Use **-** to denote a wildcard for any of the first four parameters. For example, to log all connections to destination port 5201, writing logs to **/tmp** with a period of 0.01s:

```
logweb100.py - - - 5201 /tmp/ 0.01
```

This will write a files named w100\_*CID*.log in the standard web100 binary log format. It keeps running, starting a new thread for each matching connection. To convert these to a text format, use the **logvars2** utility (available [here]{http://www.hep.man.ac.uk/u/stevek/public/logvars2/}):

```
logvars2 -p binary.log > textlog.csv
```

Finally, **plotweb100log.py** does some rudimentary visualisation of logvars2 text log files:

![Example plotweb100log.py output](/screenshot.png?raw=true "Example plotweb100log.py output")

# Copyright and license
This code is copyright 2014-2015 the CSIR, and released under [the Apache 2.0 license](LICENSE).
