#!/usr/bin/python3

import sys
import os
import numpy as np
from scipy import stats

class Lat(object):
    def __init__(self, fileName):
        f = open(fileName, 'rb')
        a = np.fromfile(f, dtype=np.uint64)
        self.reqTimes = a.reshape((a.shape[0]//3, 3))
        f.close()

    def parseQueueTimes(self):
        return self.reqTimes[:, 0]

    def parseSvcTimes(self):
        return self.reqTimes[:, 1]

    def parseSojournTimes(self):
        return self.reqTimes[:, 2]

if __name__ == '__main__':
    def getLatPct(latsFile):
        assert os.path.exists(latsFile)

        latsObj = Lat(latsFile)

        qTimes = [l/1e6 for l in latsObj.parseQueueTimes()]
        svcTimes = [l/1e6 for l in latsObj.parseSvcTimes()]
        sjrnTimes = [l/1e6 for l in latsObj.parseSojournTimes()]
        f = open('lats.txt','w')

        f.write('%12s | %12s | %12s\n\n' \
                % ('QueueTimes', 'ServiceTimes', 'SojournTimes'))

        for (q, svc, sjrn) in zip(qTimes, svcTimes, sjrnTimes):
            f.write("%12s | %12s | %12s\n" \
                    % ('%.3f' % q, '%.3f' % svc, '%.3f' % sjrn))
        f.close()
        p50 = stats.scoreatpercentile(sjrnTimes, 50)
        p90 = stats.scoreatpercentile(sjrnTimes, 90)
        p95 = stats.scoreatpercentile(sjrnTimes, 95)
        p99 = stats.scoreatpercentile(sjrnTimes, 99)
        avgLat = stats.hmean(sjrnTimes)
        # ms
        print("p50 %.3f" % p50)
        print("p90 %.3f" % p90)
        print("p95 %.3f" % p95)
        print("p99 %.3f" % p99)
        print("avg %.3f" % avgLat)

    latsFile = sys.argv[1]
    getLatPct(latsFile)

