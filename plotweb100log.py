#!/usr/bin/env python
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

f = open(sys.argv[1])
header = f.readline()
d={}
idx={}
ridx={}
x=[]
l=0
sample=0.1

for i,h in enumerate(header.strip().split('\t')):
	d[h]=[]
	idx[h]=i
	ridx[i]=h
for line in f.readlines():
	line=line.strip()
	x.append(l*sample)
	l+=1
	for i,v in enumerate(line.split('\t')):
		key = ridx[i]
		try:
			v=float(v)
		except:
			None
		d[key].append(v)

dCS = np.gradient(np.array(d['CongestionSignals']))
dRetrans = np.gradient(np.array(d['PktsRetrans']))

triageSendLim = []
triageRecvLim = []
triageNetLim = []

sumPktsRetrans = 0

goodputOut = []
goodputIn = []

for SndLimTimeSender, SndLimTimeRwin, SndLimTimeCwnd, DataBytesIn, DataBytesOut, PktsRetrans, DataBytesOut, DataBytesIn in \
	zip(d['SndLimTimeSender'], d['SndLimTimeRwin'], d['SndLimTimeCwnd'], d['DataBytesIn'], d['DataBytesOut'], d['PktsRetrans'], d['DataBytesOut'], d['DataBytesIn']):
	totaltime = SndLimTimeSender + SndLimTimeRwin + SndLimTimeCwnd # microseconds (not milli - kis.txt)
	triageSendLim.append(SndLimTimeSender/totaltime*100)
	triageRecvLim.append(SndLimTimeRwin/totaltime*100)
	triageNetLim.append(SndLimTimeCwnd/totaltime*100)
	sumPktsRetrans += PktsRetrans
	goodputOut.append(DataBytesOut*8/totaltime/1000) # Gbits/sec - payload only (goodput)
	goodputIn.append(DataBytesIn*8/totaltime/1000) # Gbits/sec - payload only (goodput)

plt.subplot(5,1,1)
plt.title('Web100 visualisation for '+sys.argv[1])
plt.ylabel('Slope CongestionSignals')
plt.grid('on')
plt.plot(x,dCS,'yo-')

plt.subplot(5,1,2)
plt.ylabel('Slope PktsRetrans')
plt.grid('on')
plt.plot(x,dRetrans,'bo-')

plt.subplot(5,1,3)
plt.ylabel('CurCwnd')
plt.grid('on')
plt.plot(x,d['CurCwnd'],'bo-')

plt.subplot(5,1,4)
plt.ylabel('Goodput (Gbps)')
plt.grid('on')
plt.ylim([0,10])
plt.plot(x,goodputOut,'bo-')

plt.subplot(5,1,5)
plt.ylabel('Sender congestion triage')
polys = plt.stackplot(x, triageSendLim, triageRecvLim, triageNetLim, colors=('blue','green','red'))
plt.ylim([0,100])
legendProxies = []
for poly in polys:
	legendProxies.append(plt.Rectangle((0, 0), 1, 1, fc=poly.get_facecolor()[0]))
plt.grid('on')
plt.legend(legendProxies, ['Sender limited', 'Receiver limited', 'Network limited'])
plt.xlabel('Time (s)')

plt.show()
