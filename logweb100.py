#!/usr/bin/env python
import os
import re
import sys
import struct
import time

from threading import Thread

import procweb100 as w 

w.loadheader()

cids_last = None

match = sys.argv[1:5]
outdir = sys.argv[5]
period = float(sys.argv[6])

def logcid(cid,outfile,period):
	END_OF_HEADER_MARKER="----End-Of-Header---- -1 -1\n"
	BEGIN_SNAP_DATA="----Begin-Snap-Data----\n"
	MAX_TMP_BUF_SIZE=80
	WEB100_LOG_CID=-1
	WEB100_GROUPNAME_LEN_MAX=32
	GROUPNAME="read"
	snapcount = 0 
	f = open(outfile,'w')
	header = open("/proc/web100/header").read()
	f.write(header)
	f.write('\0')
	f.write(END_OF_HEADER_MARKER)
	f.write(struct.pack("Q",int(time.time())))
	f.write(GROUPNAME+'\0'*(WEB100_GROUPNAME_LEN_MAX-len(GROUPNAME)))
	spec = open("/proc/web100/%s/spec" % cid).read()
	p = struct.unpack("!HBBBBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxHBBBBxxxxxxxxxxxxxxxxxx",spec)
	l = [p[0]]+[0,0]+[p[x] for x in [2,1,4,3,5]]+[0,0]+[p[x] for x in [7,6,9,8]]
	f.write(struct.pack("HBBBBBBHBBBBBB",*l))
	state = w.readvar("/proc/web100/%s/read" % cid,'State')
	while state != w.WC_STATE_CLOSED:
		f.write(BEGIN_SNAP_DATA)
		snap=open("/proc/web100/%s/read" % cid).read()
		f.write(snap)
		snapcount += 1
		time.sleep(period)
		state = w.readvar("/proc/web100/%s/read" % cid,'State')
	f.close()
	print "Wrote %d snapshots to %s, thread exiting." % (snapcount,outfile)

connseen = 0
while True:
	cids_now = set(os.listdir('/proc/web100')[1:])
	if cids_last:
		new = cids_now - cids_last
		if len(new)>0:
			for n in new:
				line = file("/proc/web100/"+n+"/spec-ascii").read().strip()
				parts = re.split("[\s:]",line);
				nomatch = False
				for m,v in zip(match,parts):
					if m != '-': # if field is not wildcard
						if m != v: # if field does not match
							nomatch = True # skip to the next connection
				# if we got here, at least one connection matches
				if not nomatch:
					connseen += 1
					print "Detected maching cid", n,\
						 w.readvar("/proc/web100/"+n+"/read",'Duration'), "us after connection."
					thread = Thread(target=logcid, args=(n,outdir+"/w100_"+str(connseen)+".log",period))
					print "Starting logging thread for connection %d" % connseen
					thread.start()
					print "Main thread waiting for more connections..."
	cids_last = cids_now
