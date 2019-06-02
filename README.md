# RSVP Project v.1.0
    A simple project written on Python2.7 based on custom RSVP protocol implementation.
    The application provides support of basic RSVP features and can be deployed on various network devices powered by Linux

## INSTALLATION NOTES

### NECESSARY MODULES TO BE IMPORTED
	apt-get -y install python-daemon
	apt-get -y install python-lockfile
	apt-get -y install python-scapy

### FOR GENERATING RSVP PACKAGES
    #### To import contrib package, which contains rsvp class:
	https://github.com/levigross/Scapy/blob/master/scapy/contrib/rsvp.py # RSVP
	
	$ mkdir /usr/lib/python2.7/dist-packages/scapy/contrib
	$ cp rsvp.py /usr/lib/python2.7/dist-packages/scapy/contrib/
	$ touch /usr/lib/python2.7/dist-packages/scapy/contrib/__init__.py
	
### ENABLE IP FORWARDING ON MIDDLE INSTANCES
	$ echo 1 > /proc/sys/net/ipv4/ip_forward
	
### WORKAROUNDS (WILL BE FIXED SOON)
	# ON ALL INSTANCES
	$ mkdir res
	$ touch res/my_daemon.log
	Note: "res" directory should be at the same level as "src"

	
## RUNNING THE APPLICATION
	# On all instances run daemon process by executing the following command:
	python -m src.daemon_utils.RunDaemon start|stop [autobandwidth]
	
	# Send test RSVP message from first instance via command:
	python -m src.rsvp.generator.GenerateRSVP
	usage: GenerateRSVP.py -src SRC_IP -dst DST_IP -tos TOS -rate RATE
                       [-route ROUTE [ROUTE ...]]
	
