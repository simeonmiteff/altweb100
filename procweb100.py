import os
import struct

h = {}

WEB100_TYPE_INTEGER = 0
WEB100_TYPE_INTEGER32 = 1
WEB100_TYPE_INET_ADDRESS_IPV4 = 2
WEB100_TYPE_IP_ADDRESS = WEB100_TYPE_INET_ADDRESS_IPV4
WEB100_TYPE_COUNTER32 = 3
WEB100_TYPE_GAUGE32 = 4
WEB100_TYPE_UNSIGNED32 = 5
WEB100_TYPE_TIME_TICKS = 6
WEB100_TYPE_COUNTER64 = 7
WEB100_TYPE_INET_PORT_NUMBER = 8
WEB100_TYPE_UNSIGNED16 = WEB100_TYPE_INET_PORT_NUMBER
WEB100_TYPE_INET_ADDRESS = 9
WEB100_TYPE_INET_ADDRESS_IPV6 = 10
WEB100_TYPE_STR32 = 11
WEB100_TYPE_OCTET = 12

t = {
	WEB100_TYPE_INTEGER:'I',
	WEB100_TYPE_INTEGER32:'I',
	WEB100_TYPE_INET_ADDRESS_IPV4:'BBBB',
	WEB100_TYPE_COUNTER32:'I',
	WEB100_TYPE_GAUGE32:'I',
	WEB100_TYPE_UNSIGNED32:'I',
	WEB100_TYPE_TIME_TICKS:'Q',
	WEB100_TYPE_COUNTER64:'Q',
	WEB100_TYPE_INET_PORT_NUMBER:'H',
	WEB100_TYPE_INET_ADDRESS:'BBBB',
	WEB100_TYPE_INET_ADDRESS_IPV6:'BBBBBBBBBBBBBBBBB',
	WEB100_TYPE_STR32:'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
	WEB100_TYPE_OCTET:'B'
}

WC_STATE_CLOSED=1
WC_STATE_LISTEN=2
WC_STATE_SYNSENT=3
WC_STATE_SYNRECEIVED=4
WC_STATE_ESTABLISHED=5
WC_STATE_FINWAIT1=6
WC_STATE_FINWAIT2=7
WC_STATE_CLOSEWAIT=8
WC_STATE_LASTACK=9
WC_STATE_CLOSING=10
WC_STATE_TIMEWAIT=11
WC_STATE_DELETECB=12

def readvar(filename,varname):
	fkey = os.path.basename(filename)
	offset,t1,t2 = h[fkey][varname]
	fstring = t[t1]
	fh = open(filename)
	fh.seek(offset)
	val = fh.read(t2)
	fh.close()
	r = struct.unpack(fstring,val)
	if len(r)==1: return r[0]
	return r

def loadheader():
	hl = open("/proc/web100/header")
	tl = hl.readline() # top line
	w100file = None

	for l in hl.readlines():
		l=l.strip()
		#print ">>>",l
		if len(l)>0: # skip blank linkes
			if l[0] == '/':
				w100file = l[1:]
				if w100file not in h:
					h[w100file] = {}
			else:
				varname,offset,t1,t2 = l.split(" ")
				h[w100file][varname] = \
					(int(offset),int(t1),int(t2))

if __name__=="__main__":
	loadheader()
	#import pprint
	#pprint.pprint(h)
	import sys
	print readvar('/proc/web100/%s/read' % sys.argv[1],'State')

# wait for WC_STATE_CLOSED			
